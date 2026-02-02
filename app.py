import streamlit as st
import streamlit.components.v1 as components

# ページの設定
st.set_page_config(
    page_title="ふわふわアニメーション",
    page_icon="🍄",
    layout="centered"
)

st.title("Interactive Cat Demo 🍄")
st.write("猫ちゃんをタップ（クリック）して掴んで動かしてみてね！")

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
    background-color: transparent;
    font-family: sans-serif;
    overflow: hidden;
    /* 選択できないようにしてドラッグしやすくする */
    user-select: none;
    -webkit-user-select: none;
  }

  /* 動かせるコンテナ */
  #draggable-root {
    position: absolute;
    /* 画面中央に配置（幅100pxの半分50px、高さ約130pxの半分65pxを引く） */
    left: calc(50% - 50px);
    top: calc(50% - 65px);
    width: 100px;
    cursor: grab;
    /* タッチ操作の遅延をなくす */
    touch-action: none;
    transition: transform 0.1s; /* つまんだ時の変形を滑らかに */
  }

  /* つまんでいる時のスタイル */
  #draggable-root.grabbing {
    cursor: grabbing;
    transform: scale(0.9); /* 少し縮んで「つまんでる感」を出す */
  }

  /* --- 以下、前回と同じアニメーションCSS --- */
  
  .cat-wrapper {
    position: relative;
    width: 100px;
    height: 100px;
    margin: 0 auto;
    animation: bounce-float 2s infinite ease-in-out;
    pointer-events: none; /* クリック判定を親要素に任せる */
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
    margin: 20px auto 0;
    animation: shadow-scale 2s infinite ease-in-out;
    pointer-events: none;
  }

  @keyframes bounce-float {
    0%, 100% { transform: translateY(0) scale(1); }
    50% { transform: translateY(-20px) scale(1.05, 0.95); }
  }

  @keyframes shadow-scale {
    0%, 100% { transform: scale(1); opacity: 0.3; }
    50% { transform: scale(0.8); opacity: 0.1; }
  }
</style>
</head>
<body>

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

<script>
  const draggable = document.getElementById('draggable-root');
  
  let isDragging = false;
  let startX, startY, initialLeft, initialTop;

  // マウス/タッチ開始時の処理
  function startDrag(e) {
    isDragging = true;
    draggable.classList.add('grabbing'); // クラス追加で見た目を変える
    
    // タッチとマウスの座標取得を統一
    const clientX = e.touches ? e.touches[0].clientX : e.clientX;
    const clientY = e.touches ? e.touches[0].clientY : e.clientY;

    startX = clientX;
    startY = clientY;

    // 現在の要素の位置を取得
    const rect = draggable.getBoundingClientRect();
    
    // コンテナ(body)に対する相対位置を計算
    initialLeft = rect.left;
    initialTop = rect.top;
  }

  // ドラッグ中の処理
  function drag(e) {
    if (!isDragging) return;
    e.preventDefault(); // スクロール防止

    const clientX = e.touches ? e.touches[0].clientX : e.clientX;
    const clientY = e.touches ? e.touches[0].clientY : e.clientY;

    const dx = clientX - startX;
    const dy = clientY - startY;

    // 新しい位置を設定
    draggable.style.left = `${initialLeft + dx}px`;
    draggable.style.top = `${initialTop + dy}px`;
  }

  // ドラッグ終了時の処理
  function endDrag() {
    isDragging = false;
    draggable.classList.remove('grabbing');
  }

  // イベントリスナー登録（マウス）
  draggable.addEventListener('mousedown', startDrag);
  window.addEventListener('mousemove', drag);
  window.addEventListener('mouseup', endDrag);

  // イベントリスナー登録（スマホ・タッチ）
  draggable.addEventListener('touchstart', startDrag, {passive: false});
  window.addEventListener('touchmove', drag, {passive: false});
  window.addEventListener('touchend', endDrag);
</script>

</body>
</html>
"""

# 高さを少し広げて画面全体を使いやすくする
components.html(html_code, height=500)
