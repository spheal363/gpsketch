<script lang="ts">
  import { onMount } from 'svelte';
  
  // 親コンポーネントから直接track_geojsonを受け取る
  export let track_geojson: {
    type: string;
    coordinates: [number, number][];
  };
  
  let mapContainer: HTMLElement;
  let map: any;
  
  onMount(async () => {
    // Leafletライブラリをインポート
    const L = await import("leaflet");
    await import("leaflet/dist/leaflet.css");
    
    // 地図を初期化
    if (track_geojson && track_geojson.coordinates && track_geojson.coordinates.length > 0) {
      // 初期の中心地点として最初の座標を使用
      const firstCoord = track_geojson.coordinates[0];
      map = L.map(mapContainer).setView([firstCoord[1], firstCoord[0]], 15);
      
      // OpenStreetMapのタイルレイヤーを追加
      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: "© OpenStreetMap contributors",
      }).addTo(map);
      
      // GeoJSONデータを地図に描画
      const routeLayer = L.geoJSON({
        type: "Feature",
        geometry: track_geojson,
        properties: {}
      }, {
        style: {
          color: "#ff4500",
          weight: 5,
          opacity: 0.7
        }
      }).addTo(map);
      
      // ルートの境界に合わせて地図を調整
      map.fitBounds(routeLayer.getBounds());
      
      // スタートとゴールのマーカーを追加
      const startCoord = track_geojson.coordinates[0];
      const endCoord = track_geojson.coordinates[track_geojson.coordinates.length - 1];
      
      L.marker([startCoord[1], startCoord[0]], {
        icon: L.divIcon({
          className: 'start-marker',
          html: '<div class="marker-content">S</div>',
          iconSize: [30, 30]
        })
      }).addTo(map).bindPopup("スタート");
      
      L.marker([endCoord[1], endCoord[0]], {
        icon: L.divIcon({
          className: 'end-marker',
          html: '<div class="marker-content">G</div>',
          iconSize: [30, 30]
        })
      }).addTo(map).bindPopup("ゴール");
    }
  });
</script>

<div class="map-container" bind:this={mapContainer}></div>

<style>
  .map-container {
    width: 100%;
    height: 400px;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  }
  
  :global(.start-marker .marker-content) {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 30px;
    height: 30px;
    background-color: #4CAF50;
    color: white;
    border-radius: 50%;
    font-weight: bold;
  }
  
  :global(.end-marker .marker-content) {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 30px;
    height: 30px;
    background-color: #F44336;
    color: white;
    border-radius: 50%;
    font-weight: bold;
  }
</style>