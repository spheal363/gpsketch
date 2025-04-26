<script lang="ts">
  import { mockRuns } from "../../lib/mock/mockRuns.js"; // 仮データの読み込み

  // 仮データの型を定義
  interface Run {
    start_time: string;
    end_time: string;
    actual_distance_km: number;
    pace_min_per_km: number;
    calories: number;
    animal_name: string;
  }

  let runs: Run[] = mockRuns;

  export let goBack: () => void;
  export let detail: (run: Run) => void;
</script>

<div class="center-wrapper">
  <button class="back-button" on:click={goBack}>戻る</button>
</div>

<h2>ラン記録一覧（仮）</h2>

<!-- 仮データを表示する部分 -->
<ul>
  {#each runs as run}
    <li>
      <button class="run-item" type="button" on:click={() => detail(run)}>
        <strong>動物名:</strong>
        {run.animal_name}
        <strong>距離:</strong>
        {run.actual_distance_km} km
      </button>
    </li>
  {/each}
</ul>

<style>
  .center-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
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
  li {
    color: white;
  }
  h2 {
    color: white;
  }
  .run-item {
    background: none;
    border: none;
    color: white;
    text-align: left;
    font-size: 1rem;
    width: 100%;
    cursor: pointer;
    padding: 0.5rem;
  }
</style>
