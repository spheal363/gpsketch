<!--
@component
- 現在位置を表示する地図コンポーネント
- このコンポーネントは、Leafletライブラリを使用して現在位置を地図上に表示します。
- ユーザーの位置情報を取得し、地図を初期化してマーカーを配置します。
-->

<script>
  export const ssr = false;

  import { onMount } from "svelte";

  let map;

  onMount(async () => {
    const L = await import("leaflet");
    await import("leaflet/dist/leaflet.css");

    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const lat = position.coords.latitude;
          const lng = position.coords.longitude;

          map = L.map("map").setView([lat, lng], 15);

          L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
            attribution: "© OpenStreetMap contributors",
          }).addTo(map);

          L.marker([lat, lng]).addTo(map).bindPopup("現在位置").openPopup();
        },
        (error) => {
          console.error("位置情報の取得に失敗しました", error);
        },
      );
    } else {
      alert("このブラウザでは位置情報がサポートされていません。");
    }
  });
</script>

<div id="map"></div>

<style>
  #map {
    width: 100%;
    height: 100vh;
  }
</style>
