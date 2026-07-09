import streamlit as st
import uuid

# 페이지 기본 설정
st.set_page_config(page_title="분실물 보관소", page_icon="🔍", layout="centered")

# 데이터 저장을 위한 session_state 초기화
if 'lost_items' not in st.session_state:
    st.session_state.lost_items = []

# 메인 타이틀 및 총 분실물 개수 표시
st.title("🔍 분실물 보관소 앱")
st.info(f"📦 현재 보관 중인 분실물: **{len(st.session_state.lost_items)}개**")

# 탭을 생성하여 화면을 깔끔하게 분리
tab1, tab2 = st.tabs(["📋 검색 및 목록", "➕ 새 분실물 등록"])

# ----------------------------------------
# 탭 2: 새 분실물 등록
# ----------------------------------------
with tab2:
    st.subheader("새 분실물 등록하기")
    with st.form("register_form", clear_on_submit=True):
        name = st.text_input("분실물 이름 (예: 검은색 가죽 지갑, 에어팟)")
        desc = st.text_area("상세 설명 (예: 신분증 들어있음, 오른쪽 유닛만 있음)")
        location = st.text_input("보관 장소 (예: 1층 안내데스크, 교무실)")
        
        submit_button = st.form_submit_button("등록하기", type="primary")
        
        if submit_button:
            if name.strip() and location.strip():
                # 고유 ID 생성 (삭제 시 정확한 항목을 찾기 위함)
                new_item = {
                    "id": str(uuid.uuid4()),
                    "name": name,
                    "desc": desc,
                    "location": location
                }
                st.session_state.lost_items.append(new_item)
                st.success(f"'{name}'이(가) 성공적으로 등록되었습니다!")
                st.rerun() # 화면 새로고침하여 개수 업데이트
            else:
                st.warning("분실물 이름과 보관 장소는 필수 입력 사항입니다.")

# ----------------------------------------
# 탭 1: 분실물 검색, 목록 보기 및 삭제
# ----------------------------------------
with tab1:
    st.subheader("분실물 검색 및 목록")
    
    # 검색창
    search_query = st.text_input("🔍 찾으시는 분실물 이름을 입력하세요", placeholder="검색어 입력...")
    
    st.divider()
    
    # 검색어에 맞춰 목록 필터링
    filtered_items = [
        item for item in st.session_state.lost_items 
        if search_query.lower() in item['name'].lower()
    ]
    
    if not filtered_items:
        if search_query:
            st.write("검색 결과가 없습니다.")
        else:
            st.write("현재 등록된 분실물이 없습니다.")
    else:
        # 필터링된 분실물 목록 출력
        for item in filtered_items:
            # expander를 사용해 클릭하면 상세 내용이 열리도록 디자인
            with st.expander(f"📌 {item['name']} (보관장소: {item['location']})"):
                st.write(f"**상세 설명:** {item['desc']}")
                st.write(f"**보관 장소:** {item['location']}")
                
                # 삭제 버튼 (주인이 찾아간 경우)
                if st.button("✅ 주인이 찾아감 (삭제)", key=item['id']):
                    # 해당 ID를 가진 항목을 리스트에서 제외
                    st.session_state.lost_items = [
                        i for i in st.session_state.lost_items if i['id'] != item['id']
                    ]
                    st.rerun() # 화면 새로고침
