<!-- src/routes/form/MapScreen.svelte -->
<script lang="ts">
  import RouteMap from "../RouteMap.svelte";
  export let animal: string;
  export let distance: string;
  export let handleStart: () => void;
  export let goBack: () => void;
  export const ssr = false;
  import { onMount } from "svelte";
  import CurrentLocation from "../CurrentLocationMap.svelte";
  import LocationProvider from "../LocationProvider.svelte";
  import { goto } from "$app/navigation";

  let errorMessage = ""; // エラー内容を格納
  const numericDistance = Number(distance);

  // 子コンポーネントからエラーを受け取ったときの処理
  function handleChildError(event) {
    const message = event.detail?.message || "不明なエラーが発生しました";
    errorMessage = message;
    console.error("MapScreenで受け取ったエラー:", errorMessage);

    // エラーメッセージをクエリパラメータに乗せてErrorScreenへ移動
    goto(`/form/error?message=${encodeURIComponent(errorMessage)}`);
  }
</script>

<div class="wrapper">
  <div class="map-container">
    <RouteMap {animal} distance={numericDistance} on:error={handleChildError} />
  </div>

  <div class="button-container">
    <button class="route-button" on:click={handleStart}>このルートで走る</button>
    <button class="back-button" on:click={goBack}>戻る</button>
  </div>
</div>

<style>
  .wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 1rem;
    gap: 2rem;
    min-height: 100vh;
    box-sizing: border-box;
    background-color: #000D41;
  }

  .map-container {
    width: 100%;
    max-width: 600px;
    height: 75vh; 
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 8px 16px rgba(0,0,0,0.1);
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
    background-color:  #FEA900;
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
      height: 75vh;
    }

    .route-button,
    .back-button {
      font-size: 0.95rem;
    }
  }
</style>
