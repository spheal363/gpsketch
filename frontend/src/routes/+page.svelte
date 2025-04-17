<script>
    export let data;
    export let error;
</script>

<h1>Welcome to SvelteKit</h1>
<p>Visit <a href="https://svelte.dev/docs/kit">svelte.dev/docs/kit</a> to read the documentation</p>

{#if error}
    <div style="color: red;">
        <h2>Error</h2>
        <p>{error}</p>
    </div>
{:else if data}
    <h2>Data from Backend:</h2>
    <pre>{JSON.stringify(data, null, 2)}</pre>
{:else}
    <p>Loading...</p>
{/if}