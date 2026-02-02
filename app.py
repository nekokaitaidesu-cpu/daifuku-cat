import streamlit as st
import streamlit.components.v1 as components

# ページの設定
st.set_page_config(
    page_title="ふわふわペットルーム",
    page_icon="🍄",
    layout="centered"
)

st.title("My Fluffy Pet Room v3 🍄")
st.write("触らないでいると、勝手にふわふわ動き回るっち！")

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
    height: 130px; /* 影込みの高さ */
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

  /* --- 猫のスタイル --- */
  .cat-wrapper {
    position: relative;
    width: 100px;
    height: 100px;
    margin: 0 auto;
    transform-origin: bottom center;
    transition: transform 0.2s ease-out; /* 動きを少し滑らかに */
  }

  /* 着地した瞬間のスライムアニメーション */
  .boing-effect {
    animation: slime-bounce 0.4s ease-out;
  }

  @keyframes slime-bounce {
    0% { transform: scale(1, 1); }
    30% { transform: scale(1.25, 0.75); }
    50% { transform: scale(0.85, 1.15); }
    70% { transform: scale(1.05, 0.95); }
    100% { transform: scale(1, 1); }
  }

  /* 左右移動するときに少し体を傾けるクラス */
  .walking-left .cat-wrapper { transform: rotate(-5deg); }
  .walking-right .cat-wrapper { transform: rotate(5deg); }

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
  const catVisual = document.getElementById('cat-visual');
  const room = document.querySelector('.room-container');
  
  // 物理演算変数
  let posX = 125, posY = 100;
  let velocityX = 0, velocityY = 0;
  const gravity = 0.6;
  const friction = 0.92;
  const bounce = -0.3;

  // 状態管理
  let isDragging = false;
  let dragStartX, dragStartY;
  
  // 自動行動用の変数
  let idleTimer = 0;      // 次の行動までのカウントダウン
  let isGrounded = false; // 床に着いているか

  function startPhysicsLoop() {
    requestAnimationFrame(updatePhysics);
  }

  function updatePhysics() {
    if (!isDragging) {
      // 1. 重力と摩擦
      velocityY += gravity;
      velocityX *= friction;
      velocityY *= friction;

      posX += velocityX;
      posY += velocityY;

      // 2. 境界判定（壁・床・天井）
      const roomRect = room.getBoundingClientRect();
      const charRect = draggable.getBoundingClientRect();
      const maxX = roomRect.width - charRect.width;
      const maxY = roomRect.height - charRect.height;

      // 床判定
      if (posY > maxY) {
        const impactSpeed = velocityY;
        posY = maxY;
        velocityY *= bounce;

        // ほぼ止まったら完全に止める
        if (Math.abs(velocityY) < 1) velocityY = 0;
        
        // 激しく落ちたら「ぽよん」
        if (impactSpeed > 5) {
          triggerBounceAnimation();
        }

        isGrounded = true; // 床にいるフラグON
      } else {
        isGrounded = false; // 空中にいるフラグOFF
      }

      // 天井
      if (posY < 0) { posY = 0; velocityY *= bounce; }
      // 左壁
      if (posX < 0) { posX = 0; velocityX *= bounce; }
      // 右壁
      if (posX > maxX) { posX = maxX; velocityX *= bounce; }

      // 3. 自動行動（暇なときシステム）
      // 床にいて、静止していて、ドラッグされていない時
      if (isGrounded && Math.abs(velocityX) < 0.5 && !isDragging) {
        handleIdleBehavior();
      }

      // 4. 見た目の更新（移動方向によって傾ける）
      updateRotation();

      // 位置適用
      draggable.style.left = `${posX}px`;
      draggable.style.top = `${posY}px`;
    }

    requestAnimationFrame(updatePhysics);
  }

  // --- 気まぐれ自動行動システム ---
  function handleIdleBehavior() {
    idleTimer--;

    if (idleTimer < 0) {
      // 次の行動をランダムに決める (0〜3の乱数)
      const action = Math.floor(Math.random() * 4);
      
      // 行動リスト
      switch(action) {
        case 0: // 左へ移動
          velocityX = -3;
          // たまに小ジャンプも混ぜる
          if(Math.random() > 0.5) velocityY = -4; 
          break;
        case 1: // 右へ移動
          velocityX = 3;
          if(Math.random() > 0.5) velocityY = -4;
          break;
        case 2: // その場で小ジャンプ（ふわっ）
          velocityY = -6;
          break;
        case 3: // 何もしない（長めの休憩）
          // 何もしない
          break;
      }

      // 次の行動までの待機時間をセット（60フレーム〜180フレーム = 1〜3秒）
      idleTimer = 60 + Math.random() * 120;
    }
  }

  // 移動方向に合わせて少し体を傾ける演出
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

  // 「ぽよん」アニメーション
  function triggerBounceAnimation() {
    catVisual.classList.remove('boing-effect');
    void catVisual.offsetWidth;
    catVisual.classList.add('boing-effect');
  }

  // --- ドラッグ操作 ---
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
    // 放した瞬間に次の行動タイマーをリセット（すぐには動かない）
    idleTimer = 60; 
  }

  // イベントリスナー
  draggable.addEventListener('mousedown', startDrag);
  window.addEventListener('mousemove', drag);
  window.addEventListener('mouseup', endDrag);
  draggable.addEventListener('touchstart', startDrag, {passive: false});
  window.addEventListener('touchmove', drag, {passive: false});
  window.addEventListener('touchend', endDrag);

  // 開始
  startPhysicsLoop();

</script>

</body>
</html>
"""

components.html(html_code, height=550)
