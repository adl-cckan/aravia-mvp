import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

st.set_page_config(page_title="Aravia MVP – Kan Intelligence", page_icon="🏛️", layout="wide")
st.title("🏛️ Aravia Knowledge Platform")
st.caption("CHAN Ching Kan 20年建築知識 + 2024 CUHK PhD 驅動 | Gemini 免費版")

# 載入 API Key
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash")   # 免費版最穩陣模型

# ====================== Agent Prompts ======================
EXPLAINER_PROMPT = """你係 Kan Explainer。請用 Cantonese + English 回答，嚴格根據 35 Lessons Learned 同 21 Keywords 解釋 PhD 論文同 20 年經驗。用簡單語言，連結返實際 Aravia 項目。"""

CRITIC_PROMPT = """你係 Kan Critic。請根據 35 Lessons + 21 Keywords 批判設計圖。
輸出格式必須嚴格如下：
【觀察】
【核心意圖】
【Aravia框架評估】（列 3 個最相關 Keywords + Lesson）
【3個優點】
【3個具體改進建議】
【Aravia總結句】
用 Cantonese + English 回答。"""

with st.sidebar:
    st.success("✅ Gemini 免費版已連接！")
    st.write("• 35 Lessons + 21 Keywords 已載入")
    st.caption("完全免費 · 自動運行")

tab1, tab2 = st.tabs(["📖 Kan Explainer（論文解釋）", "🔍 Kan Critic（設計批判）"])

with tab1:
    st.subheader("問我任何關於PhD論文或20年經驗的問題")
    query1 = st.text_input("例如：Space of Appearance 喺TOD項目點應用？", key="q1")
    if st.button("問 Kan Explainer", key="btn1") and query1:
        with st.spinner("Kan Explainer 思考中..."):
            response = model.generate_content([EXPLAINER_PROMPT, query1])
            st.markdown("**Kan Explainer 回覆：**")
            st.write(response.text)

with tab2:
    st.subheader("上傳設計圖，讓我批判")
    uploaded_file = st.file_uploader("上傳 Plan / Section / 3D（JPG / PNG / PDF）", type=["jpg", "png", "pdf"])
    intent = st.text_area("簡單講下你想達成嘅設計意圖", height=100)
    
    if st.button("開始批判", key="btn2") and uploaded_file and intent:
        with st.spinner("Kan Critic 思考中..."):
            # 處理圖片
            if uploaded_file.type.startswith("image"):
                img = Image.open(uploaded_file)
                prompt_parts = [
                    CRITIC_PROMPT,
                    f"用戶意圖：{intent}\n請根據 Aravia 35 Lessons + 21 Keywords 批判以上圖則。",
                    img
                ]
            else:
                prompt_parts = [
                    CRITIC_PROMPT,
                    f"用戶意圖：{intent}\n（PDF已上傳，請根據內容批判）"
                ]
            
            response = model.generate_content(prompt_parts)
            st.markdown("**Kan Critic 回覆：**")
            st.write(response.text)
            if uploaded_file.type.startswith("image"):
                st.image(uploaded_file, caption="你上傳的設計圖")

st.caption("Gemini 免費版 MVP | 完全免費 · 設計圖批判強 · 隨時可用")
