<script lang="ts">
  import Header from "./components/Header.svelte";
  import FormScreen from "./form/FormScreen.svelte";
  import MapScreen from "./form/MapScreen.svelte";
  import CollectionScreen from "./collection/CollectionScreen.svelte";
  import DetailScreen from "./collection/DetailScreen.svelte";
  import FinishRun from "./form/finishRun.svelte";

  let screen = "home";
  let animal = "";
  let distance = "";
  let selectedRun: {
    start_time: string;
    end_time: string;
    actual_distance_km: number;
    pace_min_per_km: number;
    calories: number;
    animal_name: string;
    track_geojson: {
      type: string;
      coordinates: [number, number][];
    };
  } | null = null;
  let screenHistory: string[] = [];

  // 次の画面への遷移
  const nextScreen = () => {
    console.log("送信された動物:", animal);
    console.log("送信された距離:", distance);
    goToScreen("mapScreen");
  };

  // 詳細画面に遷移するためにrunを設定
  const detail = (run: {
    start_time: string;
    end_time: string;
    actual_distance_km: number;
    pace_min_per_km: number;
    calories: number;
    animal_name: string;
    track_geojson: {
      type: string;
      coordinates: [number, number][];
    };
  }) => {
    selectedRun = run; // 選択したランの情報をselectedRunに格納
    goToScreen("detail"); // 詳細画面に遷移
  };

  const goToScreen = (newScreen: string) => {
    screenHistory.push(screen);
    screen = newScreen;
  };

  const goBack = () => {
    const prev = screenHistory.pop();
    if (prev) {
      screen = prev;
    } else {
      screen = "home"; // 戻る先がない場合はホームへ
    }
  };
  const handleStart = () => {
    screen = "finishRun"; //完走ページへ
  };

  const goHome = () => {
    screen = "home";
  };
  
  const goCollection = () => {
    screen = "collectionScreen"
  };
</script>

<main>
  {#if screen === "home"}
    <Header />

    <div class="logo">
      <img
        src="./DrawingRunning_logo.png"
        class="logo"
        alt="DrawingRunningのロゴ"
      />
    </div>

    <div class="button-container">
      <button class="action-button" on:click={() => goToScreen("formScreen")}>
        開始
      </button>
      <button
        class="action-button"
        on:click={() => goToScreen("collectionScreen")}
      >
        コレクション
      </button>
    </div>
  {/if}

  {#if screen === "formScreen"}
    <FormScreen bind:animal bind:distance {nextScreen} {goBack} />
  {/if}

  {#if screen === "mapScreen"}
    <MapScreen {animal} {distance} {goBack} {handleStart} />
  {/if}

  {#if screen === "collectionScreen"}
    <CollectionScreen {goBack} {detail} />
  {/if}

  {#if screen === "detail"}
    <DetailScreen {goBack} run={selectedRun} />
  {/if}

  {#if screen === "finishRun"}
    <FinishRun {goHome} {goCollection} run={selectedRun} />
  {/if}
</main>

<style>
  .logo {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 70vh;
  }

  .logo img {
    width: 600px;
    height: auto;
  }

  .button-container {
    margin-top: auto;
    padding-bottom: 2rem;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    align-items: center;
  }

  .action-button {
    width: 240px;
    padding: 1rem 1.5rem;
    font-size: 1.1rem;
    font-weight: bold;
    border: none;
    border-radius: 12px;
    background-color: #fea900;
    color: white;
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
    transition: all 0.2s ease-in-out;
  }

  .action-button:hover {
    background-color: #d29418;
    transform: translateY(-2px);
    cursor: pointer;
  }

  @media (max-width: 600px) {
    .logo img {
      width: 400px;
      height: auto;
    }

    .action-button {
      width: 80%;
      font-size: 1rem;
    }
  }
</style>
