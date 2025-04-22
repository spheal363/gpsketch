<script>
  import { invalidate } from "$app/navigation";
  import Navigation from "$lib/components/Navigation.svelte";
  import { onMount } from "svelte";

  // propsから`data`と`children`を取得
  let { data, children } = $props();

  // dataから`session`と`supabase`を取り出す（これはおそらく $derived はカスタム関数か何か）
  let { session, supabase } = $derived(data);

  // コンポーネントがマウントされた時に処理を実行
  onMount(() => {
    // 認証状態が変化したときのリスナーを登録
    const { data } = supabase.auth.onAuthStateChange((_, newSession) => {
      // セッションの有効期限が変わった場合、SvelteKitにキャッシュの無効化を通知
      if (newSession?.expires_at !== session?.expires_at) {
        invalidate("supabase:auth");
      }
    });

    // コンポーネントがアンマウントされたとき、リスナーを解除
    return () => data.subscription.unsubscribe();
  });
</script>

<Navigation {session} />

<!-- 子要素を描画 -->
{@render children()}
