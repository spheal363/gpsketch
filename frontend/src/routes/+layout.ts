import {
  createBrowserClient,
  createServerClient,
  isBrowser,
} from "@supabase/ssr";
import {
  PUBLIC_SUPABASE_ANON_KEY,
  PUBLIC_SUPABASE_URL,
} from "$env/static/public";
import type { LayoutLoad } from "./$types";

export const load: LayoutLoad = async ({ data, depends, fetch }) => {
  /**
   * この`depends`を指定することで、`supabase:auth`に依存していることを明示できます。
   * 例えばセッションが更新されたときに、このレイアウトの再読み込みが発生します。
   */
  depends("supabase:auth");

  // 実行環境（ブラウザ or サーバー）によってSupabaseクライアントを切り替え
  const supabase = isBrowser()
    ? createBrowserClient(PUBLIC_SUPABASE_URL, PUBLIC_SUPABASE_ANON_KEY, {
        global: {
          fetch,
        },
      })
    : createServerClient(PUBLIC_SUPABASE_URL, PUBLIC_SUPABASE_ANON_KEY, {
        global: {
          fetch,
        },
        cookies: {
          // サーバー側では、セッション情報をCookieから取得する必要があるため
          getAll() {
            return data.cookies;
          },
        },
      });

  /**
   * `getSession()`はクライアント側では直接セッションを取得可能。
   * サーバー側では`LayoutData`（hooks経由で検証済みセッションをセット）をもとにセッション情報を得るので安全です。
   */
  const {
    data: { session },
  } = await supabase.auth.getSession();

  // 現在ログイン中のユーザー情報を取得
  const {
    data: { user },
  } = await supabase.auth.getUser();

  // ページ側に渡すデータ
  return { session, supabase, user };
};
