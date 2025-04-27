<!-- src/routes/form/MapScreen.svelte -->
<script lang="ts">
  import RouteMap from "../RouteMap.svelte";
  import { goto } from "$app/navigation"; // SvelteKitのページ遷移用関数

  import { goto } from "$app/navigation"; // SvelteKitのページ遷移用関数

  export let animal: string;
  export let distance: string;
  export let handleStart: (routeId: string) => void;
  export let goBack: () => void;
  export const ssr = false;
  import { onMount } from "svelte";
  import CurrentLocation from "../CurrentLocationMap.svelte";
  import LocationProvider from "../LocationProvider.svelte";
  import { goto } from "$app/navigation";

  let errorMessage = ""; // エラー内容を格納
  const numericDistance = Number(distance);
  let routeId: string | null = null; // route_idを保持
  let latitude: number | null = null; // 現在地の緯度
  let longitude: number | null = null; // 現在地の経度

  // 現在地を取得
  const getCurrentLocation = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          latitude = position.coords.latitude;
          longitude = position.coords.longitude;
          console.log("現在地を取得しました:", { latitude, longitude });
        },
        (error) => {
          console.error("現在地の取得に失敗しました:", error);
          alert("現在地の取得に失敗しました。位置情報を有効にしてください。");
        }
      );
    } else {
      alert("このブラウザでは位置情報がサポートされていません。");
    }
  };

  // ルート生成時にroute_idを取得
  const onRouteGenerated = (event: CustomEvent<{ routeId: string }>) => {
    routeId = event.detail.routeId;
  };

  // navigateページに遷移
  const startRun = async () => {
    if (!routeId) {
      alert("ルートが生成されていません。");
      return;
    }

    if (latitude === null || longitude === null) {
      alert("現在地が取得されていません。もう一度お試しください。");
      return;
    }

    try {
      // /api/run/startエンドポイントを呼び出す

      // navigateページに遷移
      goto(`/navigate?route_id=${routeId}`);
    } catch (error) {
      console.error("ランの開始中にエラーが発生しました:", error);
      alert("ランの開始中にエラーが発生しました。");
    }
  };

  // コンポーネントがマウントされたときに現在地を取得
  getCurrentLocation();

  // 子コンポーネントからエラーを受け取ったときの処理
  function handleChildError(event) {
    const message = event.detail?.message || "不明なエラーが発生しました";
    errorMessage = message;
    console.error("MapScreenで受け取ったエラー:", errorMessage);

    // エラーメッセージをクエリパラメータに乗せてErrorScreenへ移動
    goto(`/form/error?message=${encodeURIComponent(errorMessage)}`);
  }
  let totalDistance = 0;

  function handleDistanceUpdate(event: CustomEvent<number>) {
    totalDistance = event.detail;
  }
</script>


<div class="wrapper">
  <div class="map-container">
    <RouteMap
      {animal}
      distance={numericDistance}
      on:updateDistance={handleDistanceUpdate}
    />
  </div>
  <div class="total-distance">
    {#if totalDistance > 0}
      <p>総距離: {totalDistance} km</p>
    {:else}
      <p>経路データがまだありません</p>
    {/if}
  </div>
  <div class="button-container">
    <button class="route-button" on:click={handleStart}>このルートで走る</button
    >
    <button class="back-button" on:click={goBack}>戻る</button>
  </div>
</div>

<style>
  .wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 1rem;
    gap: 1rem;
    min-height: 100vh;
    box-sizing: border-box;
    background-color: #000d41;
    background-color: #000d41;
  }

  .map-container {
    width: 100%;
    max-width: 600px;
    height: 75vh;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
  }

  .button-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
    width: 100%;
    max-width: 400px;
  }

  .route-button,
  .back-button {
    width: 60%;
    padding: 0.75rem 1rem;
    font-size: 1rem;
    font-weight: bold;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: background-color 0.2s;
  }

  .route-button {
    background-color: #fea900;
    color: white;
  }

  .route-button:hover {
    background-color: #d29418;
  }

  .back-button {
    background-color: #777;
    color: white;
  }

  .back-button:hover {
    background-color: rgba(119, 119, 119, 0.7);
  }

  @media (max-width: 600px) {
    .map-container {
      height: 70vh;
    }

    .route-button,
    .back-button {
      font-size: 0.95rem;
    }
  }
  .total-distance p {
    color: white;
    margin: 0;
    padding: 0;
  }
</style>
