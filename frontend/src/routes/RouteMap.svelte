<!--
@component
- バックエンドから受け取った経路を地図上に表示するコンポーネント
- 東京駅を中心として地図を初期化し、マーカーと経路を表示します。
-->

<script>
  export const ssr = false;
  import { onMount } from "svelte";

  let map;

  onMount(async () => {
    // Leafletライブラリをインポート
    const L = await import("leaflet");
    await import("leaflet/dist/leaflet.css");

    // サンプルとして東京駅の緯度経度をバックエンドに渡す
    const tokyoStation = [35.681236, 139.767125];
    // 地図を初期化
    map = L.map("map").setView(tokyoStation, 15);

    // OpenStreetMapのタイルレイヤー（地図の右下に書いてあるやつ）を追加
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: "© OpenStreetMap contributors",
    }).addTo(map);

    // 東京駅にマーカーを追加
    L.marker(tokyoStation).addTo(map).bindPopup("東京駅（中心）").openPopup();

    try {
      // TODO: ユーザが入力した値（形、距離）をバックエンドに渡す

      // バックエンドから経路を取得
      const res = await fetch("http://localhost:5000/api/route");
      const geo = await res.json();

      // 取得した経路を地図に描画
      const layer = L.geoJSON(geo, {
        style: {
          color: "red",
          weight: 8,
          opacity: 0.7,
        },
      }).addTo(map);
      map.fitBounds(layer.getBounds());
    } catch (err) {
      console.error("経路情報の取得に失敗しました", err);
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
