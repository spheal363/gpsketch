import type { EmailOtpType } from '@supabase/supabase-js'
import { redirect } from '@sveltejs/kit'
import type { RequestHandler } from './$types'

export const GET: RequestHandler = async ({ url, locals: { supabase } }) => {
  // URLクエリからワンタイムトークン情報を取得
  const token_hash = url.searchParams.get('token_hash')
  const type = url.searchParams.get('type') as EmailOtpType | null
  const next = url.searchParams.get('next') ?? '/' // 認証後のリダイレクト先

  /**
   * リダイレクトURLを構築し、認証に使用したパラメータを削除
   * `next` はエラー時に使うので残しておく
   */
  const redirectTo = new URL(url)
  redirectTo.pathname = next
  redirectTo.searchParams.delete('token_hash')
  redirectTo.searchParams.delete('type')

  // トークンとタイプが揃っていれば、認証処理を行う
  if (token_hash && type) {
    const { error } = await supabase.auth.verifyOtp({ type, token_hash })

    if (!error) {
      // 認証成功：`next` も削除してからリダイレクト
      redirectTo.searchParams.delete('next')
      redirect(303, redirectTo)
    }
  }

  // 認証失敗またはパラメータ不足時はエラーページへ
  redirectTo.pathname = '/auth/error'
  redirect(303, redirectTo)
}
