import streamlit as st
import streamlit.components.v1 as components

# ページの設定
st.set_page_config(
    page_title="ふわふわアニメーション",
    page_icon="🍄",
    layout="centered"
)

st.title("CSS Animation Demo 🍄")
st.write("CSSだけで作ったふわふわアニメーションだっち！")

# HTMLとCSSを定義
html_code = """
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<style>
  /* Streamlitのコンポーネント内で綺麗に表示するための調整 */
  body {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh; /* iframeの高さに合わせる */
    margin: 0;
    background-color: transparent; /* 背景はStreamlitに合わせる */
    font-family: sans-serif;
    overflow: hidden; /* スクロールバーを消す */
  }

  .container { text-align: center; }

  /* --- ここから下はさっきと同じCSS --- */
  
  .cat-wrapper {
    position: relative;
    width: 100px;
    height: 100px;
    margin: 0 auto;
    animation: bounce-float 2s infinite ease-in-out;
  }

  .cat-body {
    width: 100%;
    height: 100%;
    background-color: #b0b0b0; /* 猫の色 */
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
  }

  @keyframes bounce-float {
    0%, 100% { transform: translateY(0) scale(1); }
    50% { transform: translateY(-20px) scale(1.05, 0.95); }
  }

  @keyframes shadow-scale {
    0%, 100% { transform: scale(1); opacity: 0.3; }
    50% { transform: scale(0.8); opacity: 0.1; }
  }
  
  p {
    color: #666;
    margin-top: 20px;
    font-size: 14px;
  }
</style>
</head>
<body>
  <div class="container">
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
</body>
</html>
"""

# StreamlitでHTMLを表示（高さは適宜調整）
components.html(html_code, height=350)
