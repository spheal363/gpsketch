import type { LayoutServerLoad } from "./$types";

export const load: LayoutServerLoad = async ({
  locals: { safeGetSession },
  cookies,
}) => {
  // JWTの検証付きで安全にセッション情報を取得（hooks.server.tsで定義された関数）
  const { session } = await safeGetSession();

  return {
    session, // ページやコンポーネントで使えるようにセッションを返す
    cookies: cookies.getAll(), // サーバー側でのCookie一覧を取得し、必要ならクライアントに渡す
  };
};
