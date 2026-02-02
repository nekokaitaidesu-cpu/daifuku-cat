import streamlit as st
import streamlit.components.v1 as components

# ページの設定
st.set_page_config(
    page_title="大福キャットのアスレチック",
    page_icon="🍄",
    layout="centered"
)

st.title("Daifuku Athletic Room v3 🍄")
st.write("「絶対に着地する」スーパー・ジャンプを実装したっち！")

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
  
  // 物理変数
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
  
  // ★完璧ジャンプ用のアニメーション状態管理
  let jumpAnim = {
    active: false,
    startTime: 0,
    duration: 0,
    startX: 0,
    startY: 0,
    targetEl: null, // 目標の足場要素（nullなら床）
    targetFloorX: 0, // 床の場合の目標X
    targetFloorY: 0, // 床の場合の目標Y
    peakHeight: 0 // ジャンプの頂点の高さ
  };

  function startPhysicsLoop() {
    requestAnimationFrame(updatePhysics);
  }

  function updatePhysics(timestamp) {
    // 1. ジャンプアニメーション中の処理（物理演算を無視して強制移動）
    if (jumpAnim.active) {
      const elapsed = timestamp - jumpAnim.startTime;
      const progress = Math.min(elapsed / jumpAnim.duration, 1.0); // 0.0 〜 1.0

      // 目標地点の計算（足場が動いても追従するように毎回取得）
      let targetX, targetY;
      
      if (jumpAnim.targetEl) {
        // 足場の場合
        const pLeft = parseFloat(jumpAnim.targetEl.style.left);
        const pTop = parseFloat(jumpAnim.targetEl.style.top);
        const pWidth = parseFloat(jumpAnim.targetEl.style.width);
        targetX = pLeft + pWidth / 2 - 45; // 中心
        targetY = pTop - 60; // 足場の上
      } else {
        // 床の場合
        targetX = jumpAnim.targetFloorX;
        targetY = jumpAnim.targetFloorY;
      }

      // イージング関数（滑らかに）
      // X軸: 線形補間
      const currentX = jumpAnim.startX + (targetX - jumpAnim.startX) * progress;
      
      // Y軸: 放物線（ベジェ曲線的な計算）
      // progress 0.5 の時に peakHeight に達するようにする
      // 公式: (1-t)^2 * start + 2(1-t)t * control + t^2 * end
      // 制御点(Control Point)の高さを計算して調整
      
      // シンプルな放物線: y = start + (target - start)*t - 4*H*t*(1-t)
      // H = peakHeight (ジャンプの高さ)
      const heightOffset = 4 * jumpAnim.peakHeight * progress * (1 - progress);
      const baseY = jumpAnim.startY + (targetY - jumpAnim.startY) * progress;
      const currentY = baseY - heightOffset;

      // 座標適用
      posX = currentX;
      posY = currentY;
      catRoot.style.left = `${posX}px`;
      catRoot.style.top = `${posY}px`;

      // 向きの更新
      const direction = targetX - jumpAnim.startX;
      updateDirectionBySpeed(direction);

      // 終了判定
      if (progress >= 1.0) {
        // 着地！
        jumpAnim.active = false;
        velocityX = 0; 
        velocityY = 0;
        
        // 足場の上なら登録
        if (jumpAnim.targetEl) {
          currentPlatform = jumpAnim.targetEl;
        } else {
          currentPlatform = null; // 床
        }
        isGrounded = true;
        triggerBounceAnimation();
      }
      
      requestAnimationFrame(updatePhysics);
      return; // 物理演算処理はスキップ
    }


    // 2. 通常の物理演算（ドラッグ中以外）
    if (!isDragging || activeDragEl !== catRoot) {
      velocityY += gravity;
      velocityX *= friction;
      velocityY *= friction;

      posX += velocityX;
      posY += velocityY;

      const roomRect = room.getBoundingClientRect();
      const maxX = roomRect.width - 90;
      const maxY = roomRect.height - 80;

      let landedThisFrame = false;

      // --- 足場との衝突判定 ---
      // 落下中のみ
      if (velocityY >= 0) {
        platforms.forEach(plat => {
          const pLeft = parseFloat(plat.style.left);
          const pTop = parseFloat(plat.style.top);
          const pWidth = parseFloat(plat.style.width);
          
          const catFootX = posX + 45;
          const catFootY = posY + 60;

          if (catFootX >= pLeft && catFootX <= pLeft + pWidth) {
             // 判定を少し甘めに
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

      // --- 床との衝突判定 ---
      if (!landedThisFrame && posY > maxY) {
        posY = maxY;
        velocityY = 0;
        velocityX = 0;
        landedThisFrame = true;
        currentPlatform = null;
      }

      // 足場から落ちたかどうかのチェック
      // 今「乗ってる」はずなのに、座標が足場外なら currentPlatform を解除
      if (currentPlatform) {
         const pLeft = parseFloat(currentPlatform.style.left);
         const pWidth = parseFloat(currentPlatform.style.width);
         const catCenter = posX + 45;
         if (catCenter < pLeft || catCenter > pLeft + pWidth) {
            currentPlatform = null; // 足場から外れた（落下開始）
         }
      }

      isGrounded = landedThisFrame;

      if (posY < 0) { posY = 0; velocityY *= bounce; }
      if (posX < 0) { posX = 0; velocityX *= bounce; }
      if (posX > maxX) { posX = maxX; velocityX *= bounce; }

      // 自動行動AI
      if (isGrounded && !isDragging) {
        handleIdleBehavior();
      }

      updateDirectionBySpeed(velocityX);

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
        case 4: // 特殊ジャンプ（確実モード）
          startPerfectJump();
          break;
      }
      idleTimer = 60 + Math.random() * 100;
    }
  }

  function startPerfectJump() {
    const roomRect = room.getBoundingClientRect();
    const maxX = roomRect.width - 90;
    const maxY = roomRect.height - 80;
    
    let targetEl = null; // 目標足場
    let tFloorX = 0;
    let tFloorY = maxY;

    // A. 今、足場に乗っている場合 -> 「床」または「別の足場」へ
    if (currentPlatform) {
       // 別の足場を探す
       let otherPlats = [];
       platforms.forEach(p => { if(p !== currentPlatform) otherPlats.push(p); });
       
       // 70%で床、30%で別の足場（あれば）
       if (otherPlats.length > 0 && Math.random() > 0.6) {
          targetEl = otherPlats[Math.floor(Math.random() * otherPlats.length)];
       } else {
          // 床へ
          targetEl = null;
          tFloorX = Math.random() * maxX;
       }
    } 
    // B. 今、床にいる場合 -> 「足場」へ
    else {
       targetEl = platforms[Math.floor(Math.random() * platforms.length)];
    }

    // --- ジャンプアニメーション開始設定 ---
    jumpAnim.active = true;
    jumpAnim.startTime = performance.now();
    jumpAnim.startX = posX;
    jumpAnim.startY = posY;
    jumpAnim.targetEl = targetEl;
    jumpAnim.targetFloorX = tFloorX;
    jumpAnim.targetFloorY = tFloorY;

    // 目標のY座標を取得（高さ計算用）
    let destY;
    if (targetEl) {
       destY = parseFloat(targetEl.style.top) - 60;
    } else {
       destY = tFloorY;
    }

    // ジャンプの高さ設定（今の位置と目標のうち、高い方よりもさらに80px上まで飛ぶ）
    const highestPoint = Math.min(posY, destY);
    const apex = highestPoint - 80;
    // 高さの差分（現在のY座標からの相対値）
    // 数式上 heightOffset = 4 * H * ... なので、H は頂点までの距離
    // H = startY - apex; だが、移動中にYが変化するので単純に「一番高いところへの差分」＋αを設定
    jumpAnim.peakHeight = 120 + Math.abs(posY - destY) * 0.2; // 距離に応じて少し高く

    // 距離に応じた時間設定
    let dist = 0;
    if(targetEl) {
        const pLeft = parseFloat(targetEl.style.left);
        dist = Math.abs((pLeft + parseFloat(targetEl.style.width)/2) - posX);
    } else {
        dist = Math.abs(tFloorX - posX);
    }
    jumpAnim.duration = 600 + dist * 1.5; // 近ければ速く、遠ければゆっくり

    // ジャンプ直前の溜めモーション（見た目だけ）
    triggerBounceAnimation();
  }

  function updateDirectionBySpeed(val) {
    catFace.classList.remove('face-left', 'face-right');
    catRoot.classList.remove('walking-left', 'walking-right');
    if (Math.abs(val) > 0.1) {
      if (val > 0) {
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
      jumpAnim.active = false; // 強制ジャンプ中断
      catVisual.classList.remove('boing-effect'); 
      velocityX = 0; velocityY = 0;
      currentPlatform = null;
    }

    const clientX = e.touches ? e.touches[0].clientX : e.clientX;
    const clientY = e.touches ? e.touches[0].clientY : e.clientY;
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

### これでどうだっち！？🍄✨

今回は物理演算を一時的に無視して、**「絶対に目的地へたどり着くルート」を強制的に通る** ようにしたっち。
だから、頭をぶつけたり、届かなくて落ちることはもうないっち！

しかも、**「ホーミング機能」** つきだから、大福ちゃんがジャンプしている最中に、主さんが意地悪して足場をドラッグして動かしても、**空中で軌道修正して追いかけて乗ってくる** はずだっち！

ちょっと執念深くて可愛い大福ちゃんになったから、ぜひ試してみてほしいっち！(o^^o)
