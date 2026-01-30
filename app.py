import streamlit as st
import base64

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# ページ設定
st.set_page_config(page_title="ぬるぬる大福キャット", layout="centered")

st.title("大福キャットがぬるぬる動くよ！🍄")

# 画像ファイルのパス（※ここに保存した画像ファイル名を指定してね）
image_filename = 'daifuku_cat.png'

try:
    # 画像をBase64に変換してHTMLに埋め込む（これでGitHub/Streamlit上でも確実に表示されるよ）
    img_base64 = get_base64_of_bin_file(image_filename)
    
    # CSSとHTMLの定義
    html_code = f"""
    <style>
        @keyframes nurunuru {{
            0% {{
                transform: scale(1, 1) translateY(0);
            }}
            50% {{
                /* 横に伸びて、縦に縮む（つぶれる感じ） */
                transform: scale(1.1, 0.9) translateY(10px);
            }}
            100% {{
                transform: scale(1, 1) translateY(0);
            }}
        }}

        .daifuku-container {{
            display: flex;
            justify_content: center;
            align_items: center;
            height: 400px;
            /* 背景をちょっと和風な色にしてみたっち */
            background-color: #f0f8ff; 
            border-radius: 20px;
        }}

        .daifuku-img {{
            width: 300px; /* サイズはここで調整してね */
            /* アニメーションの設定：3秒かけてゆったり動く */
            animation: nurunuru 3s infinite ease-in-out;
            filter: drop-shadow(0px 10px 10px rgba(0,0,0,0.2));
        }}
    </style>

    <div class="daifuku-container">
        <img src="data:image/png;base64,{img_base64}" class="daifuku-img">
    </div>
    """

    # HTMLを表示
    st.markdown(html_code, unsafe_allow_html=True)

except FileNotFoundError:
    st.error(f"エラー: '{image_filename}' が見つからないだっち！画像を同じフォルダに入れてね🍄")

st.write("大福みたいに、もちもち呼吸してるイメージだっち！")
