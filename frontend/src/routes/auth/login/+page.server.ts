import { redirect, fail } from "@sveltejs/kit";
import { z } from "zod";
import type { Actions } from "./$types";

// 入力データの検証ルールを定義
const loginSchema = z.object({
  email: z.string().email("メールアドレスの形式ではありません。"),
  password: z.string().min(6, "6文字以上入力する必要があります。"),
});

export const actions: Actions = {
  default: async ({ request, locals: { supabase } }) => {
    const formData = Object.fromEntries(await request.formData());

    // 入力データを検証
    const result = loginSchema.safeParse(formData);
    if (!result.success) {
      // 検証エラーがある場合、エラーメッセージを返す
      return fail(400, { errors: result.error.flatten().fieldErrors });
    }

    const { email, password } = result.data;

    // Supabaseでログイン処理
    const { error } = await supabase.auth.signInWithPassword({
      email,
      password,
    });
    if (error) {
      console.error(error);
      return fail(400, { errors: { general: "ログインに失敗しました" } });
    }

    throw redirect(303, "/settings/profile");
  },
};
