import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ locals: { supabase } }) => {
  const {
    data: { session },
  } = await supabase.auth.getSession();
  const userId = session?.user.id;

  if (!userId) return { profile: null };

  const { data: profile } = await supabase
    .from("profiles")
    .select("email, name, introduce, avatar_url")
    .eq("id", userId)
    .single();

  return { profile };
};
