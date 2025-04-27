<!--
@component
- 位置情報から現在地の緯度、経度を返すコンポーネント
-->

<script lang="ts">
  import { onMount, createEventDispatcher } from 'svelte';
  
  export let autoGet = true; // 自動的に位置情報を取得するかどうか
  
  const dispatch = createEventDispatcher();
  
  // 位置情報を取得する関数
  const getLocation = () => {
    if (!navigator.geolocation) {
      dispatch('error', { message: "このブラウザでは位置情報がサポートされていません。" });
      return;
    }
    
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const locationData = {
          latitude: position.coords.latitude,
          longitude: position.coords.longitude
        };
        dispatch('locationUpdate', locationData);
      },
      (err) => {
        let errorMsg = "位置情報の取得に失敗しました。";
        
        switch (err.code) {
          case 1: errorMsg = "位置情報の利用が許可されていません。"; break;
          case 2: errorMsg = "位置情報を取得できませんでした。"; break;
          case 3: errorMsg = "タイムアウトしました。"; break;
        }
        
        dispatch('error', { message: errorMsg });
      },
      { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
    );
  };
  
  onMount(() => {
    if (autoGet) {
      getLocation();
    }
  });
</script>

<svelte:options accessors={true} />

<slot getLocation={getLocation} />