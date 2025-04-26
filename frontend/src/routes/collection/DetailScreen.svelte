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

{#if run}
    <div>
        <h3>ラン詳細</h3>
        <p><strong>動物名:</strong> {run.animal_name}</p>
        <p><strong>開始時刻:</strong> {run.start_time}</p>
        <p><strong>終了時刻:</strong> {run.end_time}</p>
        <p><strong>距離:</strong> {run.actual_distance_km} km</p>
        <p><strong>ペース:</strong> {run.pace_min_per_km} 分/km</p>
        <p><strong>カロリー:</strong> {run.calories} kcal</p>
    </div>
{:else}
    <div>
        <p>詳細情報がありません。</p>
    </div>
{/if}

<button on:click={goBack}>戻る</button>
<style>
    div{
        color:white;
    }
</style>
