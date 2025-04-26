<script lang="ts">
  import Loading from "$lib/components/Loading.svelte";
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";

  // actionsから渡されるエラーなどを取得
  let { data, message } = $props();
  let isLoading = false;

  // セッション情報を取得してリダイレクト
  let { session } = $derived(data);

  onMount(() => {
    if (session) {
      goto("/"); // セッションが存在する場合、ルートページにリダイレクト
    }
  });
</script>

<form method="POST" on:submit={() => (isLoading = true)}>
  <p>
    <input name="email" type="email" placeholder="メールアドレス" required />
    {#if message?.errors?.email}
      <span class="error">{message.errors.email[0]}</span>
    {/if}
  </p>
  <p>
    <input name="password" type="password" placeholder="パスワード" required />
    {#if message?.errors?.password}
      <span class="error">{message.errors.password[0]}</span>
    {/if}
  </p>

  {#if isLoading}
    <Loading size="30px" color="#3498db" />
  {:else}
    <button type="submit">ログイン</button>
  {/if}

  {#if message?.errors?.general}
    <p class="error">{message.errors.general}</p>
  {/if}

  <p>
    <a href="/auth/signup">パスワードを忘れた方はこちら</a>
  </p>
  <p>
    <a href="/auth/signup">アカウントを作成する</a>
  </p>
</form>
