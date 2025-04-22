<script>
  import FormScreen from "./form/FormScreen.svelte";
  import MapScreen from "./form/MapScreen.svelte";
  import CollectionScreen from "./collection/CollectionScreen.svelte";
  let screen = "home";
  let animal = "";
  let distance= "";

  const nextScreen = () => {
    screen = "mapScreen";
  };
  const backToHome = () => {
    screen = "home";
  };
</script>

{#if screen === "home"}
  <h1>お絵描きランニング</h1>
  <button on:click={() => (screen = "formScreen")}>開始</button>
  <button on:click={() => (screen = "collectionScreen")}>コレクション</button>
{/if}

{#if screen === "formScreen"}
  <FormScreen {animal} {distance} {nextScreen} {backToHome}/>
{/if}

{#if screen === "mapScreen"}
  <MapScreen />
{/if}

{#if screen === "collectionScreen"}
  <CollectionScreen {backToHome}/>
{/if}