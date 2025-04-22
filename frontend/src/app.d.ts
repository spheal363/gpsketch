import type { Session, SupabaseClient, User } from "@supabase/supabase-js";
import type { Database } from "./database.types.ts"; // Supabaseの自動生成型をインポート

// グローバルな型定義の拡張（SvelteKitで使用）
declare global {
  namespace App {
    /**
     * サーバー側（hooks.server.tsなど）で使える値を定義。
     * `event.locals` 経由でアクセスされる。
     */
    interface Locals {
      supabase: SupabaseClient<Database>; // Supabaseクライアント（型付き）
      safeGetSession: () => Promise<{
        session: Session | null; // セッション情報（JWT）
        user: User | null; // ログインユーザー情報
      }>;
      session: Session | null; // 認証済みのセッション（nullの場合は未ログイン）
      user: User | null; // 認証済みのユーザー（nullの場合は未ログイン）
    }

    /**
     * ページロード時（+page.tsなど）にクライアント/サーバー両方で取得可能な値を定義。
     */
    interface PageData {
      session: Session | null; // クライアント側でも使えるセッション情報
    }

    // 必要に応じて以下も拡張できます：
    // interface Error {}     // エラーページ用の型
    // interface PageState {} // クライアント状態の保持用
    // interface Platform {}  // 特定プラットフォームでの型定義（Cloudflareなど）
  }
}

export {};
