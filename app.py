import streamlit as st
import streamlit.components.v1 as components

# ページの設定
st.set_page_config(
    page_title="大福キャットのアスレチック",
    page_icon="🍄",
    layout="centered"
)

st.title("Daifuku Athletic Room v9 🍄")
st.write("左上のアイコンで「ごはん」と「ボール」を切り替えて遊んでね！")

# HTML/CSS/JSを定義
html_code = """
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<style>
  * { -webkit-tap-highlight-color: transparent; }

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
    cursor: pointer;
  }

  /* --- ツールバー --- */
  .toolbar {
    position: absolute;
    top: 10px;
    left: 10px;
    display: flex;
    gap: 10px;
    z-index: 50;
  }
  
  .tool-btn {
    width: 40px;
    height: 40px;
    background-color: white;
    border: 3px solid #ddd;
    border-radius: 8px;
    font-size: 20px;
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
    transition: transform 0.1s;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  }
  
  .tool-btn:active { transform: scale(0.9); }
  
  /* 選択中のスタイル */
  .tool-btn.active {
    border-color: #ffcc00; /* 黄色い枠 */
    background-color: #fffbe0;
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

  .sleepy { animation: sleep-breath 3s infinite ease-in-out !important; }
  @keyframes sleep-breath {
    0%, 100% { transform: scale(1, 1); }
    50% { transform: scale(1.04, 0.96) translateY(1px); }
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

  .eye { width: 8px; height: 8px; background-color: white; border-radius: 50%; transition: all 0.2s ease-out; }
  .sleepy .eye { height: 2px; border-radius: 1px; transform: scaleX(1.2); margin-top: 2px; }

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
    background-image: repeating-linear-gradient(45deg, transparent, transparent 10px, rgba(255,255,255,0.2) 10px, rgba(255,255,255,0.2) 20px);
  }

  /* --- お魚 --- */
  .fish {
    position: absolute;
    font-size: 24px;
    pointer-events: none;
    animation: float-fish 1s infinite ease-in-out;
    z-index: 5;
  }
  @keyframes float-fish {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-5px); }
  }

  .heart {
    position: absolute;
    font-size: 20px;
    color: #ff6b6b;
    pointer-events: none;
    animation: float-heart 1s forwards ease-out;
    z-index: 20;
  }
  @keyframes float-heart {
    0% { transform: translateY(0) scale(0.5); opacity: 1; }
    100% { transform: translateY(-30px) scale(1.5); opacity: 0; }
  }

  .notice-mark {
    position: absolute;
    font-size: 24px;
    color: #ff4500;
    font-weight: bold;
    pointer-events: none;
    animation: pop-notice 0.6s forwards ease-out;
    z-index: 20;
  }
  @keyframes pop-notice {
    0% { transform: translateY(0) scale(0); opacity: 0; }
    30% { transform: translateY(-15px) scale(1.2); opacity: 1; }
    100% { transform: translateY(-20px) scale(1.0); opacity: 1; }
  }

  /* --- ボール --- */
  .ball {
    position: absolute;
    width: 30px;
    height: 30px;
    background-color: #ff6b6b; /* 赤いボール */
    border-radius: 50%;
    border: 2px solid #e05555;
    box-shadow: inset -5px -5px 10px rgba(0,0,0,0.2);
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 14px;
    z-index: 6;
  }
  /* サッカーボールっぽい模様（簡易） */
  .ball::after {
    content: "⚽";
    font-size: 24px;
    opacity: 0.8;
  }

</style>
</head>
<body>

  <div class="room-container" id="room">
    <div class="toolbar">
      <div class="tool-btn active" id="btn-fish" onclick="setMode('fish')">🐟</div>
      <div class="tool-btn" id="btn-ball" onclick="setMode('ball')">⚽</div>
    </div>

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
  const room = document.getElementById('room');
  const platforms = document.querySelectorAll('.platform');
  const btnFish = document.getElementById('btn-fish');
  const btnBall = document.getElementById('btn-ball');
  
  // --- 状態管理 ---
  let currentMode = 'fish'; // 'fish' or 'ball'
  let posX = 130, posY = 300;
  let velocityX = 0, velocityY = 0;
  const gravity = 0.6;
  const friction = 0.92; 
  const bounce = -0.3;

  let isDragging = false;
  let hasDragged = false;
  let activeDragEl = null;
  let dragStartX, dragStartY;
  let dragOffsetLeft, dragOffsetTop;

  let idleTimer = 60;
  let isGrounded = false;
  let currentPlatform = null;
  
  let currentFish = null;
  let ballObj = null; // { el, x, y, vx, vy }

  let isNoticing = false;
  let noticeTimeout = null;

  let jumpAnim = {
    active: false,
    startTime: 0,
    duration: 0,
    startX: 0,
    startY: 0,
    targetEl: null,
    targetFloorX: 0,
    targetFloorY: 0,
    targetFish: null,
    peakHeight: 0
  };

  // --- モード切替 ---
  window.setMode = function(mode) {
    currentMode = mode;
    if (mode === 'fish') {
      btnFish.classList.add('active');
      btnBall.classList.remove('active');
    } else {
      btnFish.classList.remove('active');
      btnBall.classList.add('active');
    }
  }

  // --- クリックイベント ---
  room.addEventListener('click', (e) => {
    if (hasDragged) return;
    if (e.target.closest('.draggable') || e.target.closest('.tool-btn')) return;

    const roomRect = room.getBoundingClientRect();
    const clickX = e.clientX - roomRect.left;
    const clickY = e.clientY - roomRect.top;

    if (currentMode === 'fish') {
      // お魚モード処理
      if (currentFish || isNoticing || (jumpAnim.active && jumpAnim.targetFish)) return;
      spawnFish(clickX, clickY);

    } else if (currentMode === 'ball') {
      // ボールモード処理：ボールを生成（既にあればリセットして移動）
      spawnBall(clickX, clickY);
    }
  });

  function spawnFish(x, y) {
    const fish = document.createElement('div');
    fish.classList.add('fish');
    fish.textContent = '🐟';
    fish.style.left = (x - 12) + 'px';
    fish.style.top = (y - 12) + 'px';
    room.appendChild(fish);
    currentFish = fish;
    startNoticeSequence(x, y);
  }

  function spawnBall(x, y) {
    // 既存のボールがあれば削除
    if (ballObj && ballObj.el) ballObj.el.remove();

    const ballEl = document.createElement('div');
    ballEl.classList.add('ball');
    ballEl.style.left = (x - 15) + 'px';
    ballEl.style.top = (y - 15) + 'px';
    room.appendChild(ballEl);

    ballObj = {
      el: ballEl,
      x: x - 15,
      y: y - 15,
      vx: 0,
      vy: 0
    };
    
    // 生成時に少し跳ねさせる
    ballObj.vy = -5;
    
    // 猫が気づく
    wakeUp();
  }

  // --- 物理ループ ---
  function startPhysicsLoop() {
    requestAnimationFrame(updatePhysics);
  }

  function updatePhysics(timestamp) {
    // 1. ボールの物理演算
    if (ballObj) {
      updateBallPhysics();
    }

    // 2. 猫のジャンプアニメーション（お魚）
    if (jumpAnim.active) {
      handleJumpAnim(timestamp);
      requestAnimationFrame(updatePhysics);
      return;
    }

    // 3. 猫の通常物理演算
    if (!isDragging || activeDragEl !== catRoot) {
      updateCatPhysics();
    }

    requestAnimationFrame(updatePhysics);
  }

  function updateBallPhysics() {
    ballObj.vy += gravity;
    ballObj.vx *= 0.98; // ボールは転がりやすいように摩擦少なめ
    ballObj.vy *= 0.98;

    ballObj.x += ballObj.vx;
    ballObj.y += ballObj.vy;

    const roomRect = room.getBoundingClientRect();
    const maxX = roomRect.width - 30; // ボール幅
    const maxY = roomRect.height - 30;

    // 床・壁・天井
    if (ballObj.y > maxY) {
      ballObj.y = maxY;
      ballObj.vy *= -0.7; // 弾む
      if(Math.abs(ballObj.vy) < 1) ballObj.vy = 0;
    }
    if (ballObj.x < 0) { ballObj.x = 0; ballObj.vx *= -0.7; }
    if (ballObj.x > maxX) { ballObj.x = maxX; ballObj.vx *= -0.7; }
    
    // 足場との衝突（簡易）
    platforms.forEach(plat => {
      const pLeft = parseFloat(plat.style.left);
      const pTop = parseFloat(plat.style.top);
      const pWidth = parseFloat(plat.style.width);
      
      const ballCX = ballObj.x + 15;
      const ballCY = ballObj.y + 30;

      if (ballCX >= pLeft && ballCX <= pLeft + pWidth) {
         if (ballCY >= pTop - 5 && ballCY <= pTop + 15 && ballObj.vy > 0) {
            ballObj.y = pTop - 30;
            ballObj.vy *= -0.7;
         }
      }
    });

    ballObj.el.style.left = `${ballObj.x}px`;
    ballObj.el.style.top = `${ballObj.y}px`;
  }

  function updateCatPhysics() {
      velocityY += gravity;
      velocityX *= friction;
      velocityY *= friction;
      posX += velocityX;
      posY += velocityY;

      const roomRect = room.getBoundingClientRect();
      const maxX = roomRect.width - 90;
      const maxY = roomRect.height - 80;

      let landedThisFrame = false;
      if (velocityY >= 0) {
        platforms.forEach(plat => {
          const pLeft = parseFloat(plat.style.left);
          const pTop = parseFloat(plat.style.top);
          const pWidth = parseFloat(plat.style.width);
          const catFootX = posX + 45;
          const catFootY = posY + 60;
          if (catFootX >= pLeft && catFootX <= pLeft + pWidth) {
             if (catFootY >= pTop - 15 && catFootY <= pTop + 20) {
               posY = pTop - 60;
               velocityY = 0;
               velocityX = 0;
               landedThisFrame = true;
               currentPlatform = plat;
             }
          }
        });
      }
      if (!landedThisFrame && posY > maxY) {
        posY = maxY; velocityY = 0; velocityX = 0; landedThisFrame = true; currentPlatform = null;
      }
      if (currentPlatform) {
         const pLeft = parseFloat(currentPlatform.style.left);
         const pWidth = parseFloat(currentPlatform.style.width);
         const catCenter = posX + 45;
         if (catCenter < pLeft || catCenter > pLeft + pWidth) { currentPlatform = null; wakeUp(); }
      }
      isGrounded = landedThisFrame;
      if (posY < 0) { posY = 0; velocityY *= bounce; }
      if (posX < 0) { posX = 0; velocityX *= bounce; }
      if (posX > maxX) { posX = maxX; velocityX *= bounce; }

      // --- ボールとの衝突判定（キック！） ---
      if (ballObj) {
         const catCX = posX + 45;
         const catCY = posY + 40;
         const ballCX = ballObj.x + 15;
         const ballCY = ballObj.y + 15;
         
         const dx = ballCX - catCX;
         const dy = ballCY - catCY;
         const dist = Math.sqrt(dx*dx + dy*dy);
         
         // 接触判定 (半径の和 + マージン)
         if (dist < 55) {
             // 衝突！
             // 猫の速度を加算
             const kickPower = 0.2;
             ballObj.vx += dx * kickPower + velocityX * 1.5;
             ballObj.vy += dy * kickPower + velocityY * 1.5 - 2; // 少し浮かせる
             
             // 猫も少し反動
             velocityX -= dx * 0.05;
         }
      }

      // 自動行動
      if (isGrounded && !isDragging && !isNoticing) {
        // ★ボールモードならボールを追いかける★
        if (currentMode === 'ball' && ballObj) {
             chaseBallAI();
        } else {
             handleIdleBehavior();
        }
      }

      if (!catVisual.classList.contains('sleepy')) { updateDirectionBySpeed(velocityX); }
      catRoot.style.left = `${posX}px`; catRoot.style.top = `${posY}px`;
  }

  function chaseBallAI() {
      // ボールの方へ移動
      const ballCX = ballObj.x + 15;
      const catCX = posX + 45;
      const diffX = ballCX - catCX;
      
      if (Math.abs(diffX) > 10) {
          // 走る
          velocityX += (diffX > 0 ? 0.5 : -0.5);
          // 速度制限
          if (velocityX > 4) velocityX = 4;
          if (velocityX < -4) velocityX = -4;
      }
      
      // ボールが高いところにある場合、ジャンプ
      if (ballObj.y < posY - 50 && Math.random() < 0.05) {
          velocityY = -8;
      }
      
      // 時々休憩（ランダム停止）
      if (Math.random() < 0.01) {
          velocityX = 0;
      }
  }

  // --- (以下、既存の関数群：省略せずに記述) ---
  
  function handleJumpAnim(timestamp) {
      const elapsed = timestamp - jumpAnim.startTime;
      const progress = Math.min(elapsed / jumpAnim.duration, 1.0);
      let targetX, targetY;
      if (jumpAnim.targetFish) { targetX = jumpAnim.targetFish.x; targetY = jumpAnim.targetFish.y; }
      else if (jumpAnim.targetEl) {
        const pLeft = parseFloat(jumpAnim.targetEl.style.left);
        const pTop = parseFloat(jumpAnim.targetEl.style.top);
        const pWidth = parseFloat(jumpAnim.targetEl.style.width);
        targetX = pLeft + pWidth / 2 - 45; targetY = pTop - 60;
      } else { targetX = jumpAnim.targetFloorX; targetY = jumpAnim.targetFloorY; }
      
      const currentX = jumpAnim.startX + (targetX - jumpAnim.startX) * progress;
      const heightOffset = 4 * jumpAnim.peakHeight * progress * (1 - progress);
      const baseY = jumpAnim.startY + (targetY - jumpAnim.startY) * progress;
      const currentY = baseY - heightOffset;
      posX = currentX; posY = currentY;
      catRoot.style.left = `${posX}px`; catRoot.style.top = `${posY}px`;
      const direction = targetX - jumpAnim.startX;
      updateDirectionBySpeed(direction);
      
      if (progress >= 1.0) {
        jumpAnim.active = false;
        if (jumpAnim.targetFish) {
            eatFish(); isGrounded = false; currentPlatform = null; velocityX = 0; velocityY = 0; jumpAnim.targetFish = null;
        } else {
            velocityX = 0; velocityY = 0;
            if (jumpAnim.targetEl) currentPlatform = jumpAnim.targetEl; else currentPlatform = null;
            isGrounded = true; triggerBounceAnimation();
        }
      }
  }

  function startNoticeSequence(fishX, fishY) {
      isNoticing = true; wakeUp(); velocityX = 0; velocityY = 0;
      const direction = fishX - (posX + 45);
      updateDirectionBySpeed(direction);
      spawnNoticeMark();
      noticeTimeout = setTimeout(() => {
          startJumpToFish(fishX, fishY); isNoticing = false;
          const mark = room.querySelector('.notice-mark'); if(mark) mark.remove();
      }, 600); 
  }

  function spawnNoticeMark() {
      const mark = document.createElement('div');
      mark.classList.add('notice-mark'); mark.textContent = '!';
      mark.style.left = (posX + 40) + 'px'; mark.style.top = (posY - 30) + 'px';
      room.appendChild(mark);
  }

  function startJumpToFish(targetX, targetY) {
    if (!currentFish) { isNoticing = false; return; }
    jumpAnim.active = true; jumpAnim.startTime = performance.now();
    jumpAnim.startX = posX; jumpAnim.startY = posY; jumpAnim.targetEl = null;
    jumpAnim.targetFish = { x: targetX - 45, y: targetY - 30 };
    const destY = jumpAnim.targetFish.y; jumpAnim.peakHeight = 150 + Math.abs(posY - destY) * 0.2;
    const dist = Math.abs(jumpAnim.targetFish.x - posX); jumpAnim.duration = 500 + dist * 1.2;
    triggerBounceAnimation();
  }

  function eatFish() {
      if (currentFish) { currentFish.remove(); currentFish = null; spawnHeart(); triggerBounceAnimation(); }
  }
  function spawnHeart() {
      const heart = document.createElement('div'); heart.classList.add('heart'); heart.textContent = '💕';
      heart.style.left = (posX + 35) + 'px'; heart.style.top = (posY - 20) + 'px';
      room.appendChild(heart); setTimeout(() => heart.remove(), 1000);
  }

  function handleIdleBehavior() {
    idleTimer--;
    if (idleTimer < 0) {
      wakeUp();
      if (currentPlatform) { if (Math.random() < 0.6) { startSleeping(); } else { startPerfectJump(); } }
      else {
          const action = Math.floor(Math.random() * 5); 
          switch(action) {
            case 0: velocityX = -3; if(Math.random()>0.7) velocityY = -3; break;
            case 1: velocityX = 3; if(Math.random()>0.7) velocityY = -3; break;
            case 2: break;
            case 3: case 4: startPerfectJump(); break;
          }
      }
      if (catVisual.classList.contains('sleepy')) idleTimer = 180 + Math.random() * 180; else idleTimer = 60 + Math.random() * 100;
    }
  }

  function startSleeping() { catVisual.classList.add('sleepy'); catFace.classList.remove('face-left', 'face-right'); catRoot.classList.remove('walking-left', 'walking-right'); velocityX = 0; velocityY = 0; }
  function wakeUp() { catVisual.classList.remove('sleepy'); }

  function startPerfectJump() {
    const roomRect = room.getBoundingClientRect(); const maxX = roomRect.width - 90;
    let targetEl = null; let tFloorX = 0; let tFloorY = roomRect.height - 80;
    if (currentPlatform) {
       let otherPlats = []; platforms.forEach(p => { if(p !== currentPlatform) otherPlats.push(p); });
       if (otherPlats.length > 0 && Math.random() > 0.6) targetEl = otherPlats[Math.floor(Math.random() * otherPlats.length)];
       else { targetEl = null; tFloorX = Math.random() * maxX; }
    } else targetEl = platforms[Math.floor(Math.random() * platforms.length)];
    jumpAnim.active = true; jumpAnim.startTime = performance.now(); jumpAnim.startX = posX; jumpAnim.startY = posY;
    jumpAnim.targetEl = targetEl; jumpAnim.targetFish = null; jumpAnim.targetFloorX = tFloorX; jumpAnim.targetFloorY = tFloorY;
    let destY; if (targetEl) destY = parseFloat(targetEl.style.top) - 60; else destY = tFloorY;
    const highestPoint = Math.min(posY, destY); jumpAnim.peakHeight = 120 + Math.abs(posY - destY) * 0.2;
    let dist = 0; if(targetEl) { const pLeft = parseFloat(targetEl.style.left); dist = Math.abs((pLeft + parseFloat(targetEl.style.width)/2) - posX); } else dist = Math.abs(tFloorX - posX);
    jumpAnim.duration = 600 + dist * 1.5; triggerBounceAnimation();
  }

  function updateDirectionBySpeed(val) {
    catFace.classList.remove('face-left', 'face-right'); catRoot.classList.remove('walking-left', 'walking-right');
    if (Math.abs(val) > 0.1) { if (val > 0) { catFace.classList.add('face-right'); catRoot.classList.add('walking-right'); } else { catFace.classList.add('face-left'); catRoot.classList.add('walking-left'); } }
  }
  function triggerBounceAnimation() { catVisual.classList.remove('boing-effect'); void catVisual.offsetWidth; catVisual.classList.add('boing-effect'); }

  function startDrag(e) {
    hasDragged = false; const target = e.target.closest('.draggable'); if (!target) return;
    if (isNoticing) { clearTimeout(noticeTimeout); isNoticing = false; const mark = room.querySelector('.notice-mark'); if(mark) mark.remove(); }
    isDragging = true; activeDragEl = target; activeDragEl.classList.add('grabbing');
    if (activeDragEl === catRoot) { wakeUp(); jumpAnim.active = false; catVisual.classList.remove('boing-effect'); velocityX = 0; velocityY = 0; currentPlatform = null; }
    const clientX = e.touches ? e.touches[0].clientX : e.clientX; const clientY = e.touches ? e.touches[0].clientY : e.clientY;
    const elemRect = activeDragEl.getBoundingClientRect(); dragOffsetLeft = clientX - elemRect.left; dragOffsetTop = clientY - elemRect.top;
  }
  function drag(e) {
    if (!isDragging || !activeDragEl) return; hasDragged = true; e.preventDefault();
    const clientX = e.touches ? e.touches[0].clientX : e.clientX; const clientY = e.touches ? e.touches[0].clientY : e.clientY;
    const roomRect = room.getBoundingClientRect(); let newLeft = clientX - roomRect.left - dragOffsetLeft; let newTop = clientY - roomRect.top - dragOffsetTop;
    if (activeDragEl === catRoot) { posX = newLeft; posY = newTop; } activeDragEl.style.left = `${newLeft}px`; activeDragEl.style.top = `${newTop}px`;
  }
  function endDrag() { if (activeDragEl) activeDragEl.classList.remove('grabbing'); isDragging = false; activeDragEl = null; idleTimer = 60; }

  room.addEventListener('mousedown', startDrag); window.addEventListener('mousemove', drag); window.addEventListener('mouseup', endDrag);
  room.addEventListener('touchstart', startDrag, {passive: false}); window.addEventListener('touchmove', drag, {passive: false}); window.addEventListener('touchend', endDrag);

  startPhysicsLoop();
</script>

</body>
</html>
"""

components.html(html_code, height=550)
