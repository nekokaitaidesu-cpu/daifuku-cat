import streamlit as st

# ページ設定
st.set_page_config(page_title="Daifuku Cat Animation Final", page_icon="🍄")

st.title("もちもちだいふく猫だっち（ファイナル修正版） 🍄")
st.write("赤ペンの指示に全集中して、コードで再現してみたっち！🔥")

# HTML/CSSコード
html_code = """
<!DOCTYPE html>
<html lang="ja">
<head>
<style>
  /* 全体のコンテナ */
  .container {
    display: flex;
    justify_content: center;
    align-items: center;
    height: 400px;
    background-color: #f0f2f6; /* 背景色 */
    overflow: hidden;
  }

  /* 猫の全体ラッパー */
  .cat-wrapper {
    position: relative;
    width: 320px;
    height: 200px;
  }

  /* 体（だいふく部分） */
  .body {
    position: absolute;
    width: 300px;
    height: 190px;
    background-color: #fff;
    border: 4px solid #333;
    border-radius: 50% 50% 45% 45% / 60% 60% 40% 40%;
    z-index: 10;
    top: 0;
    left: 0;
  }

  /* 耳 (修正: より尖らせて、位置を調整) */
  .ear {
    position: absolute;
    width: 45px;
    height: 50px;
    background-color: #fff;
    border: 4px solid #333;
    border-radius: 5px 30px 0 0; /* より尖らせる */
    z-index: 5;
  }
  .ear.left {
    top: -5px; /* 位置調整 */
    left: 45px; /* 位置調整 */
    transform: rotate(-25deg);
  }
  .ear.right {
    top: -10px; /* 位置調整 */
    left: 115px; /* 位置調整 */
    transform: rotate(15deg);
  }
  /* 耳の内側の線を隠すためのカバー */
  .ear-cover {
    position: absolute;
    width: 40px;
    height: 15px;
    background-color: #fff;
    z-index: 11;
    top: 35px;
    left: 2px;
  }

  /* 顔のパーツ (修正: 全体的にかなり下に移動) */
  .face {
    position: absolute;
    z-index: 20;
    top: 110px; /* かなり下に移動 */
    left: 55px; /* 中央寄りに */
  }

  /* 目 */
  .eye {
    position: absolute;
    width: 18px;
    height: 8px;
    border-top: 4px solid #333;
    border-radius: 50%;
    top: 0;
  }
  .eye.left { left: 0; }
  .eye.right { left: 75px; }

  /* ほっぺ (修正: 位置を調整) */
  .cheek {
    position: absolute;
    width: 22px;
    height: 12px;
    background-color: #ffcccc;
    border-radius: 50%;
    opacity: 0.6;
    top: 25px; /* 少し下に */
  }
  .cheek.left { left: -15px; }
  .cheek.right { left: 90px; }

  /* 口 (修正: 位置を調整、少し小さく) */
  .mouth {
    position: absolute;
    width: 18px;
    height: 8px;
    border-bottom: 4px solid #333;
    border-right: 4px solid #333;
    border-radius: 0 0 8px 0;
    transform: rotate(45deg);
    top: 18px; /* 位置調整 */
    left: 38px;
  }
  .mouth::after {
    content: '';
    position: absolute;
    width: 18px;
    height: 8px;
    border-bottom: 4px solid #333;
    border-left: 4px solid #333;
    border-radius: 0 0 0 8px;
    transform: rotate(90deg) translate(-12px, -12px); 
    top: 0;
    left: 0;
  }
  
  /* しっぽ (修正: 元の丸い形に戻す) */
  .tail {
    position: absolute;
    width: 90px;
    height: 70px;
    background-color: #fff;
    border: 4px solid #333;
    border-radius: 50%;
    top: 65px;
    right: -35px;
    z-index: 1;
    transform-origin: 0% 50%;
    animation: wag 1s infinite alternate ease-in-out;
  }

  /* ハート */
  .heart {
    position: absolute;
    color: #333;
    font-size: 20px;
    top: 40px;
    right: -30px;
    z-index: 20;
    animation: float 2s infinite ease-in-out;
    font-weight: bold;
  }

  /* アニメーション定義 */
  @keyframes wag {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(20deg); }
  }

  @keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-8px); }
  }

</style>
</head>
<body>

<div class="container">
  <div class="cat-wrapper">
    <div class="ear left"><div class="ear-cover"></div></div>
    <div class="ear right"><div class="ear-cover"></div></div>
    
    <div class="tail"></div>
    
    <div class="body"></div>
    
    <div class="face">
      <div class="eye left"></div>
      <div class="eye right"></div>
      <div class="cheek left"></div>
      <div class="cheek right"></div>
      <div class="mouth"></div>
    </div>

    <div class="heart">♡</div>
  </div>
</div>

</body>
</html>
"""

# HTMLを描画
st.components.v1.html(html_code, height=450)

st.caption("CSS Animation by Streamlit")
