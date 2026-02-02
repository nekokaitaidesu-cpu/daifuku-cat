import streamlit as st
import streamlit.components.v1 as components

# ページの設定
st.set_page_config(
    page_title="大福キャットのお部屋",
    page_icon="🍄",
    layout="centered"
)

st.title("Daifuku Cat Room 🍄")
st.write("大福みたいにモチモチな猫ちゃんだっち！")

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
    left: 115px; /* サイズ変更に合わせて調整 */
    top: 100px;
    width: 120px; /* 大福なので少し横長に */
    height: 100px; /* 影込みの高さ */
    cursor: grab;
    touch-action: none;
  }

  #draggable-root.grabbing {
    cursor: grabbing;
  }

  /* つまんだ時は少し縮こまる */
  #draggable-root.grabbing .cat-wrapper {
    transform: scale(0.9) !important;
    transition: transform 0.1s;
  }

  /* --- 大福キャットのデザイン --- */
  .cat-wrapper {
    position: relative;
    width: 120px; /* 横幅を広げたっち */
    height: 80px; /* 高さを低くして「潰れ感」を出したっち */
    margin: 0 auto;
    transform-origin: bottom center;
    transition: transform 0.2s ease-out;
  }

  /* 着地した瞬間のぷるんとした動き */
  .boing-effect {
    animation: slime-bounce 0.4s ease-out;
  }

  @keyframes slime-bounce {
    0% { transform: scale(1, 1); }
    30% { transform: scale(1.3, 0.7); }  /* より平べったく */
    50% { transform: scale(0.8, 1.2); }
    70% { transform: scale(1.1, 0.9); }
    100% { transform: scale(1, 1); }
  }

  /* 歩くときのアニメーション */
  .walking-left .cat-wrapper { transform: rotate(-5deg); }
  .walking-right .cat-wrapper { transform: rotate(5deg); }

  /* 体（大福部分） */
  .cat-body {
    width: 100%;
    height: 100%;
    background-color: #b0b0b0; /* 指定のグレー */
    /* 上を丸く、下を少し平らにして「地面に置いてある感」を出す */
    border-radius: 50% 50% 40% 40% / 60% 60% 40% 40%;
    position: relative;
    z-index: 2;
  }

  /* 耳（小さくちょこんと） */
  .cat-ear {
    position: absolute;
    top: -5px; /* 位置を下げる */
    width: 0;
    height: 0;
    border-left: 12px solid transparent;
    border-right: 12px solid transparent;
    border-bottom: 25px solid #b0b0b0;
    z-index: 1;
  }
  .ear-left { left: 15px; transform: rotate(-25deg); }
  .ear-right { right: 15px; transform: rotate(25deg); }

  /* しっぽ（お尻に丸いのをつける） */
  .cat-tail {
    position: absolute;
    bottom: 5px;
    right: -5px;
    width: 20px;
    height: 20px;
    background-color: #b0b0b0;
    border-radius: 50%;
    z-index: 1;
  }

  /* 顔（少し下に配置して赤ちゃん顔に） */
  .cat-face {
    position: absolute;
    top: 60%; /* 顔の位置を下げる */
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 3;
    width: 50px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .eye {
    width: 10px;
    height: 10px;
    background-color: white;
    border-radius: 50%;
  }

  /* 影（大福の形に合わせて横長に） */
  .shadow {
    width: 100px;
    height: 12px;
    background-color: rgba(0,0,0,0.1);
    border-radius: 50%;
    margin: 5px auto 0;
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
        <div class="cat-tail"></div>
      </div>
      <div class="shadow"></div>
    </div>
  </div>

<script>
  const draggable = document.getElementById('draggable-root');
  const catVisual = document.getElementById('cat-visual');
  const room = document.querySelector('.room-container');
  
  // 物理演算変数
  let posX = 115, posY = 100;
  let velocityX = 0, velocityY = 0;
  const gravity = 0.6;
  const friction = 0.92;
  const bounce = -0.3;

  let isDragging = false;
  let dragStartX, dragStartY;
  
  let idleTimer = 0;
  let isGrounded = false;

  function startPhysicsLoop() {
    requestAnimationFrame(updatePhysics);
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

      // 床判定
      if (posY > maxY) {
        const impactSpeed = velocityY;
        posY = maxY;
        velocityY *= bounce;

        if (Math.abs(velocityY) < 1) velocityY = 0;
        
        // ぽよん判定
        if (impactSpeed > 5) {
          triggerBounceAnimation();
        }

        isGrounded = true;
      } else {
        isGrounded = false;
      }

      // 壁・天井判定
      if (posY < 0) { posY = 0; velocityY *= bounce; }
      if (posX < 0) { posX = 0; velocityX *= bounce; }
      if (posX > maxX) { posX = maxX; velocityX *= bounce; }

      // 自動行動
      if (isGrounded && Math.abs(velocityX) < 0.5 && !isDragging) {
        handleIdleBehavior();
      }

      updateRotation();

      draggable.style.left = `${posX}px`;
      draggable.style.top = `${posY}px`;
    }

    requestAnimationFrame(updatePhysics);
  }

  function handleIdleBehavior() {
    idleTimer--;
    if (idleTimer < 0) {
      const action = Math.floor(Math.random() * 4);
      switch(action) {
        case 0: // 左
          velocityX = -3;
          if(Math.random() > 0.5) velocityY = -3; // ジャンプは低めに
          break;
        case 1: // 右
          velocityX = 3;
          if(Math.random() > 0.5) velocityY = -3;
          break;
        case 2: // ジャンプ
          velocityY = -5;
          break;
        case 3: // 休憩
          break;
      }
      idleTimer = 60 + Math.random() * 120;
    }
  }

  function updateRotation() {
    if (Math.abs(velocityX) > 1) {
      if (velocityX > 0) {
        draggable.classList.add('walking-right');
        draggable.classList.remove('walking-left');
      } else {
        draggable.classList.add('walking-left');
        draggable.classList.remove('walking-right');
      }
    } else {
      draggable.classList.remove('walking-right');
      draggable.classList.remove('walking-left');
    }
  }

  function triggerBounceAnimation() {
    catVisual.classList.remove('boing-effect');
    void catVisual.offsetWidth;
    catVisual.classList.add('boing-effect');
  }

  function startDrag(e) {
    isDragging = true;
    draggable.classList.add('grabbing');
    catVisual.classList.remove('boing-effect'); 
    
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
    idleTimer = 60; 
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
