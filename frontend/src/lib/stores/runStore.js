import { writable } from 'svelte/store';

// ランデータを保存するストア
export const runs = writable([]);
// 読み込み状態を保存するストア
export const isLoading = writable(false);
// エラー情報を保存するストア
export const error = writable(null);

// APIからデータを取得する関数
export const fetchRunCollection = async () => {
  isLoading.set(true);
  error.set(null);
  
  try {
    const response = await fetch("http://localhost:5000/api/runs");
    
    if (!response.ok) {
      throw new Error('ラン記録の取得に失敗しました');
    }
    
    const data = await response.json();
    runs.set(data);
  } catch (err) {
    console.error('エラー:', err);
    error.set(err.message);
  } finally {
    isLoading.set(false);
  }
};