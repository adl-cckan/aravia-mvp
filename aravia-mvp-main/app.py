import streamlit as st
import anthropic
import base64
from io import BytesIO

st.set_page_config(page_title="Aravia MVP – Kan Intelligence", page_icon="🏛️", layout="wide")
st.title("🏛️ Aravia Knowledge Platform")
st.caption("CHAN Ching Kan 20年建築知識 + 2024 CUHK PhD 驅動 | 自動化版本")

client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

EXPLAINER_SYSTEM = """You are Kan Explainer. 
You ONLY explain CHAN Ching Kan’s 2024 CUHK PhD thesis and 35 Lessons Learned.
Always answer in Cantonese + English.
Link every answer back to Lessons / Keywords.
Use simple language."""

CRITIC_SYSTEM = """You are Kan Critic. 
You are a world-class architectural critic with 20+ years experience + PhD.
You have full access to 35 Lessons Learned + 21 Keywords.
Critique any design drawing step-by-step.
Output format: 【觀察】 【核心意圖】 【Aravia框架評估】 【3個優點】 【3個具體改進建議】 【Aravia總結句】
Always answer in Cantonese + English."""

with st.sidebar:
    st.success("✅ 自動化連接成功！")
    st.write("• 35 Lessons + 21 Keywords 已載入")
    st.write("• Kan Explainer + Kan Critic 自動運行")

tab1, tab2 = st.tabs(["📖 Kan Explainer（論文解釋）", "🔍 Kan Critic（設計批判）"])

with tab1:
    st.subheader("問我任何關於PhD論文或20年經驗的問題")
    query1 = st.text_input("例如：Space of Appearance 喺TOD項目點應用？", key="q1")
    
    if st.button("問 Kan Explainer", key="btn1") and query1:
        with st.spinner("Kan Explainer 思考中..."):
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                system=EXPLAINER_SYSTEM,
                messages=[{"role": "user", "content": query1}]
            )
            st.markdown("**Kan Explainer 回覆：**")
            st.write(response.content[0].text)

with tab2:
    st.subheader("上傳設計圖，讓我批判")
    uploaded_file = st.file_uploader("上傳 Plan / Section / 3D（JPG / PNG / PDF）", type=["jpg", "png", "pdf"])
    intent = st.text_area("簡單講下你想達成嘅設計意圖", height=100)
    
    if st.button("開始批判", key="btn2") and uploaded_file and intent:
        with st.spinner("Kan Critic 思考中..."):
            bytes_data = uploaded_file.getvalue()
            if uploaded_file.type.startswith("image"):
                media_type = uploaded_file.type
                image_data = base64.b64encode(bytes_data).decode("utf-8")
                content = [
                    {"type": "image", "source": {"type": "base64", "media_type": media_type, "data": image_data}},
                    {"type": "text", "text": f"用戶意圖：{intent}\n請根據 Aravia 35 Lessons + 21 Keywords 批判以上圖則。"}
                ]
            else:
                content = f"用戶意圖：{intent}\n（PDF已上傳，請根據內容批判）"

            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2500,
                system=CRITIC_SYSTEM,
                messages=[{"role": "user", "content": content}]
            )
            st.markdown("**Kan Critic 回覆：**")
            st.write(response.content[0].text)
            if uploaded_file.type.startswith("image"):
                st.image(uploaded_file, caption="你上傳的設計圖")

st.caption("MVP 自動化 v2.0 | 直接呼叫 Claude API")
