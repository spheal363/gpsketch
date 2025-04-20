<script>
  import FormScreen from "./form/FormScreen.svelte";
  import RouteMap from "./RouteMap.svelte";

  let screen = "home";
  let animal = "";
  let distance= "";

  const nextScreen = () => {
    screen = "mapScreen";
  };
</script>

{#if screen === "home"}
  <h1>お絵描きランニング</h1>
  <button on:click={() => (screen = "formScreen")}>開始</button>
{/if}

{#if screen === "formScreen"}
  <FormScreen {animal} {distance} {nextScreen} />
{/if}

{#if screen === "mapScreen"}
  <RouteMap />
{/if}