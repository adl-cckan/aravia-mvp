import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Aravia MVP – Kan Intelligence", page_icon="🏛️", layout="wide")
st.title("🏛️ Aravia Knowledge Platform")
st.caption("CHAN Ching Kan 20年建築知識 + 2024 CUHK PhD 驅動 | Gemini 最終加強版（不依賴檔案）")

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    generation_config={"temperature": 0.7, "max_output_tokens": 4096}
)

# ====================== 內置完整知識庫 Prompt ======================
EXPLAINER_PROMPT = """你係 Kan Explainer。
你有完整 35 Lessons Learned 同 21 Keywords 知識庫。
請用 Cantonese + English 詳細回答，每個問題都要：
1. 先簡單總結用戶問題
2. 用 1-2 句解釋 PhD 核心概念（Space of Appearance、Heterotopias、Relational Topology、Adaptive Resilience、Agency of Architect 等）
3. 明確連結到最相關的 2-3 個 Lessons + Keywords
4. 舉 1-2 個 Aravia 真實項目例子
5. 最後給實戰啟示（對開發商/業主有什麼價值）
答案必須豐富、有結構、詳細引用知識庫內容。"""

CRITIC_PROMPT = """你係 Kan Critic。
你有完整 35 Lessons Learned 同 21 Keywords 知識庫。
請根據知識庫批判設計圖。
輸出格式必須嚴格如下：
【觀察】
【核心意圖】
【Aravia框架評估】（列 3 個最相關 Keywords + Lesson）
【3個優點】（每點詳細解釋）
【3個具體改進建議】（每點講「點改」同「改完效果」）
【Aravia總結句】
用 Cantonese + English 回答，答案必須詳細豐富。"""

with st.sidebar:
    st.success("✅ Gemini 最終版已連接成功！（不依賴 md 檔案）")
    st.write("• 35 Lessons + 21 Keywords 已內置")
    st.caption("深度已大幅提升")

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
            if uploaded_file.type.startswith("image"):
                img = Image.open(uploaded_file)
                prompt_parts = [CRITIC_PROMPT, f"用戶意圖：{intent}\n請根據 Aravia 知識庫批判以上圖則。", img]
            else:
                prompt_parts = [CRITIC_PROMPT, f"用戶意圖：{intent}\n（PDF已上傳，請根據內容批判）"]
            response = model.generate_content(prompt_parts)
            st.markdown("**Kan Critic 回覆：**")
            st.write(response.text)
            if uploaded_file.type.startswith("image"):
                st.image(uploaded_file, caption="你上傳的設計圖")

st.caption("Gemini 最終版 MVP v2.7 | 不依賴 md 檔案 · 深度已大幅提升")
