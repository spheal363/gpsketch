<script lang="ts">
  export let animal: string;
  export let distance: string;
  export let nextScreen: () => void;
  export let backToHome: () => void;

  /* 走る距離入力のカウントアップ・ダウン幅 */
  const increment = () => {
    const current = parseFloat(distance) || 0;
    distance = String((current + 0.1).toFixed(1));
  };

  const decrement = () => {
    const current = parseFloat(distance) || 0;
    if (current > 0) {
      distance = String((current - 0.1).toFixed(1));
    }
  };
  // 入力が正しいかを検証する関数
  const handleInput = (e: Event) => {
    const input = e.currentTarget as HTMLInputElement; // 型キャスト
    let value = input.value;

    // 半角数字と小数点以外を除外
    value = value.replace(/[^0-9\.]/g, "");

    // 小数点が複数回入力されないように制限
    const dotCount = (value.match(/\./g) || []).length;
    if (dotCount > 1) {
      // 小数点が複数回入力されていた場合は最後の小数点を削除
      value = value.slice(0, value.lastIndexOf("."));
    }

    input.value = value; // 修正された入力値を設定
    distance = value; 
  };
</script>

<div class="form-wrapper">
  <form class="form" on:submit|preventDefault={nextScreen}>
    <h2>描きたい動物と走る距離を入力</h2>

    <select bind:value={animal} required>
      <option value="" disabled selected>動物を選択</option>
      <option value="犬">犬</option>
      <option value="猫">猫</option>
      <option value="鳥">鳥</option>
      <option value="ウサギ">ウサギ</option>
    </select>

    <div class="distance-input">
      <label>距離（km）</label>
      <div class="distance-control">
        <button type="button" class="step-button" on:click={decrement}>−</button
        >
        <input
          type="text"
          bind:value={distance}
          inputmode="decimal"
          pattern="^\d*\.?\d*$"
          required
          on:input={(e) => handleInput(e)}
          autocomplete="off"
          autocorrect="off"
          autocapitalize="off"
        />
        <button type="button" class="step-button" on:click={increment}
          >＋</button
        >
      </div>
    </div>

    <button type="submit">ルート生成</button>
  </form>

  <button class="back-button" on:click={backToHome}>戻る</button>
</div>

<style>
  .form-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 2rem;
    min-height: 100vh;
    background-color: #000d41;
  }

  .form {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    width: 100%;
    max-width: 400px;
    background: white;
    padding: 2rem;
    border-radius: 1rem;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
  }

  select,
  input {
    padding: 0.75rem;
    font-size: 1rem;
    border: 1px solid #ccc;
    border-radius: 8px;
    outline: none;
    width: 100%;
  }

  .distance-input label {
    margin-bottom: 0.25rem;
    font-weight: bold;
  }

  .distance-control {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .distance-control input {
    text-align: center;
    max-width: 100px;
  }

  .step-button {
    background-color: #e0e0e0;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 8px;
    font-size: 1.2rem;
    font-weight: bold;
    cursor: pointer;
    transition: background-color 0.2s;
    user-select: none;
    touch-action: manipulation;
  }

  button[type="submit"] {
    padding: 0.75rem;
    background-color: #fea900;
    color: white;
    font-weight: bold;
    border: none;
    border-radius: 8px;
    transition: background-color 0.2s;
    width: 100%;
  }

  .back-button {
    padding: 0.75rem;
    margin-top: 1rem;
    background-color: #777;
    color: white;
    font-weight: bold;
    border: none;
    border-radius: 8px;
    transition: background-color 0.2s;
    width: 400px;
  }

  .step-button:hover {
    background-color: rgba(192, 192, 192, 0.7);
  }

  button[type="submit"]:hover {
    background-color: #d29418;
  }

  .back-button:hover {
    background-color: rgba(119, 119, 119, 0.7);
  }

  @media (max-width: 600px) {
    .form {
      padding: 1.5rem;
    }

    .step-button {
      padding: 0.5rem;
      font-size: 1rem;
    }

    .distance-control input {
      max-width: 80px;
    }

    .back-button {
      max-width: 100%;
    }
  }
</style>
