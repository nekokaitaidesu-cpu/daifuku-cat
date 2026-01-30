import streamlit as st

# ページ設定
st.set_page_config(page_title="Daifuku Cat Animation Corrected", page_icon="🍄")

st.title("もちもちだいふく猫だっち（修正版） 🍄")
st.write("赤ペンの指示に合わせて、お顔の位置としっぽをフサフサに修正したっち！")

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
    width: 350px; /* しっぽのために少し広げる */
    height: 220px; /* 少し高さを広げる */
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
    top: 10px; /* 少し下げる */
    left: 0;
  }

  /* 耳 (修正: 位置を少し外側に、形を少し尖らせる) */
  .ear {
    position: absolute;
    width: 45px; /* 少し幅を狭く */
    height: 45px; /* 少し高さを低く */
    background-color: #fff;
    border: 4px solid #333;
    border-radius: 10px 35px 0 0; /* 角丸を調整して尖らせる */
    z-index: 5;
  }
  .ear.left {
    top: 0px; /* 位置調整 */
    left: 35px; /* 位置調整 */
    transform: rotate(-25deg); /* 角度調整 */
  }
  .ear.right {
    top: 0px; /* 位置調整 */
    left: 120px; /* 位置調整 */
    transform: rotate(15deg); /* 角度調整 */
  }
  /* 耳の内側の線を隠すためのカバー */
  .ear-cover {
    position: absolute;
    width: 38px;
    height: 15px;
    background-color: #fff;
    z-index: 11;
    top: 28px;
    left: 2px;
  }

  /* 顔のパーツ (修正: 全体的に下に移動) */
  .face {
    position: absolute;
    z-index: 20;
    top: 100px; /* 下に移動 */
    left: 60px; /* 少し右に移動して中央寄せ */
  }

  /* 目 (修正: 間隔を少し狭める) */
  .eye {
    position: absolute;
    width: 20px;
    height: 10px;
    border-top: 4px solid #333;
    border-radius: 50%;
    top: 0;
  }
  .eye.left { left: 0; }
  .eye.right { left: 70px; } /* 間隔を狭める */

  /* ほっぺ (修正: 位置を調整) */
  .cheek {
    position: absolute;
    width: 20px;
    height: 10px;
    background-color: #ffcccc;
    border-radius: 50%;
    opacity: 0.6;
    top: 20px;
  }
  .cheek.left { left: -10px; } /* 位置調整 */
  .cheek.right { left: 85px; } /* 位置調整 */

  /* 口 (修正: 位置を調整) */
  .mouth {
    position: absolute;
    width: 20px;
    height: 10px;
    border-bottom: 4px solid #333;
    border-right: 4px solid #333;
    border-radius: 0 0 10px 0;
    transform: rotate(45deg);
    top: 15px;
    left: 35px; /* 目の間に合わせる */
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
  
  /* しっぽ (修正: 複数の楕円を組み合わせてフサフサ感を出す) */
  .tail-wrapper {
    position: absolute;
    top: 70px;
    right: -50px;
    z-index: 1;
    transform-origin: 0% 50%;
    animation: wag 1s infinite alternate ease-in-out;
  }
  .tail-part {
    position: absolute;
    background-color: #fff;
    border: 4px solid #333;
    border-radius: 50%;
  }
  /* メインの房 */
  .tail-main {
    width: 100px;
    height: 60px;
    top: 0;
    left: 0;
    z-index: 3;
  }
  /* 上のフサフサ */
  .tail-top {
    width: 50px;
    height: 40px;
    top: -15px;
    left: 40px;
    transform: rotate(-20deg);
    z-index: 2;
  }
  /* 下のフサフサ */
  .tail-bottom {
    width: 50px;
    height: 40px;
    top: 35px;
    left: 30px;
    transform: rotate(20deg);
    z-index: 2;
  }
  /* 継ぎ目を隠すカバー */
  .tail-cover {
    position: absolute;
    background-color: #fff;
    z-index: 4;
  }
  .tail-cover-1 { width: 40px; height: 20px; top: 5px; left: 45px; transform: rotate(-10deg); }
  .tail-cover-2 { width: 40px; height: 20px; top: 35px; left: 35px; transform: rotate(10deg); }


  /* ハート */
  .heart {
    position: absolute;
    color: #333;
    font-size: 24px;
    top: 40px; /* 少し下げる */
    right: -40px;
    z-index: 20;
    animation: float 2s infinite ease-in-out;
    font-weight: bold;
  }

  /* アニメーション定義 */
  @keyframes wag {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(20deg); } /* 角度を少し控えめに */
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
    
    <div class="tail-wrapper">
        <div class="tail-part tail-main"></div>
        <div class="tail-part tail-top"></div>
        <div class="tail-part tail-bottom"></div>
        <div class="tail-cover tail-cover-1"></div>
        <div class="tail-cover tail-cover-2"></div>
    </div>
    
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
