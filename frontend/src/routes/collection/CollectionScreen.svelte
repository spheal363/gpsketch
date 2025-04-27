<script lang="ts">
  import { onMount } from 'svelte';
  import { runs, isLoading, error, fetchRunCollection } from '../../lib/stores/runStore';

  export let goBack: () => void;
  export let detail: (run: Run) => void;

  // コンポーネントがマウントされたらデータを取得
  onMount(() => {
    fetchRunCollection();
  });
</script>

<header class="page-header">
  <h1>ラン記録一覧（仮）</h1>
</header>

{#if $isLoading}
  <div class="loading">
    <div class="spinner"></div>
    <p>ラン記録を読み込み中...</p>
  </div>
{:else if $error}
  <div class="error">{$error}</div>
  <div class="center-wrapper">
    <button class="retry-button" on:click={fetchRunCollection}>再試行</button>
  </div>
{:else if $runs.length === 0}
  <div class="empty-state">記録がありません</div>
{:else}
  <div class="card-list">
    {#each $runs as run}
      <div class="card" on:click={() => detail(run)}>
        <div class="card-content">
          <div><strong>描いた動物名:</strong> {run.animal_name}</div>
          <div><strong>距離:</strong> {run.actual_distance_km} km</div>
        </div>
      </div>
    {/each}
  </div>
{/if}

<div class="center-wrapper">
  <button class="back-button" on:click={goBack}>戻る</button>
</div>

<style>
  .page-header {
    background-color: #000825; 
    padding: 1rem 1rem;
    margin-bottom: 1rem;
    text-align: center;
    box-shadow: 0 2px 6px rgba(0,0,0,0.2);
  }

  .page-header h1 {
    margin: 0;
    color: white;
    font-size: 1.8rem;
  }

  .card-list {
    display: flex;
    flex-direction: column;
    align-items: center; 
    gap: 1rem;
    padding: 1rem;
  }

  .card {
    background-color: white;
    border-radius: 12px;
    padding: 1rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    cursor: pointer;
    transition: transform 0.2s, box-shadow 0.2s;
    width: 300px; /* ← 横幅を固定（例えば300px） */
    max-width: 90%; /* スマホ対応で縮む */
  }

  .card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
  }

  .card-content {
    color: #000d41;
    font-size: 1rem;
  }

  .center-wrapper {
    display: flex;
    justify-content: center;
    margin-top: 2rem;
  }

  .back-button {
    padding: 0.75rem;
    background-color: #777;
    color: white;
    font-weight: bold;
    border: none;
    border-radius: 8px;
    transition: background-color 0.2s;
    width: 200px;
  }

  .back-button:hover {
    background-color: rgba(119, 119, 119, 0.7);
  }

  @media (max-width: 600px) {
    .back-button {
      max-width: 100%;
    }
  }
</style>
