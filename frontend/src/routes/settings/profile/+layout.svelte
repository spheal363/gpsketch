<script>
  let { data, children } = $props();
  let { supabase } = $derived(data);

  const logout = async () => {
    const { error } = await supabase.auth.signOut();
    if (error) console.error(error);
  };
</script>

<header>
  <nav>
    <a href="/">Home</a>
    <a href="/settings/profile">Profile</a>
  </nav>
  <button on:click={logout}>Logout</button>
</header>

<main>
  {@render children()}
</main>
