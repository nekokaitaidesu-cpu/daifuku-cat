import streamlit as st
import streamlit.components.v1 as components

# ページの設定
st.set_page_config(
    page_title="大福キャットのアスレチック",
    page_icon="🍄",
    layout="centered"
)

st.title("Daifuku Athletic Room 🍄")
st.write("足場をドラッグして、好きな場所に配置してみてね！")

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
    height: 450px; /* 少し高さを広げたっち */
    background-color: #fdfaf5;
    border: 4px solid #d4c4b5;
    border-bottom: 8px solid #bfab99;
    border-radius: 12px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    overflow: hidden;
  }

  /* --- 共通のドラッグ可能クラス --- */
  .draggable {
    cursor: grab;
    touch-action: none;
    position: absolute;
  }
  .draggable.grabbing {
    cursor: grabbing;
    z-index: 100; /* 持ってる時は一番手前に */
  }

  /* --- 大福キャット --- */
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

  /* --- 足場（プラットフォーム）のデザイン --- */
  .platform {
    height: 12px;
    background-color: #e6c68b; /* 木の色 */
    border: 2px solid #bfa068;
    border-radius: 6px;
    box-shadow: 0 4px 0 rgba(0,0,0,0.1);
    /* 木目っぽい模様（CSSストライプ） */
    background-image: repeating-linear-gradient(
      45deg,
      transparent,
      transparent 10px,
      rgba(255,255,255,0.2) 10px,
      rgba(255,255,255,0.2) 20px
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
  
  // 物理変数
  let posX = 130, posY = 300;
  let velocityX = 0, velocityY = 0;
  const gravity = 0.6;
  const friction = 0.92;
  const bounce = -0.3;

  // 状態管理
  let isDragging = false;
  let activeDragEl = null;
  let dragStartX, dragStartY;
  let dragOffsetLeft, dragOffsetTop;

  let idleTimer = 60;
  let isGrounded = false;
  let currentPlatform = null; // 今乗っている台（nullなら床か空中）

  // --- メインループ ---
  function startPhysicsLoop() {
    requestAnimationFrame(updatePhysics);
  }

  function updatePhysics() {
    // 猫の物理演算はドラッグしていない時だけ
    if (!isDragging || activeDragEl !== catRoot) {
      velocityY += gravity;
      velocityX *= friction;
      velocityY *= friction;

      posX += velocityX;
      posY += velocityY;

      const roomRect = room.getBoundingClientRect();
      const charRect = catRoot.getBoundingClientRect();
      
      // お部屋サイズ内での座標制限
      const maxX = roomRect.width - 90; // 幅90px
      const maxY = roomRect.height - 80; // 高さ80px (影含む全体枠はもう少し大きいが判定はこれで)

      let landedThisFrame = false;

      // --- 足場との衝突判定 ---
      // ジャンプ中（上昇中）はすり抜けて、落下中のみ乗れる
      currentPlatform = null; // 一旦リセット
      
      if (velocityY >= 0) { // 落下中のみ判定
        platforms.forEach(plat => {
          // getBoundingClientRectは画面全体での位置なので、room内相対位置に変換が必要
          // しかしドラッグでstyle.left/topが変わっているので、styleをパースするのが一番正確かつ速い
          const pLeft = parseFloat(plat.style.left);
          const pTop = parseFloat(plat.style.top);
          const pWidth = parseFloat(plat.style.width);
          const pHeight = 16; // border含む高さ概算

          // 猫の足元（X中心、Y下端）
          const catFootX = posX + 45; // 幅90の半分
          const catFootY = posY + 60; // 本体の高さ（影除く）

          // 判定：足場の上にいて、かつ高さが近い
          if (catFootX >= pLeft && catFootX <= pLeft + pWidth) {
             // 許容範囲（足場の少し上〜少し下）
             if (catFootY >= pTop - 5 && catFootY <= pTop + 15) {
               posY = pTop - 60; // 足場の上に乗せる
               velocityY = 0;
               landedThisFrame = true;
               currentPlatform = plat; // この台に乗っていると記録
             }
          }
        });
      }

      // --- 床との衝突判定 ---
      if (!landedThisFrame && posY > maxY) {
        posY = maxY;
        velocityY *= bounce;
        if (Math.abs(velocityY) < 1) velocityY = 0;
        landedThisFrame = true;
      }

      isGrounded = landedThisFrame;

      // 壁・天井
      if (posY < 0) { posY = 0; velocityY *= bounce; }
      if (posX < 0) { posX = 0; velocityX *= bounce; }
      if (posX > maxX) { posX = maxX; velocityX *= bounce; }

      // 自動行動AI
      if (isGrounded && Math.abs(velocityX) < 0.5 && !isDragging) {
        handleIdleBehavior();
      }

      // 見た目の更新
      updateDirection();
      
      // ぽよんアニメーション（着地時）
      // 簡易的に、前フレームで空中かつ今回接地で、速度があった場合
      // （ここでは省略して、自動行動のジャンプだけで可愛く見せる）

      catRoot.style.left = `${posX}px`;
      catRoot.style.top = `${posY}px`;
    }

    requestAnimationFrame(updatePhysics);
  }

  // --- 賢いAI ---
  function handleIdleBehavior() {
    idleTimer--;
    if (idleTimer < 0) {
      // 行動決定 (0:左, 1:右, 2:小ジャンプ, 3:足場へジャンプ/降りる)
      // 足場があるときはジャンプの確率を上げる
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
        case 2: // 小ジャンプ
          velocityY = -5;
          break;
        case 3: 
        case 4: // 特殊ジャンプ（足場へ or 床へ）
          performSpecialJump();
          break;
      }
      idleTimer = 60 + Math.random() * 100;
    }
  }

  function performSpecialJump() {
    // A. 今、足場に乗っているなら → 降りる
    if (currentPlatform) {
       // 左右どちらかに降りる
       velocityX = (Math.random() > 0.5) ? 4 : -4;
       velocityY = -4; // 軽くホップ
       return;
    }

    // B. 今、床にいるなら → 足場に乗りたい
    // ランダムにターゲット足場を選ぶ
    const targetPlat = platforms[Math.floor(Math.random() * platforms.length)];
    
    // 足場の位置を取得
    const pLeft = parseFloat(targetPlat.style.left);
    const pTop = parseFloat(targetPlat.style.top);
    const pWidth = parseFloat(targetPlat.style.width);
    
    // ターゲット地点（足場の中心、少し上）
    const targetX = pLeft + pWidth / 2 - 45; // 猫の中心座標に合わせる
    const targetY = pTop - 60; // 足場の上

    // 現在地より高い場所にある足場だけ狙う
    if (targetY < posY) {
      // ジャンプ計算（物理の公式）
      // 到達したい高さの少し上を頂点とする
      const apexY = targetY - 40; // 足場より40px高く飛ぶ
      const heightDiff = posY - apexY;
      
      // 必要な初速 Vy = -sqrt(2 * g * h)
      const reqVy = -Math.sqrt(2 * gravity * heightDiff);
      
      // 滞空時間（頂点まで + 頂点からターゲットまで）
      // T_up = |Vy| / g
      const t_up = Math.abs(reqVy) / gravity;
      // T_down = sqrt(2 * (targetY - apexY) / g) ... targetY > apexYなので正
      // しかしY軸は下向き正なので、(targetY - apexY) は正の値(40)
      const t_down = Math.sqrt(2 * (targetY - apexY) / gravity);
      const totalTime = t_up + t_down;

      // 必要な水平速度 Vx = 距離 / 時間
      const reqVx = (targetX - posX) / totalTime;

      // 発射！
      velocityY = reqVy;
      velocityX = reqVx;
      
      triggerBounceAnimation(); // 勢いをつける演出
    } else {
      // 足場が下にある（ありえないけど）場合は普通のジャンプ
      velocityY = -6;
    }
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

  // --- 汎用ドラッグ処理 ---
  function startDrag(e) {
    const target = e.target.closest('.draggable');
    if (!target) return;

    isDragging = true;
    activeDragEl = target;
    activeDragEl.classList.add('grabbing');
    
    // 猫の場合はアニメーションリセット
    if (activeDragEl === catRoot) {
      catVisual.classList.remove('boing-effect'); 
      velocityX = 0; velocityY = 0;
      currentPlatform = null;
    }

    const clientX = e.touches ? e.touches[0].clientX : e.clientX;
    const clientY = e.touches ? e.touches[0].clientY : e.clientY;
    
    // room内でのクリック位置計算
    const roomRect = room.getBoundingClientRect();
    const elemRect = activeDragEl.getBoundingClientRect();

    // マウス位置と要素左上のズレを保存
    dragOffsetLeft = clientX - elemRect.left;
    dragOffsetTop = clientY - elemRect.top;
  }

  function drag(e) {
    if (!isDragging || !activeDragEl) return;
    e.preventDefault();
    
    const clientX = e.touches ? e.touches[0].clientX : e.clientX;
    const clientY = e.touches ? e.touches[0].clientY : e.clientY;
    const roomRect = room.getBoundingClientRect();

    // room相対座標に変換
    let newLeft = clientX - roomRect.left - dragOffsetLeft;
    let newTop = clientY - roomRect.top - dragOffsetTop;

    // 画面外に出ないように制限
    // (簡易的に)
    // activeDragEl.style.left = `${newLeft}px`;
    // activeDragEl.style.top = `${newTop}px`;
    
    // 猫の変数(posX, posY)はドラッグ中も同期させる
    if (activeDragEl === catRoot) {
      posX = newLeft;
      posY = newTop;
    }
    
    // 要素に反映
    activeDragEl.style.left = `${newLeft}px`;
    activeDragEl.style.top = `${newTop}px`;
  }

  function endDrag() {
    if (activeDragEl) {
      activeDragEl.classList.remove('grabbing');
    }
    isDragging = false;
    activeDragEl = null;
    idleTimer = 60; 
  }

  // イベントリスナー（room全体で監視して、targetで判断）
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
