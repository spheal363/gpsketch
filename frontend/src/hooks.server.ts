import { createServerClient } from "@supabase/ssr";
import { type Handle, redirect } from "@sveltejs/kit";
import { sequence } from "@sveltejs/kit/hooks";

import {
  PUBLIC_SUPABASE_URL,
  PUBLIC_SUPABASE_ANON_KEY,
} from "$env/static/public";

// Supabaseクライアントを生成し、JWTトークン検証付きでセッションを取得するハンドラ
const supabase: Handle = async ({ event, resolve }) => {
  /**
   * リクエストごとに専用のSupabaseクライアントを作成します。
   * 認証トークン（JWT）はリクエストのCookieから取得されます。
   */
  event.locals.supabase = createServerClient(
    PUBLIC_SUPABASE_URL,
    PUBLIC_SUPABASE_ANON_KEY,
    {
      cookies: {
        getAll: () => event.cookies.getAll(),
        /**
         * SvelteKitのcookie APIでは、`path`オプションを明示的に指定する必要があります。
         * `path: '/'` にすることで、従来と同じ動作を再現できます。
         */
        setAll: (cookiesToSet) => {
          cookiesToSet.forEach(({ name, value, options }) => {
            event.cookies.set(name, value, { ...options, path: "/" });
          });
        },
      },
    }
  );

  /**
   * セッションを安全に取得する関数を定義します。
   * `getSession()`はJWTの検証を行いませんが、
   * `getUser()`を併用することでJWTの有効性を確認できます。
   */
  event.locals.safeGetSession = async () => {
    const {
      data: { session },
    } = await event.locals.supabase.auth.getSession();
    if (!session) {
      return { session: null, user: null };
    }

    const {
      data: { user },
      error,
    } = await event.locals.supabase.auth.getUser();

    if (error) {
      // JWTが無効な場合
      return { session: null, user: null };
    }

    return { session, user };
  };

  return resolve(event, {
    filterSerializedResponseHeaders(name) {
      /**
       * Supabaseは`content-range`と`x-supabase-api-version`ヘッダーを使用します。
       * これらのヘッダーはSvelteKitのレスポンスに含める必要があります。
       */
      return name === "content-range" || name === "x-supabase-api-version";
    },
  });
};

// 認証チェック（認可ガード）を行うハンドラ
const authGuard: Handle = async ({ event, resolve }) => {
  const { session, user } = await event.locals.safeGetSession();
  event.locals.session = session;
  event.locals.user = user;

  // 認証されていない場合は、保護されたページ（/private）へのアクセスを拒否し、ログインページにリダイレクト
  if (!event.locals.session && event.url.pathname.startsWith("/private")) {
    redirect(303, "/auth");
  }

  // すでにログインしているユーザーが認証ページにアクセスしようとしたら、保護ページにリダイレクト
  if (event.locals.session && event.url.pathname === "/auth") {
    redirect(303, "/private");
  }

  return resolve(event);
};

// 2つのハンドラを順番に実行：supabase -> authGuard
export const handle: Handle = sequence(supabase, authGuard);
