<script lang="ts">
    import { onMount } from 'svelte';
    import confetti from 'canvas-confetti';
    export let goHome: () => void;
    export let goCollection: () => void;
  
    let message = "完走おめでとう！";
  
    onMount(() => {
      console.log("完走ページに到達！");
      console.log("完走ページに到達！");
      confetti({
        particleCount: 150,
        spread: 70,
        origin: { y: 0.6 }
      });
    });
  
    export let run: {
        start_time: string;
        end_time: string;
        actual_distance_km: number;
        pace_min_per_km: number;
        calories: number;
        animal_name: string;
    } | null = null;
</script>

<div class="complete-wrapper">
  <h1>{message}</h1>

  {#if run}
    <div class="detail-card">
      <h3>ラン詳細</h3>
      <div class="detail-item"><strong>動物名:</strong> {run.animal_name}</div>
      <div class="detail-item"><strong>開始時刻:</strong> {run.start_time}</div>
      <div class="detail-item"><strong>終了時刻:</strong> {run.end_time}</div>
      <div class="detail-item"><strong>距離:</strong> {run.actual_distance_km} km</div>
      <div class="detail-item"><strong>ペース:</strong> {run.pace_min_per_km} 分/km</div>
      <div class="detail-item"><strong>消費カロリー:</strong> {run.calories} kcal</div>
    </div>
  {:else}
    <div class="no-data">
      <h3>ラン詳細</h3>
      <p>詳細情報がありません。</p>
    </div>
  {/if}


  <div class="button-container">
    <button class="button" on:click={goHome}>ホームに戻る</button>
    <button class="button" on:click={goCollection}>コレクション画面</button>
  </div>
</div>  

<style>
  .complete-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 4rem 2rem;
    color: white;
    text-align: center;
    min-height: 100vh;
    background: linear-gradient(135deg, #000d41, #0031c3);
  }

  h1 {
    font-size: 1.5rem;
    margin-top: 11rem;
    margin-bottom: 2rem;
    color: #ffd700;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.6);
  }

  .detail-card {
      background-color: white;
      border-radius: 12px;
      padding: 0.5rem 1.5rem 1.5rem 1.5rem; /* 上だけ1remにして、他は1.5rem */
      width: 300px;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
      color: #000d41;
      margin-bottom: 2rem;
  }

  .detail-card h3 {
      font-size: 1.5rem;
      text-align: center;
      margin-bottom: 1rem;
  }

  .detail-item {
      margin-bottom: 0.8rem;
      font-size: 1rem;
  }

  .no-data {
    background-color: white;
    border-radius: 12px;
    padding: 1.2rem;
    width: 300px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    color: #000d41;
    margin-bottom: 2rem;
    text-align: center;
  }

  .button-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1.5rem;
    width: 100%;
    max-width: 400px;
  }

  .button {
    width: 60%;
    padding: 0.75rem 1rem;
    font-size: 1rem;
    font-weight: bold;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: background-color 0.2s;
    background-color: #fea900;
    color: white;
  }

  .button:hover {
    background-color: #d29418;
  }

  @media (max-width: 600px) {
    .stats-card {
      width: 90%;
    }
  }
</style>