<!-- src/routes/form/ErrorScreen.svelte -->
<script lang="ts">
  import { page } from '$app/stores';
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';

  let message = "不明なエラーが発生しました";

  function returnHome() {
    goto('/');
  }

  onMount(() => {
    const searchParams = $page.url.searchParams;
    const paramMessage = searchParams.get('message');
    if (paramMessage) {
      message = paramMessage;
    } else {
      // 直接アクセスされた場合はトップに戻す
      console.warn("直接アクセスされたのでホームに戻ります");
      returnHome();
    }
  });
</script>

<div class="error-container">
  <div class="icon">⚠️</div>
  <h1>エラーが発生しました</h1>
  <p>{message}</p>

  <button class="back-button" on:click={returnHome}>ホームに戻る</button>
</div>

<style>
  .error-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    padding: 2rem;
    background-color: #1b1b1b;
    color: #ff4c4c;
    text-align: center;
    animation: shake 0.5s ease-in-out;
  }

  .icon {
    font-size: 4rem;
    margin-bottom: 1rem;
    animation: pulse 1.5s infinite;
  }

  h1 {
    font-size: 2rem;
    margin-bottom: 1rem;
    font-weight: bold;
    color: #ff0000;
  }

  p {
    font-size: 1rem;
    margin-bottom: 2rem;
    max-width: 600px;
    word-break: break-word;
  }

  button {
    background-color: #777;
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    font-size: 1.1rem;
    font-weight: bold;
    border-radius: 0.5rem;
    cursor: pointer;
    transition: background-color 0.3s;
  }

  button:hover {
    background-color: rgba(192, 192, 192, 0.7);
  }

  @keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.2); }
    100% { transform: scale(1); }
  }

  @keyframes shake {
    0%, 100% { transform: translateX(0); }
    20%, 60% { transform: translateX(-10px); }
    40%, 80% { transform: translateX(10px); }
  }
</style>