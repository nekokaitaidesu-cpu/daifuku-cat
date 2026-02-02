import streamlit as st
import streamlit.components.v1 as components

# ページの設定
st.set_page_config(
    page_title="ふわふわペットルーム",
    page_icon="🍄",
    layout="centered"
)

st.title("My Fluffy Pet Room 🍄")
st.write("猫ちゃんを高いところから離すと、ふんわり落ちるっち！")

# HTML/CSS/JSを定義
html_code = """
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<style>
  body {
    height: 100vh;
    margin: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: transparent;
    font-family: sans-serif;
    overflow: hidden;
    user-select: none;
    -webkit-user-select: none;
  }

  /* --- お部屋のスタイル --- */
  .room-container {
    position: relative;
    width: 350px;  /* 部屋の幅 */
    height: 400px; /* 部屋の高さ */
    background-color: #fdfaf5; /* 壁紙の色 */
    border: 4px solid #d4c4b5; /* 枠の色 */
    border-bottom: 8px solid #bfab99; /* 床を少し厚く */
    border-radius: 12px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    overflow: hidden; /* 部屋からはみ出さないようにする */
  }

  /* --- 動かせるキャラクターの親要素 --- */
  #draggable-root {
    position: absolute;
    left: 125px; /* 初期位置X (部屋の中央付近) */
    top: 100px;  /* 初期位置Y */
    width: 100px;
    height: 130px; /* 影を含む全体の高さ */
    cursor: grab;
    touch-action: none;
    /* transitionは物理演算と干渉するので削除 */
  }

  #draggable-root.grabbing {
    cursor: grabbing;
  }

  /* つまんだ時に中の要素だけを縮小させる */
  #draggable-root.grabbing .cat-wrapper,
  #draggable-root.grabbing .shadow {
    transform: scale(0.9) !important; /* CSSアニメーションを一時的に上書き */
    transition: transform 0.1s;
  }

  /* --- 以下、猫のアニメーションCSS --- */
  .cat-wrapper {
    position: relative;
    width: 100px;
    height: 100px;
    margin: 0 auto;
    animation: bounce-float 2s infinite ease-in-out;
    pointer-events: none;
  }

  .cat-body {
    width: 100%;
    height: 100%;
    background-color: #b0b0b0;
    border-radius: 50% 50% 45% 45%;
    position: relative;
    z-index: 2;
  }

  .cat-ear {
    position: absolute;
    top: -10px;
    width: 0;
    height: 0;
    border-left: 20px solid transparent;
    border-right: 20px solid transparent;
    border-bottom: 40px solid #b0b0b0;
    z-index: 1;
  }
  .ear-left { left: 5px; transform: rotate(-15deg); }
  .ear-right { right: 5px; transform: rotate(15deg); }

  .cat-face {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 3;
    width: 60px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .eye {
    width: 12px;
    height: 12px;
    background-color: white;
    border-radius: 50%;
  }

  .shadow {
    width: 80px;
    height: 10px;
    background-color: rgba(0,0,0,0.1);
    border-radius: 50%;
    margin: 10px auto 0; /* マージンを調整 */
    animation: shadow-scale 2s infinite ease-in-out;
    pointer-events: none;
  }

  /* 物理演算中はCSSアニメーションを止めるクラス（今回は使わないアプローチに変更） */
  /* .physics-active .cat-wrapper, .physics-active .shadow { animation: none !important; transform: scale(1) translateY(0) !important; } */

  @keyframes bounce-float {
    0%, 100% { transform: translateY(0) scale(1); }
    50% { transform: translateY(-15px) scale(1.05, 0.95); }
  }

  @keyframes shadow-scale {
    0%, 100% { transform: scale(1); opacity: 0.3; }
    50% { transform: scale(0.8); opacity: 0.1; }
  }
</style>
</head>
<body>

  <div class="room-container">
    <div id="draggable-root">
      <div class="cat-wrapper">
        <div class="cat-ear ear-left"></div>
        <div class="cat-ear ear-right"></div>
        <div class="cat-body">
          <div class="cat-face">
            <div class="eye"></div>
            <div class="eye"></div>
          </div>
        </div>
      </div>
      <div class="shadow"></div>
    </div>
  </div>

<script>
  const draggable = document.getElementById('draggable-root');
  const room = document.querySelector('.room-container');
  
  // 物理演算パラメータ
  let posX = 125, posY = 100; // 初期位置
  let velocityX = 0, velocityY = 0; // 速度
  const gravity = 0.5; // 重力加速度（値が大きいほど速く落ちる）
  const friction = 0.92; // 空気抵抗（値が小さいほど「ふんわり」する）
  const bounce = -0.4; // 跳ね返り係数（マイナスの値。0に近いほど跳ねない）

  let isDragging = false;
  let dragStartX, dragStartY;
  let animationFrameId;

  // ループ処理を開始する関数
  function startPhysicsLoop() {
    if (!animationFrameId) {
      updatePhysics();
    }
  }

  // ループ処理を停止する関数
  function stopPhysicsLoop() {
    if (animationFrameId) {
      cancelAnimationFrame(animationFrameId);
      animationFrameId = null;
    }
  }

  // 物理演算のメインループ
  function updatePhysics() {
    if (!isDragging) {
      // 重力を加える
      velocityY += gravity;
      
      // 空気抵抗を加える（速度を減衰させる）
      velocityX *= friction;
      velocityY *= friction;

      // 速度を位置に加える
      posX += velocityX;
      posY += velocityY;

      // 部屋の境界値を取得
      const roomRect = room.getBoundingClientRect();
      const charRect = draggable.getBoundingClientRect();
      const maxX = roomRect.width - charRect.width;
      const maxY = roomRect.height - charRect.height;

      // --- 衝突判定 ---
      
      // 床との衝突
      if (posY > maxY) {
        posY = maxY; // 床の位置に戻す
        velocityY *= bounce; // 速度を反転して減衰させる（跳ね返り）
        
        // 速度が十分に小さくなったら止める（微振動防止）
        if (Math.abs(velocityY) < 1) velocityY = 0;
      }

      // 天井との衝突
      if (posY < 0) {
        posY = 0;
        velocityY *= bounce;
      }

      // 左壁との衝突
      if (posX < 0) {
        posX = 0;
        velocityX *= bounce;
      }

      // 右壁との衝突
      if (posX > maxX) {
        posX = maxX;
        velocityX *= bounce;
      }

      // 新しい位置を適用
      draggable.style.left = `${posX}px`;
      draggable.style.top = `${posY}px`;
    }

    // 次のフレームをリクエスト
    animationFrameId = requestAnimationFrame(updatePhysics);
  }


  // --- ドラッグ操作関連 ---

  function startDrag(e) {
    isDragging = true;
    draggable.classList.add('grabbing');
    
    // 物理演算の速度をリセット（掴んだ瞬間は静止）
    velocityX = 0;
    velocityY = 0;

    const clientX = e.touches ? e.touches[0].clientX : e.clientX;
    const clientY = e.touches ? e.touches[0].clientY : e.clientY;
    
    // クリックした位置と要素の左上との差分を記録
    const rect = draggable.getBoundingClientRect();
    dragStartX = clientX - rect.left;
    dragStartY = clientY - rect.top;
  }

  function drag(e) {
    if (!isDragging) return;
    e.preventDefault();

    const clientX = e.touches ? e.touches[0].clientX : e.clientX;
    const clientY = e.touches ? e.touches[0].clientY : e.clientY;

    // 親要素（部屋）からの相対座標を計算
    const roomRect = room.getBoundingClientRect();
    posX = clientX - roomRect.left - dragStartX;
    posY = clientY - roomRect.top - dragStartY;

    // ドラッグ中も位置を即時反映
    draggable.style.left = `${posX}px`;
    draggable.style.top = `${posY}px`;
  }

  function endDrag() {
    isDragging = false;
    draggable.classList.remove('grabbing');
    // 手を離した瞬間から物理演算が再開される
  }

  // イベントリスナー登録
  draggable.addEventListener('mousedown', startDrag);
  window.addEventListener('mousemove', drag);
  window.addEventListener('mouseup', endDrag);

  draggable.addEventListener('touchstart', startDrag, {passive: false});
  window.addEventListener('touchmove', drag, {passive: false});
  window.addEventListener('touchend', endDrag);

  // ページ読み込み時に物理演算ループを開始
  startPhysicsLoop();

</script>

</body>
</html>
"""

components.html(html_code, height=550)
