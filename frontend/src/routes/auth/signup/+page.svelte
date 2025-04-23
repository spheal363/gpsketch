<script>
  import Loading from "$lib/components/Loading.svelte";

  let isLoading = false; // サインアップ処理中かどうかを管理するフラグ

  // 入力値を管理する変数
  let name = "";
  let email = "";
  let password = "";
</script>

<form method="POST" on:submit={() => (isLoading = true)}>
  <p>
    <input name="name" type="text" placeholder="名前" bind:value={name} />
  </p>
  <p>
    <input
      name="email"
      type="email"
      placeholder="メールアドレス"
      bind:value={email}
    />
  </p>
  <p>
    <input
      name="password"
      type="password"
      placeholder="パスワード"
      bind:value={password}
    />
  </p>

  {#if isLoading}
    <Loading size="30px" color="#3498db" />
  {:else}
    <button type="submit">サインアップ</button>
  {/if}

  <p>
    <a href="/auth/login">ログインはこちら</a>
  </p>
</form>

<style>
  .error {
    color: red;
    font-size: 0.9em;
  }
</style>
