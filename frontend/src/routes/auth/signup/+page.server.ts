import { redirect } from "@sveltejs/kit";
import { z } from "zod";
import type { Actions } from "./$types";

// 入力データの検証ルールを定義
const loginSchema = z.object({
  name: z.string().min(2, "2文字以上入力する必要があります。"),
  email: z.string().email("メールアドレスの形式ではありません。"),
  password: z.string().min(6, "6文字以上入力する必要があります。"),
});

export const actions: Actions = {
  default: async ({ request, locals }) => {
    const formData = await request.formData();
    const name = formData.get("name") as string;
    const email = formData.get("email") as string;
    const password = formData.get("password") as string;

    const { error } = await supabase.auth.signUp({ email, password });
    if (error) {
      console.error(error);
      throw redirect(303, "/auth/error");
    }

    // プロフィールの名前を更新
    const { error: updateError } = await supabase
      .from("profiles")
      .update({ name })
      .eq("email", email);
    if (updateError) {
      console.error(updateError);
      throw redirect(303, "/auth/error");
    }

    // 本登録用のURLを記載したメールを送信しました。メールをご確認の上、メール本文中のURLをクリックして、本登録を行ってください。
    throw redirect(303, "/");
  },
};
