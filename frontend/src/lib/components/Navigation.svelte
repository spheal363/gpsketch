<script>
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";

  export let session;

  const logout = async () => {
    if (session?.supabase) {
      const { error } = await session.supabase.auth.signOut();
      if (error) console.error(error);
      goto("/auth/login");
    }
  };
</script>

<header>
  <nav>
    {#if session?.user}
      <a href="/settings/profile">プロフィール</a>
      <button on:click={logout}>ログアウト</button>
    {:else}
      <a href="/auth/login">Login</a>
      <a href="/auth/signup">Sign up</a>
    {/if}
  </nav>
</header>
