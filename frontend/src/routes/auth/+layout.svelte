<script>
  let { children } = $props();
</script>

<header>
  <nav>
    <a href="/">Home</a>
    <a href="/auth/login">Login</a>
    <a href="/auth/signup">Sign up</a>
  </nav>
</header>

{@render children()}
