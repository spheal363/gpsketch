<script lang="ts">
  import RouteMap from "../RouteMap.svelte";
  import Loading from "../components/Loading.svelte";
  export let animal: string;
  export let distance: string;
  export let backToHome: () => void;

  let loading = false;

  const handleStart = async () => {
    loading = true;

    // 仮の処理（ここをAPI呼び出しやローカル処理に置き換えてOK）
    await new Promise(resolve => setTimeout(resolve, 2000));

    loading = false;
  };
</script>

{#if loading}
  <Loading />
{:else}
  <div class="wrapper">
    <div class="map-container">
      <RouteMap {animal} {distance} />
    </div>

    <div class="button-group">
      <button class="route-button" on:click={handleStart}>
        このルートで走る！
      </button>
      <button class="back-button" on:click={backToHome}>
        戻る
      </button>
    </div>
  </div>
{/if}

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

  .button-group {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
    width: 100%;
    max-width: 400px;
  }

  .route-button,
  .back-button {
    width: 100%;
    padding: 0.75rem 1rem;
    font-size: 1rem;
    font-weight: bold;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: background-color 0.2s;
  }

  .route-button {
    background-color: #FEA900;
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
      height: 40vh;
    }

    .route-button,
    .back-button {
      font-size: 0.95rem;
    }
  }
</style>
