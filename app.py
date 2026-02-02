import streamlit as st
import streamlit.components.v1 as components

# ページの設定
st.set_page_config(
    page_title="大福キャットのお部屋",
    page_icon="🍄",
    layout="centered"
)

st.title("Daifuku Cat Room v4 🍄")
st.write("足場ができたっち！ジャンプして乗れるかな？")

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

  /* --- 新しい要素：足場 --- */
  .platform {
    position: absolute;
    height: 12px;
    background-color: #e8d3b9; /* 木のような色 */
    border: 2px solid #d4c4b5;
    border-radius: 4px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  }
  /* 左下の足場 */
  .platform-1 {
    width: 100px;
    left: 20px;
    top: 280px;
  }
  /* 右上の足場 */
  .platform-2 {
    width: 120px;
    right: 30px;
    top: 150px;
  }

  /* --- キャラクター関連（変更なし） --- */
  #draggable-root {
    position: absolute;
    left: 130px;
    top: 150px;
    width: 90px;
    height: 80px;
    cursor: grab;
    touch-action: none;
    z-index: 10; /* 足場より前に表示 */
  }
  #draggable-root.grabbing { cursor: grabbing; }
  #draggable-root.grabbing .cat-wrapper { transform: scale(0.9) !important; transition: transform 0.1s; }

  .cat-wrapper {
    position: relative;
    width: 90px; height: 60px;
    margin: 0 auto;
    transform-origin: bottom center;
    transition: transform 0.2s ease-out;
  }
  .boing-effect { animation: slime-bounce 0.4s ease-out; }
  @keyframes slime-bounce {
    0% { transform: scale(1, 1); } 30% { transform: scale(1.3, 0.7); }
    50% { transform: scale(0.8, 1.2); } 70% { transform: scale(1.1, 0.9); } 100% { transform: scale(1, 1); }
  }
  .walking-left .cat-wrapper { transform: rotate(-5deg); }
  .walking-right .cat-wrapper { transform: rotate(5deg); }
  .cat-body {
    width: 100%; height: 100%; background-color: #b0b0b0;
    border-radius: 50% 50% 40% 40% / 60% 60% 40% 40%; position: relative; z-index: 2;
  }
  .cat-ear {
    position: absolute; top: -4px; width: 0; height: 0;
    border-left: 10px solid transparent; border-right: 10px solid transparent;
    border-bottom: 20px solid #b0b0b0; z-index: 1;
  }
  .ear-left { left: 10px; transform: rotate(-25deg); }
  .ear-right { right: 10px; transform: rotate(25deg); }
  .cat-tail {
    position: absolute; bottom: 4px; right: -4px; width: 15px; height: 15px;
    background-color: #b0b0b0; border-radius: 50%; z-index: 1; transition: all 0.2s ease-out;
  }
  .walking-right .cat-tail { right: auto; left: -4px; }
  .cat-face {
    position: absolute; top: 58%; left: 50%; transform: translate(-50%, -50%);
    z-index: 3; width: 36px; display: flex; justify-content: space-between; align-items: center;
    transition: transform 0.2s ease-out;
  }
  .face-left { transform: translate(calc(-50% - 5px), -50%); }
  .face-right { transform: translate(calc(-50% + 5px), -50%); }
  .eye { width: 8px; height: 8px; background-color: white; border-radius: 50%; }
  .shadow {
    width: 80px; height: 8px; background-color: rgba(0,0,0,0.1);
    border-radius: 50%; margin: 4px auto 0; pointer-events: none;
  }
</style>
</head>
<body>

  <div class="room-container">
    <div class="platform platform-1"></div>
    <div class="platform platform-2"></div>

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
  // 足場の要素を取得
  const platforms = document.querySelectorAll('.platform');
  
  let posX = 130, posY = 150;
  let velocityX = 0, velocityY = 0;
  const gravity = 0.6;
  const friction = 0.92;
  const bounce = -0.3;

  let isDragging = false;
  let dragStartX, dragStartY;
  
  let idleTimer = 0;
  let isGrounded = false;
  // 現在乗っている地面の高さ（初期値は床）
  let groundLevel = 0;

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
      const roomFloorY = roomRect.height - charRect.height;
      const roomCeilingY = 0;
      const roomLeftX = 0;
      const roomRightX = roomRect.width - charRect.width;

      // --- 当たり判定開始 ---
      
      // 1. まずは床を基準にする
      groundLevel = roomFloorY;
      let hasLanded = false;

      // 2. 足場との当たり判定
      // 落下中(velocityY >= 0)のみ判定する
      if (velocityY >= 0) {
        platforms.forEach(platform => {
          const platRect = platform.getBoundingClientRect();
          // 部屋の左上を原点とした相対座標に変換
          const platLeft = platRect.left - roomRect.left;
          const platRight = platRect.right - roomRect.left;
          const platTop = platRect.top - roomRect.top;
          
          // キャラクターの足元の位置
          const charFootX = posX + charRect.width / 2;
          const charFootY = posY + charRect.height;

          // 足場の上面の高さ（キャラの原点基準）
          const platSurfaceY = platTop - charRect.height;

          // 判定：横方向が範囲内 かつ 縦方向が足場表面を通過したか
          // (前回の位置が足場より上で、今回の位置が足場より下または同じ)
          const prevPosY = posY - velocityY;
          if (
            charFootX > platLeft && charFootX < platRight && // 横の判定
            prevPosY <= platSurfaceY && posY >= platSurfaceY // 縦の判定
          ) {
            groundLevel = platSurfaceY;
            hasLanded = true;
          }
        });
      }

      // 3. 床または足場への着地処理
      if (posY > groundLevel) {
        const impactSpeed = velocityY;
        posY = groundLevel;
        
        // 跳ね返り（足場の上では少し弱くしてみる）
        velocityY *= bounce;
        if (hasLanded) velocityY *= 0.5; // 足場ならさらに減衰

        if (Math.abs(velocityY) < 1) velocityY = 0;
        
        // 激しい着地なら「ぽよん」
        if (impactSpeed > 5) triggerBounceAnimation();
        
        isGrounded = true;
      } else if (posY < groundLevel && velocityY > 0) {
        // 地面より上にいて落下中＝空中
        isGrounded = false;
      } else if (posY === groundLevel) {
         // 完全に地面にいる
         isGrounded = true;
      }


      // 天井・壁判定
      if (posY < roomCeilingY) { posY = roomCeilingY; velocityY *= bounce; }
      if (posX < roomLeftX) { posX = roomLeftX; velocityX *= bounce; }
      if (posX > roomRightX) { posX = roomRightX; velocityX *= bounce; }

      // 自動行動
      if (isGrounded && Math.abs(velocityX) < 0.5 && Math.abs(velocityY) < 0.5 && !isDragging) {
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
      // 行動の選択肢を増やす
      const action = Math.floor(Math.random() * 6); 
      switch(action) {
        case 0: // 左移動
          velocityX = -3; break;
        case 1: // 右移動
          velocityX = 3; break;
        case 2: // 小ジャンプ（その場）
          velocityY = -5; break;
        case 3: // 中ジャンプ（左右どちらかへ）
          velocityX = (Math.random() > 0.5 ? 4 : -4);
          velocityY = -8;
          break;
        case 4: // 大ジャンプ（高いところを目指す！）
          velocityX = (Math.random() > 0.5 ? 5 : -5);
          velocityY = -12;
          break;
        case 5: // 休憩
          break;
      }
      // 次の行動までの時間を少し長めにランダム設定
      idleTimer = 100 + Math.random() * 200;
    }
  }

  function updateDirection() {
    catFace.classList.remove('face-left', 'face-right');
    draggable.classList.remove('walking-left', 'walking-right');
    if (Math.abs(velocityX) > 0.5) {
      if (velocityX > 0) {
        catFace.classList.add('face-right');
        draggable.classList.add('walking-right');
      } else {
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
