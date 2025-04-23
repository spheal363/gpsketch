<script>
  import Loading from "$lib/components/Loading.svelte";

  let isLoading = false; // サインアップ処理中かどうかを管理するフラグ
</script>

<form method="POST" on:submit={() => (isLoading = true)}>
  <p>
    <input name="email" type="email" placeholder="メールアドレス" required />
  </p>
  <p>
    <input name="password" type="password" placeholder="パスワード" required />
  </p>

  {#if isLoading}
    <Loading size="30px" color="#3498db" />
  {:else}
    <button type="submit">ログイン</button>
  {/if}

  <p>
    <a href="/auth/signup">パスワードを忘れた方はこちら</a>
  </p>
  <p>
    <a href="/auth/signup">アカウントを作成する</a>
  </p>
</form>
