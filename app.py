import streamlit as st
import streamlit.components.v1 as components

# ページの設定
st.set_page_config(
    page_title="大福キャットのアスレチック",
    page_icon="🍄",
    layout="centered"
)

st.title("Daifuku Athletic Room v2 🍄")
st.write("今度こそ！華麗にジャンプして足場に乗るっち！")

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
    height: 450px;
    background-color: #fdfaf5;
    border: 4px solid #d4c4b5;
    border-bottom: 8px solid #bfab99;
    border-radius: 12px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    overflow: hidden;
  }

  .draggable {
    cursor: grab;
    touch-action: none;
    position: absolute;
  }
  .draggable.grabbing {
    cursor: grabbing;
    z-index: 100;
  }

  /* --- 猫 --- */
  #cat-root {
    left: 130px;
    top: 300px;
    width: 90px;
    height: 80px;
    z-index: 10;
  }

  #cat-root.grabbing .cat-wrapper {
    transform: scale(0.9);
    transition: transform 0.1s;
  }

  .cat-wrapper {
    position: relative;
    width: 90px;
    height: 60px;
    margin: 0 auto;
    transform-origin: bottom center;
    transition: transform 0.2s ease-out;
  }

  .boing-effect { animation: slime-bounce 0.4s ease-out; }
  @keyframes slime-bounce {
    0% { transform: scale(1, 1); }
    30% { transform: scale(1.3, 0.7); }
    50% { transform: scale(0.8, 1.2); }
    70% { transform: scale(1.1, 0.9); }
    100% { transform: scale(1, 1); }
  }

  .walking-left .cat-wrapper { transform: rotate(-5deg); }
  .walking-right .cat-wrapper { transform: rotate(5deg); }

  .cat-body {
    width: 100%;
    height: 100%;
    background-color: #b0b0b0;
    border-radius: 50% 50% 40% 40% / 60% 60% 40% 40%;
    position: relative;
    z-index: 2;
  }

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

  .cat-tail {
    position: absolute;
    bottom: 4px;
    right: -4px;
    width: 15px;
    height: 15px;
    background-color: #b0b0b0;
    border-radius: 50%;
    z-index: 1;
    transition: all 0.2s ease-out;
  }
  .walking-right .cat-tail { right: auto; left: -4px; }

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

  .eye { width: 8px; height: 8px; background-color: white; border-radius: 50%; }
  
  .shadow {
    width: 80px;
    height: 8px;
    background-color: rgba(0,0,0,0.1);
    border-radius: 50%;
    margin: 4px auto 0;
    pointer-events: none;
  }

  /* --- 足場 --- */
  .platform {
    height: 12px;
    background-color: #e6c68b;
    border: 2px solid #bfa068;
    border-radius: 6px;
    box-shadow: 0 4px 0 rgba(0,0,0,0.1);
    background-image: repeating-linear-gradient(
      45deg, transparent, transparent 10px, rgba(255,255,255,0.2) 10px, rgba(255,255,255,0.2) 20px
    );
  }

</style>
</head>
<body>

  <div class="room-container">
    <div class="platform draggable" id="plat-1" style="width: 100px; left: 20px; top: 250px;"></div>
    <div class="platform draggable" id="plat-2" style="width: 100px; left: 220px; top: 150px;"></div>

    <div id="cat-root" class="draggable">
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
  const catRoot = document.getElementById('cat-root');
  const catVisual = document.getElementById('cat-visual');
  const catFace = document.getElementById('cat-face');
  const room = document.querySelector('.room-container');
  const platforms = document.querySelectorAll('.platform');
  
  let posX = 130, posY = 300;
  let velocityX = 0, velocityY = 0;
  const gravity = 0.6;
  const friction = 0.92; 
  const bounce = -0.3;

  let isDragging = false;
  let activeDragEl = null;
  let dragStartX, dragStartY;
  let dragOffsetLeft, dragOffsetTop;

  let idleTimer = 60;
  let isGrounded = false;
  let currentPlatform = null;
  
  // ★重要：自動ジャンプ中は摩擦を無視するためのフラグ
  let isAutoJumping = false;

  function startPhysicsLoop() {
    requestAnimationFrame(updatePhysics);
  }

  function updatePhysics() {
    if (!isDragging || activeDragEl !== catRoot) {
      velocityY += gravity;

      // ★自動ジャンプ中（空中）は摩擦をかけない！これで狙った場所に届く！
      if (!isAutoJumping) {
        velocityX *= friction;
      }
      velocityY *= friction;

      posX += velocityX;
      posY += velocityY;

      const roomRect = room.getBoundingClientRect();
      
      const maxX = roomRect.width - 90;
      const maxY = roomRect.height - 80;

      let landedThisFrame = false;

      // --- 足場との衝突判定 ---
      // 落下中のみ判定
      if (velocityY >= 0) {
        platforms.forEach(plat => {
          const pLeft = parseFloat(plat.style.left);
          const pTop = parseFloat(plat.style.top);
          const pWidth = parseFloat(plat.style.width);

          const catFootX = posX + 45; // 中心
          const catFootY = posY + 60; // 足元

          // 足場の範囲内、かつ高さが合致
          if (catFootX >= pLeft && catFootX <= pLeft + pWidth) {
             if (catFootY >= pTop - 10 && catFootY <= pTop + 20) { // 判定を少し広げた
               posY = pTop - 60; // 完全に足場の上に乗せる
               velocityY = 0;
               velocityX = 0; // 着地したら滑らないように止める
               landedThisFrame = true;
               currentPlatform = plat;
               
               // ジャンプ成功！モード解除
               if (isAutoJumping) {
                 isAutoJumping = false;
                 triggerBounceAnimation(); // 着地ぽよん
               }
             }
          }
        });
      }

      // --- 床との衝突判定 ---
      if (!landedThisFrame && posY > maxY) {
        posY = maxY;
        velocityY = 0; // 床でも跳ねずにピタッと止める（大福感）
        velocityX = 0;
        landedThisFrame = true;
        currentPlatform = null; // 床なのでnull
        
        if (isAutoJumping) {
           isAutoJumping = false;
           triggerBounceAnimation();
        }
      }

      isGrounded = landedThisFrame;

      // 壁・天井
      if (posY < 0) { posY = 0; velocityY *= bounce; }
      if (posX < 0) { posX = 0; velocityX *= bounce; }
      if (posX > maxX) { posX = maxX; velocityX *= bounce; }

      // 自動行動AI (接地していて、かつ自動ジャンプ中でない時)
      if (isGrounded && !isDragging && !isAutoJumping) {
        handleIdleBehavior();
      }

      updateDirection();

      catRoot.style.left = `${posX}px`;
      catRoot.style.top = `${posY}px`;
    }

    requestAnimationFrame(updatePhysics);
  }

  function handleIdleBehavior() {
    idleTimer--;
    if (idleTimer < 0) {
      // 0:左, 1:右, 2:待機, 3:ジャンプ移動(高確率)
      const action = Math.floor(Math.random() * 5); 

      switch(action) {
        case 0: // 左
          velocityX = -3; 
          if(Math.random()>0.7) velocityY = -3;
          break;
        case 1: // 右
          velocityX = 3;
          if(Math.random()>0.7) velocityY = -3;
          break;
        case 2: // 休憩
          break;
        case 3: 
        case 4: // 特殊ジャンプ（足場⇔床）
          performSpecialJump();
          break;
      }
      idleTimer = 60 + Math.random() * 100;
    }
  }

  function performSpecialJump() {
    let targetX, targetY;
    const roomRect = room.getBoundingClientRect();
    const maxX = roomRect.width - 90;
    const maxY = roomRect.height - 80;

    // A. 今、足場に乗っている場合 -> 「床」または「別の足場」へ
    if (currentPlatform) {
       // 70%の確率で床へ降りる、30%で別の足場へ（もしあれば）
       if (Math.random() < 0.7 || platforms.length < 2) {
          // 床のランダムな位置へ
          targetX = Math.random() * maxX;
          targetY = maxY; // 床のY座標
       } else {
          // 別の足場を探す
          let otherPlats = [];
          platforms.forEach(p => { if(p !== currentPlatform) otherPlats.push(p); });
          const targetPlat = otherPlats[Math.floor(Math.random() * otherPlats.length)];
          const pLeft = parseFloat(targetPlat.style.left);
          const pWidth = parseFloat(targetPlat.style.width);
          const pTop = parseFloat(targetPlat.style.top);
          
          targetX = pLeft + pWidth / 2 - 45; // 足場中心
          targetY = pTop - 60; // 足場の上
       }
    } 
    // B. 今、床にいる場合 -> 「足場」へ
    else {
       // ランダムな足場を選ぶ
       const targetPlat = platforms[Math.floor(Math.random() * platforms.length)];
       const pLeft = parseFloat(targetPlat.style.left);
       const pWidth = parseFloat(targetPlat.style.width);
       const pTop = parseFloat(targetPlat.style.top);
       
       targetX = pLeft + pWidth / 2 - 45;
       targetY = pTop - 60;
    }

    // --- 放物線の計算（摩擦無視前提） ---
    // 頂点高さの設定（現在地と目的地より高い位置）
    const startY = posY;
    const peakHeight = Math.min(startY, targetY) - 80; // 少なくとも80px上に飛ぶ
    
    const h1 = startY - peakHeight; // 上昇距離
    const h2 = targetY - peakHeight; // 下降距離
    
    // 上昇時間 t1 = sqrt(2 * h1 / g)
    const t1 = Math.sqrt(2 * h1 / gravity);
    // 下降時間 t2 = sqrt(2 * h2 / g)
    const t2 = Math.sqrt(2 * h2 / gravity);
    
    const totalTime = t1 + t2;

    // 初速度計算
    const vY = -Math.sqrt(2 * gravity * h1); // 上向き初速
    const vX = (targetX - posX) / totalTime; // 水平速度

    // ジャンプ実行！
    velocityY = vY;
    velocityX = vX;
    isAutoJumping = true; // ★摩擦無効モードON
    
    triggerBounceAnimation(); // 勢いよく
  }

  function updateDirection() {
    catFace.classList.remove('face-left', 'face-right');
    catRoot.classList.remove('walking-left', 'walking-right');
    if (Math.abs(velocityX) > 0.5) {
      if (velocityX > 0) {
        catFace.classList.add('face-right');
        catRoot.classList.add('walking-right');
      } else {
        catFace.classList.add('face-left');
        catRoot.classList.add('walking-left');
      }
    }
  }

  function triggerBounceAnimation() {
    catVisual.classList.remove('boing-effect');
    void catVisual.offsetWidth;
    catVisual.classList.add('boing-effect');
  }

  function startDrag(e) {
    const target = e.target.closest('.draggable');
    if (!target) return;
    isDragging = true;
    activeDragEl = target;
    activeDragEl.classList.add('grabbing');
    
    if (activeDragEl === catRoot) {
      catVisual.classList.remove('boing-effect'); 
      velocityX = 0; velocityY = 0;
      currentPlatform = null;
      isAutoJumping = false; // ドラッグしたら自動モード解除
    }

    const clientX = e.touches ? e.touches[0].clientX : e.clientX;
    const clientY = e.touches ? e.touches[0].clientY : e.clientY;
    const roomRect = room.getBoundingClientRect();
    const elemRect = activeDragEl.getBoundingClientRect();

    dragOffsetLeft = clientX - elemRect.left;
    dragOffsetTop = clientY - elemRect.top;
  }

  function drag(e) {
    if (!isDragging || !activeDragEl) return;
    e.preventDefault();
    
    const clientX = e.touches ? e.touches[0].clientX : e.clientX;
    const clientY = e.touches ? e.touches[0].clientY : e.clientY;
    const roomRect = room.getBoundingClientRect();

    let newLeft = clientX - roomRect.left - dragOffsetLeft;
    let newTop = clientY - roomRect.top - dragOffsetTop;

    if (activeDragEl === catRoot) {
      posX = newLeft;
      posY = newTop;
    }
    
    activeDragEl.style.left = `${newLeft}px`;
    activeDragEl.style.top = `${newTop}px`;
  }

  function endDrag() {
    if (activeDragEl) activeDragEl.classList.remove('grabbing');
    isDragging = false;
    activeDragEl = null;
    idleTimer = 60; 
  }

  room.addEventListener('mousedown', startDrag);
  window.addEventListener('mousemove', drag);
  window.addEventListener('mouseup', endDrag);
  room.addEventListener('touchstart', startDrag, {passive: false});
  window.addEventListener('touchmove', drag, {passive: false});
  window.addEventListener('touchend', endDrag);

  startPhysicsLoop();
</script>

</body>
</html>
"""

components.html(html_code, height=550)
