import streamlit as st
import streamlit.components.v1 as components

# ページの設定
st.set_page_config(
    page_title="ふわふわペットルーム",
    page_icon="🍄",
    layout="centered"
)

st.title("My Fluffy Pet Room v2 🍄")
st.write("普段は大人しいけど、落とすと「ぽよん」ってなるっち！")

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

  .room-container {
    position: relative;
    width: 350px;
    height: 400px;
    background-color: #fdfaf5;
    border: 4px solid #d4c4b5;
    border-bottom: 8px solid #bfab99;
    border-radius: 12px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    overflow: hidden;
  }

  #draggable-root {
    position: absolute;
    left: 125px;
    top: 100px;
    width: 100px;
    height: 130px;
    cursor: grab;
    touch-action: none;
  }

  #draggable-root.grabbing {
    cursor: grabbing;
  }

  /* つまんだ時は少し縮こまる（継続） */
  #draggable-root.grabbing .cat-wrapper {
    transform: scale(0.9) !important;
    transition: transform 0.1s;
  }

  /* --- 猫のスタイル --- */
  .cat-wrapper {
    position: relative;
    width: 100px;
    height: 100px;
    margin: 0 auto;
    /* 常時のぽよぽよアニメーションは削除したっち！ */
    /* animation: bounce-float ...;  <-- 削除 */
    transform-origin: bottom center; /* 下を中心に変形させる */
  }

  /* ★ここがポイント！着地した瞬間のスライムアニメーション ★ */
  .boing-effect {
    animation: slime-bounce 0.4s ease-out;
  }

  @keyframes slime-bounce {
    0% { transform: scale(1, 1); }
    30% { transform: scale(1.25, 0.75); } /* 横に潰れる（むぎゅっ） */
    50% { transform: scale(0.85, 1.15); } /* 縦に伸びる（びよん） */
    70% { transform: scale(1.05, 0.95); } /* 少し揺り戻し */
    100% { transform: scale(1, 1); }      /* 元に戻る */
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
    margin: 10px auto 0;
    /* 影のアニメーションも停止 */
    pointer-events: none;
  }

</style>
</head>
<body>

  <div class="room-container">
    <div id="draggable-root">
      <div class="cat-wrapper" id="cat-visual">
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
  const catVisual = document.getElementById('cat-visual'); // アニメーションさせる対象
  const room = document.querySelector('.room-container');
  
  let posX = 125, posY = 100;
  let velocityX = 0, velocityY = 0;
  const gravity = 0.6;   // 重力を少し強めに
  const friction = 0.92;
  const bounce = -0.3;   // 跳ね返りは少し弱めに（スライム感を出すため）

  let isDragging = false;
  let dragStartX, dragStartY;
  let animationFrameId;

  function startPhysicsLoop() {
    if (!animationFrameId) updatePhysics();
  }

  function updatePhysics() {
    if (!isDragging) {
      velocityY += gravity;
      velocityX *= friction;
      velocityY *= friction;

      posX += velocityX;
      posY += velocityY;

      const roomRect = room.getBoundingClientRect();
      const charRect = draggable.getBoundingClientRect();
      const maxX = roomRect.width - charRect.width;
      const maxY = roomRect.height - charRect.height;

      // --- 床との衝突判定 ---
      if (posY > maxY) {
        const impactSpeed = velocityY; // 衝突時の速度を記録
        
        posY = maxY;
        velocityY *= bounce; 
        
        if (Math.abs(velocityY) < 1) velocityY = 0;

        // ★ここでアニメーション発動判定★
        // ある程度の勢い(speed > 5)で落ちたときだけ「ぽよん」とさせる
        if (impactSpeed > 5) {
          triggerBounceAnimation();
        }
      }

      // 天井
      if (posY < 0) {
        posY = 0;
        velocityY *= bounce;
      }
      // 壁
      if (posX < 0) {
        posX = 0;
        velocityX *= bounce;
      }
      if (posX > maxX) {
        posX = maxX;
        velocityX *= bounce;
      }

      draggable.style.left = `${posX}px`;
      draggable.style.top = `${posY}px`;
    }
    animationFrameId = requestAnimationFrame(updatePhysics);
  }

  // 「ぽよん」アニメーションを発動させる関数
  function triggerBounceAnimation() {
    // クラスを一旦外して、リフロー（強制再描画）させてからまたつける
    catVisual.classList.remove('boing-effect');
    void catVisual.offsetWidth; // これが魔法の呪文（リセット）だっち
    catVisual.classList.add('boing-effect');
  }

  function startDrag(e) {
    isDragging = true;
    draggable.classList.add('grabbing');
    catVisual.classList.remove('boing-effect'); // 掴んだらアニメーション停止
    
    velocityX = 0;
    velocityY = 0;

    const clientX = e.touches ? e.touches[0].clientX : e.clientX;
    const clientY = e.touches ? e.touches[0].clientY : e.clientY;
    
    const rect = draggable.getBoundingClientRect();
    dragStartX = clientX - rect.left;
    dragStartY = clientY - rect.top;
  }

  function drag(e) {
    if (!isDragging) return;
    e.preventDefault();

    const clientX = e.touches ? e.touches[0].clientX : e.clientX;
    const clientY = e.touches ? e.touches[0].clientY : e.clientY;

    const roomRect = room.getBoundingClientRect();
    posX = clientX - roomRect.left - dragStartX;
    posY = clientY - roomRect.top - dragStartY;

    draggable.style.left = `${posX}px`;
    draggable.style.top = `${posY}px`;
  }

  function endDrag() {
    isDragging = false;
    draggable.classList.remove('grabbing');
  }

  draggable.addEventListener('mousedown', startDrag);
  window.addEventListener('mousemove', drag);
  window.addEventListener('mouseup', endDrag);

  draggable.addEventListener('touchstart', startDrag, {passive: false});
  window.addEventListener('touchmove', drag, {passive: false});
  window.addEventListener('touchend', endDrag);

  startPhysicsLoop();

</script>

</body>
</html>
"""

components.html(html_code, height=550)
