<!--
@component
- バックエンドから受け取った経路を地図上に表示するコンポーネント
- 東京駅を中心として地図を初期化し、マーカーと経路を表示します。
-->

<script>
  export const ssr = false;
  import { onMount } from "svelte";
  import LocationProvider from "./LocationProvider.svelte";

  // animalとdistanceのプロパティを受け取るように宣言
  export let animal = "hiyoko"; // デフォルト値を設定
  export let distance = 10; // デフォルト値をkm単位で設定

  let map;
  let routeLayer;
  let loading = true;
  let errorMessage = "";
  let locationData = null;  // 位置情報を格納する変数を初期化
  let L;

  // 位置情報が更新されたときの処理
  function handleLocationUpdate(event) {
    locationData = event.detail;
    if (locationData && L) {
      initializeMap(locationData.latitude, locationData.longitude);
      generateRoute();
    }
  }

  // 位置情報の取得に失敗したときの処理
    errorMessage = event.detail.message;
    // 位置情報が取得できない場合は東京駅を使用
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
    if (map) return; // 既に初期化されている場合は何もしない
    
    map = L.map("map").setView([lat, lng], 15);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: "© OpenStreetMap contributors",
    }).addTo(map);

    // 現在位置にマーカーを追加
    L.marker([lat, lng]).addTo(map).bindPopup("現在位置").openPopup();
  }

  // ルート生成関数
  async function generateRoute() {
    if (!map || !locationData) {
      errorMessage = "地図が初期化されていないか、位置情報が取得できていません";
      loading = false;
      return;
    }

    try {
      // animalとdistanceをログに出力
      console.log(`形状: ${animal}、距離: ${distance}km`);
      console.log(`緯度: ${locationData.latitude}、経度: ${locationData.longitude}`);
      // 既存のルートレイヤーがあれば削除
      if (routeLayer) {
        map.removeLayer(routeLayer);
      }

      // バックエンドに送信するデータ
      const requestData = {
        shape: animal,
        length: parseFloat(distance) || 10.0, // 数値に変換、変換できない場合はデフォルト値
        latitude: locationData.latitude,
        longitude: locationData.longitude
      };

      console.log("APIリクエスト送信:", requestData);

      // バックエンドAPIを呼び出し
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
      // バックエンドから経路を取得 const res = await fetch("http://localhost:5000/api/route"); const geo = await res.json();
      

      // 取得した経路を地図に描画
      routeLayer = L.geoJSON(routeData, {
        style: {
          color: "red",
          weight: 8,
          opacity: 0.7,
        },
      }).addTo(map);
      map.fitBounds(routeLayer.getBounds());
    } catch (err) {
      console.error("経路情報の取得に失敗しました", err);
      errorMessage = "経路の取得に失敗しました。ネットワーク接続を確認してください。";
    } finally {
      loading = false;
    }
  }

  onMount(async () => {
    // Leafletライブラリをインポート
    L = await import("leaflet");
    await import("leaflet/dist/leaflet.css");

    // もし位置情報がすでにあれば地図を初期化
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

<div id="map"></div>

<style>
  #map {
    width: 100%;
    height: 100vh;
  }
</style>
