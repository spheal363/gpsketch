<!--
@component
- SvelteKitのルートページ（http://localhost:5173/）
-->

<script>
    import CurrentLocationMap from "./CurrentLocationMap.svelte";
    import RouteMap from "./RouteMap.svelte";
</script>

<!-- ナビゲーション -->
<nav>
    <a href="/">home</a>
    <a href="/sample">sample</a>
</nav>

<h1>Welcome to SvelteKit</h1>
<p>
    Visit <a href="https://svelte.dev/docs/kit">svelte.dev/docs/kit</a> to read the
    documentation
</p>

<!-- 現在位置を表示する地図コンポーネント -->
<!-- <CurrentLocationMap /> -->

<!-- バックエンドから受け取ったルートを表示する地図コンポーネント -->
<RouteMap />
