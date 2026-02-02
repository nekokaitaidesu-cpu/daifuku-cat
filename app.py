import streamlit as st
import streamlit.components.v1 as components

# ページの設定
st.set_page_config(
    page_title="大福キャットのお部屋",
    page_icon="🍄",
    layout="centered"
)

st.title("Daifuku Cat Room v3 🍄")
st.write("右に向くとき、しっぽの位置も変わるようになったっち！")

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
    left: 130px;
    top: 150px;
    width: 90px;
    height: 80px;
    cursor: grab;
    touch-action: none;
  }

  #draggable-root.grabbing {
    cursor: grabbing;
  }

  #draggable-root.grabbing .cat-wrapper {
    transform: scale(0.9) !important;
    transition: transform 0.1s;
  }

  /* --- 大福キャット --- */
  .cat-wrapper {
    position: relative;
    width: 90px;
    height: 60px;
    margin: 0 auto;
    transform-origin: bottom center;
    transition: transform 0.2s ease-out;
  }

  /* 着地アニメーション */
  .boing-effect { animation: slime-bounce 0.4s ease-out; }
  @keyframes slime-bounce {
    0% { transform: scale(1, 1); }
    30% { transform: scale(1.3, 0.7); }
    50% { transform: scale(0.8, 1.2); }
    70% { transform: scale(1.1, 0.9); }
    100% { transform: scale(1, 1); }
  }

  /* 移動時の体の傾き */
  .walking-left .cat-wrapper { transform: rotate(-5deg); }
  .walking-right .cat-wrapper { transform: rotate(5deg); }

  /* 体 */
  .cat-body {
    width: 100%;
    height: 100%;
    background-color: #b0b0b0;
    border-radius: 50% 50% 40% 40% / 60% 60% 40% 40%;
    position: relative;
    z-index: 2;
  }

  /* 耳 */
  .cat-ear {
    position: absolute;
    top: -4px;
    width: 0;
    height: 0;
    border-left: 10px solid transparent;
    border-right: 10px solid transparent;
    border-bottom: 20px solid #b0b0b0;
    z-index: 1;
  }
  .ear-left { left: 10px; transform: rotate(-25deg); }
  .ear-right { right: 10px; transform: rotate(25deg); }

  /* しっぽ（基本は右側） */
  .cat-tail {
    position: absolute;
    bottom: 4px;
    right: -4px; /* デフォルトは右 */
    width: 15px;
    height: 15px;
    background-color: #b0b0b0;
    border-radius: 50%;
    z-index: 1;
    transition: all 0.2s ease-out; /* しっぽの移動も滑らかに */
  }

  /* ★ここが追加ポイント！右移動中はしっぽを左にする★ */
  .walking-right .cat-tail {
    right: auto;
    left: -4px;
  }

  /* 顔 */
  .cat-face {
    position: absolute;
    top: 58%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 3;
    width: 36px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: transform 0.2s ease-out;
  }

  .face-left { transform: translate(calc(-50% - 5px), -50%); }
  .face-right { transform: translate(calc(-50% + 5px), -50%); }

  .eye {
    width: 8px;
    height: 8px;
    background-color: white;
    border-radius: 50%;
  }

  .shadow {
    width: 80px;
    height: 8px;
    background-color: rgba(0,0,0,0.1);
    border-radius: 50%;
    margin: 4px auto 0;
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
          <div class="cat-face" id="cat-face">
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
  const catFace = document.getElementById('cat-face');
  const room = document.querySelector('.room-container');
  
  let posX = 130, posY = 150;
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

      if (posY > maxY) {
        const impactSpeed = velocityY;
        posY = maxY;
        velocityY *= bounce;
        if (Math.abs(velocityY) < 1) velocityY = 0;
        if (impactSpeed > 5) triggerBounceAnimation();
        isGrounded = true;
      } else {
        isGrounded = false;
      }

      if (posY < 0) { posY = 0; velocityY *= bounce; }
      if (posX < 0) { posX = 0; velocityX *= bounce; }
      if (posX > maxX) { posX = maxX; velocityX *= bounce; }

      if (isGrounded && Math.abs(velocityX) < 0.5 && !isDragging) {
        handleIdleBehavior();
      }

      updateDirection();

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
        case 0: velocityX = -3; if(Math.random()>0.5) velocityY = -3; break;
        case 1: velocityX = 3; if(Math.random()>0.5) velocityY = -3; break;
        case 2: velocityY = -5; break;
        case 3: break;
      }
      idleTimer = 60 + Math.random() * 120;
    }
  }

  function updateDirection() {
    catFace.classList.remove('face-left', 'face-right');
    draggable.classList.remove('walking-left', 'walking-right');

    if (Math.abs(velocityX) > 0.5) {
      if (velocityX > 0) {
        // 右へ移動中
        catFace.classList.add('face-right');
        draggable.classList.add('walking-right');
      } else {
        // 左へ移動中
        catFace.classList.add('face-left');
        draggable.classList.add('walking-left');
      }
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
    velocityX = 0; velocityY = 0;
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
