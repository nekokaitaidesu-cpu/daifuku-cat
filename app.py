import streamlit as st

# ページ設定
st.set_page_config(page_title="Daifuku Cat Animation", page_icon="🍄")

st.title("もちもちだいふく猫だっち 🍄")
st.write("HTMLとCSSだけで描画して動かしているっち！")

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

  /* 耳 */
  .ear {
    position: absolute;
    width: 50px;
    height: 50px;
    background-color: #fff;
    border: 4px solid #333;
    border-radius: 10px 40px 0 0;
    z-index: 5;
  }
  .ear.left {
    top: -15px;
    left: 40px;
    transform: rotate(-20deg);
  }
  .ear.right {
    top: -15px;
    left: 110px;
    transform: rotate(10deg);
  }
  /* 耳の内側の線を隠すためのカバー */
  .ear-cover {
    position: absolute;
    width: 40px;
    height: 10px;
    background-color: #fff;
    z-index: 11;
    top: 25px;
    left: 5px;
  }

  /* 顔のパーツ */
  .face {
    position: absolute;
    z-index: 20;
    top: 80px;
    left: 40px;
  }

  /* 目 (ニコニコ) */
  .eye {
    position: absolute;
    width: 20px;
    height: 10px;
    border-top: 4px solid #333;
    border-radius: 50%;
    top: 0;
  }
  .eye.left { left: 0; }
  .eye.right { left: 80px; }

  /* ほっぺ */
  .cheek {
    position: absolute;
    width: 20px;
    height: 10px;
    background-color: #ffcccc;
    border-radius: 50%;
    opacity: 0.6;
    top: 20px;
  }
  .cheek.left { left: -15px; }
  .cheek.right { left: 95px; }

  /* 口 (wの形) */
  .mouth {
    position: absolute;
    width: 20px;
    height: 10px;
    border-bottom: 4px solid #333;
    border-right: 4px solid #333;
    border-radius: 0 0 10px 0;
    transform: rotate(45deg);
    top: 15px;
    left: 40px;
  }
  .mouth::after {
    content: '';
    position: absolute;
    width: 20px;
    height: 10px;
    border-bottom: 4px solid #333;
    border-left: 4px solid #333;
    border-radius: 0 0 0 10px;
    transform: rotate(90deg) translate(-14px, -14px); 
    top: 0;
    left: 0;
  }
  
  /* しっぽ */
  .tail {
    position: absolute;
    width: 100px;
    height: 60px;
    background-color: #fff;
    border: 4px solid #333;
    border-radius: 50%;
    top: 60px;
    right: -40px;
    z-index: 1;
    transform-origin: 0% 50%; /* 左側を中心に回転 */
    animation: wag 1s infinite alternate ease-in-out; /* アニメーション設定 */
  }

  /* ハート */
  .heart {
    position: absolute;
    color: #333;
    font-size: 24px;
    top: 30px;
    right: -40px;
    z-index: 20;
    animation: float 2s infinite ease-in-out;
    font-weight: bold;
  }

  /* アニメーション定義 */
  @keyframes wag {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(25deg); }
  }

  @keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
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
