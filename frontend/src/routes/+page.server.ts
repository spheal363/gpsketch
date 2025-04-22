import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ locals: { supabase } }) => {
  // Supabaseの`profiles`テーブルから、`name`カラムのみを5件取得（名前順でソート）
  const { data: profiles } = await supabase
    .from("profiles")
    .select("name")
    .limit(5)
    .order("name");

  // クライアント側に渡すデータ。もし取得できなければ空配列を返す
  return { profiles: profiles ?? [] };
};
