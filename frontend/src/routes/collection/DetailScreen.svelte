<script lang="ts">
    export let backToHome: () => void;
</script>

<div class="center-wrapper">
    <button class="back-button" on:click={backToHome}>戻る</button>
</div>
