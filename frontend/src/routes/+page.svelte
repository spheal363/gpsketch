<script>
  import Header from './components/Header.svelte';
  import FormScreen from "./form/FormScreen.svelte";
  import MapScreen from "./form/MapScreen.svelte";
  import CollectionScreen from "./collection/CollectionScreen.svelte";

  let screen = "home";
  let animal = "";
  let distance = "";

  const nextScreen = () => screen = "mapScreen";
  const backToHome = () => screen = "home";
</script>

<main>
  {#if screen === "home"}
    <Header />

    <div class="button-container">
      <button class="action-button" on:click={() => screen = "formScreen"}>
        開始
      </button>
      <button class="action-button" on:click={() => screen = "collectionScreen"}>
        コレクション
      </button>
    </div>
  {/if}

  {#if screen === "formScreen"}
    <FormScreen {animal} {distance} {nextScreen} {backToHome} />
  {/if}

  {#if screen === "mapScreen"}
    <MapScreen {backToHome}/>
  {/if}

  {#if screen === "collectionScreen"}
    <CollectionScreen {backToHome} />
  {/if}
</main>

<style>
  main {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    padding: 1rem;
    background-color: #f0f4f8;
  }

  .button-container {
    margin-top: auto;
    padding-bottom: 2rem;
    display: flex;
    flex-direction: column;
    gap: 1.2rem;
    align-items: center;
  }

  .action-button {
    width: 240px;
    padding: 1rem 1.5rem;
    font-size: 1.1rem;
    font-weight: bold;
    border: none;
    border-radius: 12px;
    background-color: #4CAF50;
    color: white;
    box-shadow: 0 6px 12px rgba(0,0,0,0.1);
    transition: all 0.2s ease-in-out;
  }

  .action-button:hover {
    background-color: #45a049;
    transform: translateY(-2px);
    cursor: pointer;
  }

  @media (max-width: 600px) {
    .action-button {
      width: 80%;
      font-size: 1rem;
    }
  }
</style>
