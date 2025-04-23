<script>
  export let size = "50px"; // ローディングアイコンのサイズを指定可能
  export let color = "#3498db"; // ローディングアイコンの色を指定可能
</script>

<div
  class="spinner"
  style="--size: {size}; --color: {color};"
  aria-label="Loading"
></div>

<style>
  .spinner {
    border: 4px solid transparent;
    border-top: 4px solid var(--color, #3498db);
    border-radius: 50%;
    width: var(--size, 50px);
    height: var(--size, 50px);
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    from {
      transform: rotate(0deg);
    }
    to {
      transform: rotate(360deg);
    }
  }
</style>
