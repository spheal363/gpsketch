<script lang="ts">
  import { invalidate } from "$app/navigation";
  import type { PageData } from "./$types";

  let { data } = $props();
  let { profile, supabase } = $derived(data);

  let name = profile?.name ?? "";
  let introduce = profile?.introduce ?? "";
  let avatar_url = profile?.avatar_url ?? "";

  const handleUpdate = async (e: SubmitEvent) => {
    e.preventDefault();
    const {
      data: { session },
    } = await supabase.auth.getSession();
    if (!session?.user) return;

    const updates = {
      id: session.user.id,
      name,
      introduce,
      avatar_url,
    };

    const { error } = await supabase.from("profiles").upsert(updates);
    if (error) console.error(error);

    invalidate();
  };
</script>

<h1>プロフィール設定</h1>

<form on:submit={handleUpdate}>
  <label>
    名前:
    <input bind:value={name} />
  </label>
  <label>
    自己紹介:
    <textarea bind:value={introduce}></textarea>
  </label>
  <label>
    アバター画像URL:
    <input type="url" bind:value={avatar_url} />
  </label>
  <button type="submit">保存</button>
</form>

{#if avatar_url}
  <img src={avatar_url} alt="アバター" width="100" />
{/if}
