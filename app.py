import streamlit as st
from modules.database import DBManager
import modules.components as ui

st.set_page_config(page_title="SQLite Pro Manager", layout="wide")

# 1. 파일 업로드 로직
uploaded_file = st.sidebar.file_uploader("DB 파일 업로드", type=["db", "sqlite"])

if uploaded_file:
    temp_path = "managed_user_db.db"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # DB 초기화
    db = DBManager(temp_path)
    
    # 2. 사이드바 SQL 실행기 렌더링
    query, run_clicked = ui.sidebar_query_editor()
    if run_clicked:
        success, msg = db.run_script(query)
        if success: st.sidebar.success("✅ 반영 완료")
        else: st.sidebar.error(f"❌ 에러: {msg}")
        st.rerun()

    # 3. 메인 콘텐츠
    st.title("🗂️ Advanced SQLite Manager")
    
    # 상단 요약
    tables = db.get_objects('table')
    views = db.get_objects('view')
    ui.display_stats(tables, views)

    # 데이터 뷰어
    obj_type, selected_name = ui.data_viewer_ui(tables, views)
    
    if selected_name:
        df = db.fetch_dataframe(selected_name)
        st.dataframe(df, use_container_width=True)
        
        # [확장 포인트] 여기서 분석 버튼 등을 추가하기 쉬움
        if st.button(f"{selected_name} 기반 차트 생성"):
            st.info("시각화 기능은 modules/analysis.py에서 처리할 예정입니다.")

    db.close()
else:
    st.title("🚀 Welcome to SQLite Manager")
    st.info("시작하려면 왼쪽에서 DB 파일을 업로드하세요.")
