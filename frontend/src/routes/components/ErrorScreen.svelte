<script lang="ts">
  export let type: 'location' | 'route';
</script>

<div class="error-screen">
  {#if type === 'location'}
    <h2>位置情報が取得できませんでした</h2>
    <p>ブラウザの位置情報設定を確認してください。</p>
  {:else if type === 'route'}
    <h2>ルートの生成に失敗しました</h2>
    <p>ネットワーク環境やサーバーの状態をご確認ください。</p>
  {/if}
</div>

<style>
  .error-screen {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100vh;
    text-align: center;
    background-color: #ffeaea;
    color: #c00;
    padding: 2rem;
  }

  h2 {
    font-size: 1.8rem;
    margin-bottom: 1rem;
  }

  p {
    font-size: 1.2rem;
  }
</style>