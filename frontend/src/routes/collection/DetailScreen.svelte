<script lang="ts">
    export let goBack: () => void;
    export let run: {
        start_time: string;
        end_time: string;
        actual_distance_km: number;
        pace_min_per_km: number;
        calories: number;
        animal_name: string;
    } | null = null;
</script>

<div class="detail-wrapper">
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
      <p>詳細情報がありません。</p>
    </div>
  {/if}

  <button class="back-button" on:click={goBack}>戻る</button>
</div>

<style>
    .detail-wrapper {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 2rem;
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
        color: white;
        font-size: 1.2rem;
    }

    .back-button {
        background-color: #777;
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-size: 1rem;
        transition: background-color 0.2s;
        width: 200px;
    }

    .back-button:hover {
        background-color: rgba(119, 119, 119, 0.8);
        cursor: pointer;
    }

    @media (max-width: 600px) {
        .detail-card {
            width: 90%;
    }
    }
</style>
