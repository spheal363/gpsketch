<!--
@component
- バックエンドから受け取った経路を地図上に表示するコンポーネント
- 東京駅を中心として地図を初期化し、マーカーと経路を表示します。
-->

<script>
  export const ssr = false;
  import { onMount, createEventDispatcher } from "svelte";
  import LocationProvider from "./LocationProvider.svelte";
  import Loading from "./components/Loading.svelte";

  // animalとdistanceのプロパティを受け取るように宣言
  export let animal = "hiyoko"; // デフォルト値を設定
  export let distance = 10; // デフォルト値をkm単位で設定

  let map;
  let routeLayer;
  let imageOverlay;
  let loading = true;
  let errorMessage = "";
  let locationData = null;
  let L;
  let waypointMarkers = [];

  const dispatch = createEventDispatcher(); // 親に通知するためのdispatcher

  // 位置情報が更新されたときの処理
  function handleLocationUpdate(event) {
    locationData = event.detail;
    if (locationData && L) {
      initializeMap(locationData.latitude, locationData.longitude);
      generateRoute();
    }
  }

  // 位置情報の取得に失敗したときの処理
  function handleLocationError(event) {
    errorMessage = event.detail.message;
    dispatch('error', { message: errorMessage }); // 親に通知
    locationData = {
      latitude: 35.681236,
      longitude: 139.767125
    };
    if (L) {
      initializeMap(locationData.latitude, locationData.longitude);
      generateRoute();
    }
  }

  // 地図初期化関数
  function initializeMap(lat, lng) {
    if (map) return;
    map = L.map("map").setView([lat, lng], 15);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: "© OpenStreetMap contributors",
    }).addTo(map);

    delete L.Icon.Default.prototype._getIconUrl;
    L.Icon.Default.mergeOptions({
      iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
      iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
      shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png'
    });

    L.marker([lat, lng]).addTo(map).openPopup();
  }

  // マーカーを削除する関数
  function clearWaypointMarkers() {
    waypointMarkers.forEach(marker => {
      if (map) map.removeLayer(marker);
    });
    waypointMarkers = [];
  }

  // 青色のマーカーを作成するためのカスタムアイコン
  function createBlueIcon() {
    return L.divIcon({
      className: 'blue-marker',
      iconSize: [25, 25],
      iconAnchor: [12, 12],
      html: '<div style="background-color: #1E90FF; border-radius: 50%; width: 100%; height: 100%; border: 2px solid white;"></div>'
    });
  }

  // 動物の画像をオーバーレイする関数
  function addAnimalImageOverlay(waypoints) {
    if (imageOverlay && map) {
      map.removeLayer(imageOverlay);
    }
    if (waypoints.length < 3) {
      console.error("経由地点が不十分です");
      return null;
    }

    let imageUrl;
    switch(animal) {
      case 'hiyoko':
        imageUrl = 'imgs/hiyoko.png'; break;
      case 'kuma':
        imageUrl = 'imgs/kuma.png'; break;
      case 'uma':
        imageUrl = 'imgs/uma.png'; break;
      case 'yunicorn':
        imageUrl = 'imgs/yunicorn.png'; break;
      default:
        imageUrl = 'imgs/hiyoko.png'; break;
    }

    let lats = waypoints.map(p => p.lat);
    let lngs = waypoints.map(p => p.lng);
    let minLat = Math.min(...lats), maxLat = Math.max(...lats);
    let minLng = Math.min(...lngs), maxLng = Math.max(...lngs);
    let centerLat = (minLat + maxLat) / 2;
    let centerLng = (minLng + maxLng) / 2;
    let maxSize = Math.max(maxLat - minLat, maxLng - minLng);
    let scaleFactor = 1.0;

    let bounds = [
      [centerLat - maxSize * scaleFactor / 2, centerLng - maxSize * scaleFactor / 2],
      [centerLat + maxSize * scaleFactor / 2, centerLng + maxSize * scaleFactor / 2]
    ];

    imageOverlay = L.imageOverlay(imageUrl, bounds, {
      opacity: 0.9,
      interactive: false,
      zIndex: 400
    }).addTo(map);

    console.log("画像境界ボックス:", bounds);
    return bounds;
  }

  // マップの表示範囲を調整する関数
  function adjustMapView(bounds) {
    if (!map || !bounds) return;
    map.fitBounds(bounds, {
      padding: [20, 20], // 少しだけ余白を追加
      maxZoom: 14,       // 最大ズームレベルを制限
      animate: true      // アニメーションを有効化
    });
    console.log("マップの表示範囲を調整しました");
  }

  // ルート生成関数
  async function generateRoute() {
    loading = true;
    if (!map || !locationData) {
      errorMessage = "地図が初期化されていないか、位置情報が取得できていません";
      dispatch('error', { message: errorMessage });
      loading = false;
      return;
    }

    try {
      console.log(`形状: ${animal}、距離: ${distance}km`);
      console.log(`緯度: ${locationData.latitude}、経度: ${locationData.longitude}`);

      if (routeLayer) map.removeLayer(routeLayer);
      clearWaypointMarkers();

      const requestData = {
        shape: animal,
        length: parseFloat(distance) || 10.0,
        latitude: locationData.latitude,
        longitude: locationData.longitude
      };

      console.log("APIリクエスト送信:", requestData);

      const response = await fetch("http://localhost:5000/api/route/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "経路生成に失敗しました");
      }

      const routeData = await response.json();
      console.log("APIレスポンス:", routeData);

      if (!routeData.features || routeData.features.length === 0) {
        throw new Error("経路データが空です");
      }

      if (routeData.waypoints && routeData.waypoints.length > 0) {
        const blueIcon = createBlueIcon();
        routeData.waypoints.forEach((waypoint, index) => {
          const popupContent = waypoint.name 
            ? `ポイント ${index + 1}: ${waypoint.name}` 
            : `ポイント ${index + 1}`;
          const marker = L.marker([waypoint.lat, waypoint.lng], {
            icon: blueIcon
          }).addTo(map);
          marker.bindTooltip(popupContent, {
            direction: 'top',
            offset: [0, -10]
          });
          waypointMarkers.push(marker);
        });
      }

      console.log("経由地点", routeData.waypoints);
      console.log("総距離", routeData.total_distance);

      routeLayer = L.geoJSON(routeData, {
        style: {
          color: "red",
          weight: 8,
          opacity: 0.7,
        },
      }).addTo(map);

      setTimeout(() => {
        const imageBounds = addAnimalImageOverlay(routeData.waypoints);
        if (imageBounds) {
          setTimeout(() => {
            adjustMapView(imageBounds);
          }, 200);
        }
      }, 300);

    } catch (err) {
      console.error("経路情報の取得に失敗しました", err);
      errorMessage = "経路の取得に失敗しました。ネットワーク接続を確認してください。";
      dispatch('error', { message: errorMessage }); // 親に通知
    } finally {
      loading = false;
    }
  }

  onMount(async () => {
    const leaflet = await import("leaflet");
    L = leaflet.default;
    await import("leaflet/dist/leaflet.css");

    if (locationData) {
      initializeMap(locationData.latitude, locationData.longitude);
      generateRoute();
    }
  });
</script>

<!-- LocationProviderコンポーネントを使用して位置情報を取得 -->
<LocationProvider 
  on:locationUpdate={handleLocationUpdate}
  on:error={handleLocationError}
  autoGet={true}
/>
{#if loading}
  <Loading />
{/if}
<div id="map"></div>

<style>
  #map {
    width: 100%;
    height: 100vh;
  }
  :global(.blue-marker) {
    background: transparent;
    border: none;
  }
  :global(.leaflet-tooltip) {
    background: rgba(0, 0, 0, 0.7);
    color: white;
    border: none;
    border-radius: 4px;
    padding: 4px 8px;
    font-size: 12px;
  }
  :global(.leaflet-tooltip-top:before) {
    border-top-color: rgba(0, 0, 0, 0.7);
  }
</style>
