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

  export let backToHome: () => void;
  export let detail: () => void;
</script>

<div class="center-wrapper">
  <button class="back-button" on:click={backToHome}>戻る</button>
</div>

<h2>ラン記録一覧（仮）</h2>

<!-- 仮データを表示する部分 -->
<ul>
  {#each runs as run}
    <li>
      <strong>開始:</strong>
      {run.start_time}、
      <strong>終了:</strong>
      {run.end_time}、
      <strong>距離:</strong>
      {run.actual_distance_km} km、
      <strong>ペース:</strong>
      {run.pace_min_per_km} min/km、
      <strong>カロリー:</strong>
      {run.calories} kcal、
      <strong on:click = {detail}>動物名:</strong>
      {run.animal_name}
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
  li{
    color:white;
  }
  h2{
    color:white;
  }
</style>
