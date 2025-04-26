<!-- ルート生成中に表示する画面 -->
<div class="loading-screen">
    <div class="spinner"></div>
    <p>ルートを生成中...</p>
  </div>
  
  <style>
    .loading-screen {
      position: fixed;
      top: 0;
      left: 0;
      z-index: 9999;
      width: 100vw;
      height: 100vh;
      background: rgba(0, 13, 65, 0.9);
      color: white;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      font-size: 1.2rem;
    }
  
    .spinner {
      border: 4px solid rgba(255, 255, 255, 0.2);
      border-top: 4px solid #FEA900;
      border-radius: 50%;
      width: 48px;
      height: 48px;
      animation: spin 1s linear infinite;
      margin-bottom: 1rem;
    }
  
    @keyframes spin {
      to {
        transform: rotate(360deg);
      }
    }
  </style>
  