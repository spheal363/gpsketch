<!--
@component
- 現在位置を表示する地図コンポーネント
- このコンポーネントは、Leafletライブラリを使用して現在位置を地図上に表示します。
- ユーザーの位置情報を取得し、地図を初期化してマーカーを配置します。
-->

<script lang="ts">
  export const ssr = false;

  import { onMount } from "svelte";
  import { goto } from "$app/navigation";

  let map;

  onMount(async () => {
    try {
      const L = await import("leaflet");
      await import("leaflet/dist/leaflet.css");

      if (!navigator.geolocation) {
        throw new Error("このブラウザでは位置情報がサポートされていません。");
      }

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
          let errorMessage = "位置情報の取得に失敗しました。";

          switch (error.code) {
            case 1:
              errorMessage = "位置情報の利用が許可されていません。";
              break;
            case 2:
              errorMessage = "位置情報を取得できませんでした。";
              break;
            case 3:
              errorMessage = "位置情報取得がタイムアウトしました。";
              break;
          }

          console.error("位置情報エラー:", errorMessage);
          goto(`/form/error?message=${encodeURIComponent(errorMessage)}`);
        },
        { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
      );
    } catch (err) {
      const fallbackMessage = err instanceof Error ? err.message : "未知のエラーが発生しました。";
      console.error("地図初期化エラー:", fallbackMessage);
      goto(`/form/error?message=${encodeURIComponent(fallbackMessage)}`);
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
