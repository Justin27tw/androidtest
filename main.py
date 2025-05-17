import streamlit as st
import pandas as pd
import random

# 載入資料
@st.cache_data
def load_questions():
    df = pd.read_excel("安卓9_330題庫1111019.xlsx")
    df = df.dropna(subset=["題目", "答案"])  # 去除空題目
    return df

df = load_questions()

st.title("隨機選擇題測驗")

# 使用者選擇題數
num_questions = st.number_input("請輸入想要作答的題數", min_value=1, max_value=len(df), value=5)

if st.button("開始出題"):
    st.session_state["quiz_started"] = True
    st.session_state["questions"] = df.sample(n=num_questions).reset_index(drop=True)
    st.session_state["answers"] = {}

if st.session_state.get("quiz_started", False):
    questions = st.session_state["questions"]
    
    with st.form("quiz_form"):
        for i, row in questions.iterrows():
            st.markdown(f"**第{i+1}題：{row['題目']}**")
            
            options = []
            for opt in ["A", "B", "C", "D"]:
                if pd.notna(row.get(opt)):
                    options.append(f"{opt}. {row[opt]}")
            
            correct_answer = str(row["答案"]).strip().upper()
            is_multiple = len(correct_answer) > 1
            
            key = f"q{i}"
            if is_multiple:
                selected = st.multiselect("請選擇（複選）", options, key=key)
            else:
                selected = st.radio("請選擇（單選）", options, key=key)
            
            st.session_state["answers"][key] = selected
        
        submitted = st.form_submit_button("交卷")
    
    if submitted:
        st.subheader("成績與解析")
        score = 0
        for i, row in questions.iterrows():
            st.markdown(f"**第{i+1}題：{row['題目']}**")
            correct = str(row["答案"]).strip().upper()
            correct_options = [f"{c}. {row[c]}" for c in correct]
            user_input = st.session_state["answers"].get(f"q{i}", [])

            if isinstance(user_input, str):
                user_input = [user_input]

            if set(user_input) == set(correct_options):
                st.success("✔️ 答對")
                score += 1
            else:
                st.error(f"❌ 答錯，正確答案為：{', '.join(correct_options)}")

        st.info(f"🎯 總分：{score} / {num_questions}")