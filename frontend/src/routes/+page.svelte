<script>
  import Header from './components/Header.svelte';
  import FormScreen from "./form/FormScreen.svelte";
  import MapScreen from "./form/MapScreen.svelte";
  import CollectionScreen from "./collection/CollectionScreen.svelte";

  let screen = "home";
  let animal = "";
  let distance = "";

  const nextScreen = () => {
    console.log("送信された動物:", animal);
    console.log("送信された距離:", distance);
    screen = "mapScreen";
  };

  const backToHome = () => screen = "home";
  const backToForm = () => screen = "formScreen";
</script>

<main>
  {#if screen === "home"}
    <Header />

    <div class = "logo">
      <img src="./DrawingRunning_logo.png" class="logo">
    </div>

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
    <FormScreen bind:animal bind:distance {nextScreen} {backToHome} />
  {/if}

  {#if screen === "mapScreen"}
    <MapScreen {animal}{distance}{backToForm}/>
  {/if}

  {#if screen === "collectionScreen"}
    <CollectionScreen {backToHome} />
  {/if}
</main>

<style>
  .main {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    padding: 1rem;
  }

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
    background-color: #FEA900;
    color: white;
    box-shadow: 0 6px 12px rgba(0,0,0,0.1);
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
