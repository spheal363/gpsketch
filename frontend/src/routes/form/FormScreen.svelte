<script lang="ts">
  export let animal: string;
  export let distance: string;
  export let nextScreen: () => void;
</script>
<form on:submit|preventDefault={nextScreen}>
  <select bind:value={animal} required>
    <option value="" disabled selected>描きたい動物</option>
    <option value="犬">犬</option>
    <option value="猫">猫</option>
    <option value="鳥">鳥</option>
    <option value="ウサギ">ウサギ</option>
  </select>
  <input placeholder="走りたい距離" bind:value={distance} required />
  <button type="submit">生成</button>
</form>
