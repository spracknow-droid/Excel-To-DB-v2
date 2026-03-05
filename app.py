import streamlit as st
from modules.database import DBManager
import modules.components as ui

st.set_page_config(page_title="SQLite Pro v2", layout="wide")

# 세션 상태로 DB 경로 고정 (WebSocket 에러 방지)
if 'db_path' not in st.session_state:
    st.session_state.db_path = None

st.title("🛡️ SQLite Viewer v2")

uploaded_file = st.sidebar.file_uploader("DB 파일 업로드", type=["db", "sqlite"])

if uploaded_file:
    # 1. 파일 세팅
    if st.session_state.db_path is None:
        temp_path = "managed_db.db"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.session_state.db_path = temp_path
    
    db = DBManager(st.session_state.db_path)

    # 2. 사이드바 UI 렌더링
    query, run_clicked = ui.render_query_editor()
    if run_clicked:
        success, msg = db.run_script(query)
        if success:
            st.sidebar.success("✅ 반영 완료")
            st.rerun()
        else:
            st.sidebar.error(f"❌ 오류: {msg}")

    # 3. 메인 현황판
    tables = db.get_objects('table')
    views = db.get_objects('view')
    ui.render_stats(tables, views)

    # 4. 데이터 뷰어
    obj_type, selected_obj = ui.render_data_browser(tables, views)
    if selected_obj:
        try:
            df = db.fetch_data(selected_obj)
            st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(f"데이터 로드 실패: {e}")

    # 5. 다운로드 버튼
    st.sidebar.divider()
    with open(st.session_state.db_path, "rb") as f:
        st.sidebar.download_button("💾 수정한 DB 저장", f, file_name="updated.db")

else:
    st.info("👈 사이드바에서 파일을 업로드하면 모듈형 시스템이 가동됩니다.")
