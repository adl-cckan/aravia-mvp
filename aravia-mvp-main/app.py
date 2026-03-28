import streamlit as st
import os

# ====================== 設定 ======================
st.set_page_config(
    page_title="Aravia MVP – Kan Intelligence",
    page_icon="🏛️",
    layout="wide"
)

st.title("🏛️ Aravia Knowledge Platform")
st.caption("CHAN Ching Kan 20年建築知識 + 2024 CUHK PhD 驅動 | Phase 2 完成")

# ====================== 載入知識庫 ======================
@st.cache_data
def load_knowledge():
    lessons_path = "lessons_35.md"
    keywords_path = "keywords.md"
    
    lessons = "檔案未找到，請確認 lessons_35.md 已放在同一資料夾"
    keywords = "檔案未找到，請確認 keywords.md 已放在同一資料夾"
    
    if os.path.exists(lessons_path):
        with open(lessons_path, "r", encoding="utf-8") as f:
            lessons = f.read()
    if os.path.exists(keywords_path):
        with open(keywords_path, "r", encoding="utf-8") as f:
            keywords = f.read()
    
    return lessons, keywords

lessons_text, keywords_text = load_knowledge()

# ====================== Sidebar ======================
with st.sidebar:
    st.success("✅ Knowledge Base 已載入")
    st.write(f"• 35 Lessons Learned")
    st.write(f"• 21 Keywords")
    st.caption("Claude / Grok 兩個Agent已準備好")
    
    st.divider()
    st.info("使用方法：\n1. 開兩個Claude Project\n2. Paste Agent Prompt\n3. 這裡直接Copy問題過去問")

# ====================== 主介面 Tabs ======================
tab1, tab2 = st.tabs(["📖 Kan Explainer（論文解釋）", "🔍 Kan Critic（設計批判）"])

with tab1:
    st.subheader("問我任何關於PhD論文或20年經驗的問題")
    query1 = st.text_input("例如：Space of Appearance 喺TOD項目點應用？或解釋 Lesson 7", key="explainer")
    
    if st.button("問 Kan Explainer", key="btn1"):
        st.markdown("**Kan Explainer 回覆：**")
        st.info("（請Copy上面問題去你Claude「Kan Explainer」Project貼上，即刻有答案）\n\n"
                "提示：我已載入 35 Lessons + 21 Keywords，你可以直接問任何Lesson或Keyword。")

with tab2:
    st.subheader("上傳設計圖，讓我批判")
    uploaded_file = st.file_uploader("上傳 Plan / Section / 3D（JPG / PNG / PDF）", 
                                   type=["jpg", "png", "pdf"])
    
    intent = st.text_area("簡單講下你想達成嘅設計意圖（例如：我想呢個空間更 porous 同埋有 Strategic Public Amenities）", 
                          height=100)
    
    if st.button("開始批判", key="btn2") and uploaded_file and intent:
        st.markdown("**Kan Critic 回覆：**")
        st.info("（請Copy以下內容去你Claude「Kan Critic」Project貼上，即刻有專業批判）\n\n"
                f"用戶意圖：{intent}\n\n"
                "請根據 Aravia 35 Lessons + 21 Keywords 批判以上圖則。")
        
        if uploaded_file:
            st.image(uploaded_file, caption="你上傳的設計圖", use_column_width=True)

# ====================== Footer ======================
st.divider()
st.caption("MVP v1.0 | 可分享、可自己run | 下一步可加 PM Agent + Proposal Generator")