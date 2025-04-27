<script lang="ts">
  export const ssr = false;

  import { onMount } from "svelte";
  import { browser } from "$app/environment";
  import { goto } from "$app/navigation";
  import { writable, get } from "svelte/store";

  let map: any;
  let routeId: string = "";
  let allLayers: any[] = [];
  let startTime: string = "";

  const routeData = writable<any>(null);
  const routeIndex = writable<number>(0);
  const showFullRoute = writable<boolean>(true);

  async function setupMap() {
    const L = await import("leaflet");
    await import("leaflet/dist/leaflet.css");

    map = L.map("map").setView([35.681236, 139.767125], 14);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: "© OpenStreetMap contributors",
    }).addTo(map);
  }

  function getRouteIdFromUrl() {
    const url = new URL(window.location.href);
    return url.searchParams.get("route_id");
  }

  function clearLayers() {
    allLayers.forEach((layer) => map.removeLayer(layer));
    allLayers = [];
  }

  async function fetchRoute() {
    const res = await fetch(`http://localhost:5000/api/route/${routeId}`);
    if (!res.ok) {
      alert("ルート情報が取得できませんでした。");
      goto("/");
      return;
    }
    const data = await res.json();
    console.log("取得したルートデータ:", data);

    const geojson = JSON.parse(data.route_geojson);
    const waypoints = geojson.waypoints;

    routeData.set({ ...data, waypoints });

    console.log("waypointsの数:", waypoints.length);

    if (!waypoints || waypoints.length === 0) {
      alert("経由地点データが存在しません。");
      return;
    }

    const L = await import("leaflet");
    clearLayers();

    const coordinates = geojson.features[0].geometry.coordinates;
    const latlngs = coordinates.map((c: number[]) => [c[1], c[0]]);

    const polyline = L.polyline(latlngs, { color: "blue" }).addTo(map);
    allLayers.push(polyline);

    map.fitBounds(polyline.getBounds());
  }

  async function moveToNextWaypoint() {
    const data = get(routeData);
    if (!data || !data.waypoints) {
      alert("経由地点データが存在しません。");
      return;
    }

    const waypoints = data.waypoints;
    let currentIndex = get(routeIndex);

    if (currentIndex >= waypoints.length - 1) {
      await submitCompletion();
      return;
    }

    const L = await import("leaflet");

    function areWaypointsSame(wp1: any, wp2: any) {
      if (!wp1 || !wp2) return false;
      return wp1.name === wp2.name;
    }

    let nextIndex = currentIndex + 1;

    // nextIndex同士（nextとnext+1）が同じ間スキップ
    while (
      nextIndex < waypoints.length - 1 &&
      areWaypointsSame(waypoints[nextIndex], waypoints[nextIndex + 1])
    ) {
      nextIndex++;
    }

    // 最後の地点で止まる防止
    if (nextIndex >= waypoints.length) {
      alert("すべての経由地点を通過しました。");
      return;
    }

    routeIndex.set(nextIndex);

    clearLayers();

    const geojson = JSON.parse(data.route_geojson);
    const coordinates = geojson.features[0].geometry.coordinates;
    const segments = geojson.features[0].properties.segments;

    if (get(showFullRoute)) {
      const latlngs = coordinates.map((c: number[]) => [c[1], c[0]]);
      const polyline = L.polyline(latlngs, { color: "blue" }).addTo(map);
      allLayers.push(polyline);
      map.fitBounds(polyline.getBounds());
    } else {
      const segment = segments[nextIndex];
      if (!segment || !segment.steps || segment.steps.length === 0) {
        alert("区間データが存在しません。");
        return;
      }

      const startIndex = segment.steps[0].way_points[0];
      const endIndex = segment.steps[segment.steps.length - 1].way_points[1];

      if (startIndex == null || endIndex == null || startIndex > endIndex) {
        alert("区間インデックスが無効です。");
        return;
      }

      const sectionCoords = coordinates.slice(startIndex, endIndex + 1);
      const sectionLatLngs = sectionCoords.map((c: number[]) => [c[1], c[0]]);

      if (sectionLatLngs.length === 0) {
        alert("区間ルートが存在しません。");
        return;
      }

      const sectionPolyline = L.polyline(sectionLatLngs, {
        color: "red",
        weight: 6,
        dashArray: "8,8",
        opacity: 0.8,
      }).addTo(map);

      allLayers.push(sectionPolyline);
      map.fitBounds(sectionPolyline.getBounds());
    }
  }

  function toggleRouteView() {
    showFullRoute.set(!get(showFullRoute));

    const data = get(routeData);
    if (!data || !data.waypoints) {
      alert("経由地点データが存在しません。");
      return;
    }

    const currentIndex = get(routeIndex);
    clearLayers();

    const geojson = JSON.parse(data.route_geojson);
    const coordinates = geojson.features[0].geometry.coordinates;
    const segments = geojson.features[0].properties.segments;

    if (get(showFullRoute)) {
      const latlngs = coordinates.map((c: number[]) => [c[1], c[0]]);
      const polyline = L.polyline(latlngs, { color: "blue" }).addTo(map);
      allLayers.push(polyline);
      map.fitBounds(polyline.getBounds());
    } else {
      if (!segments || segments.length === 0) {
        alert("区間データが存在しません。");
        return;
      }

      const segment = segments[currentIndex];
      if (!segment || !segment.steps || segment.steps.length === 0) {
        alert("区間ステップデータが無効です。");
        return;
      }

      const startIndex = segment.steps[0].way_points[0];
      const endIndex = segment.steps[segment.steps.length - 1].way_points[1];

      if (startIndex == null || endIndex == null || startIndex > endIndex) {
        alert("区間インデックスが無効です。");
        return;
      }

      const sectionCoords = coordinates.slice(startIndex, endIndex + 1);
      if (sectionCoords.length === 0) {
        alert("区間ルートが存在しません。");
        return;
      }

      const sectionLatLngs = sectionCoords.map((c: number[]) => [c[1], c[0]]);

      const sectionPolyline = L.polyline(sectionLatLngs, {
        color: "red",
        weight: 6,
        dashArray: "8, 8", // ← 破線設定
        opacity: 0.8,
      }).addTo(map);

      allLayers.push(sectionPolyline);

      map.fitBounds(sectionPolyline.getBounds());
    }
  }

  async function submitCompletion() {
    const data = get(routeData);
    if (!data) {
      alert("送信するルートデータがありません。");
      return;
    }

    try {
      const response = await fetch("http://localhost:5000/api/route/complete", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          route_id: routeId,
          start_time: startTime,
          geojson: JSON.parse(data.route_geojson),
        }),
      });

      if (!response.ok) {
        alert("完了データ送信に失敗しました。");
      } else {
        alert("ルート完了データを送信しました！");
      }
    } catch (error) {
      console.error("送信エラー:", error);
      alert("送信中にエラーが発生しました。");
    }
  }

  onMount(async () => {
    if (browser) {
      const id = getRouteIdFromUrl();
      if (!id) {
        alert("ルートIDが取得できませんでした。");
        goto("/");
        return;
      }
      routeId = id;

      startTime = new Date().toISOString();

      await setupMap();
      await fetchRoute();
    }
  });
</script>

<div class="controls">
  <button class="next-button" on:click={moveToNextWaypoint}>
    次の区間へ進む
  </button>
  <button class="toggle-button" on:click={toggleRouteView}>
    {#if $showFullRoute}
      区間ルート表示
    {:else}
      全体ルート表示
    {/if}
  </button>
</div>

<div id="map"></div>

<style>
  .controls {
    position: absolute;
    top: 1rem;
    left: 50%;
    transform: translateX(-50%);
    z-index: 1000;
    display: flex;
    gap: 1rem;
  }

  .next-button,
  .toggle-button {
    background-color: #0077cc;
    border: none;
    padding: 0.6rem 1.2rem;
    border-radius: 10px;
    font-size: 1rem;
    font-weight: bold;
    cursor: pointer;
    color: white;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
  }

  #map {
    width: 100%;
    height: 100vh;
  }
</style>
