<script lang="ts">
    export let backToHome: () => void;
  </script>
  
  <div class="center-wrapper">
    <button class="back-button" on:click={backToHome}>戻る</button>
  </div>
  
  <style>
    .center-wrapper {
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh; /* 画面全体の中央に */
    }
  
    .back-button {
      padding: 0.75rem;
      background-color: #777;
      color: white;
      font-weight: bold;
      border: none;
      border-radius: 8px;
      transition: background-color 0.2s;
      width: 400px;
    }

    .back-button:hover {
      background-color: rgba(119, 119, 119, 0.7); /* グレー + 透過 */
    }
  
    @media (max-width: 600px) {
      .back-button {
        max-width: 100%;
      }
    }
  </style>
  