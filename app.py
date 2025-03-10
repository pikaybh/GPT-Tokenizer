import streamlit as st
from utils import num_tokens_from_string, calc_input, calc_output, calc_cost
from models import gpt_model_dict  # 모델 정보 불러오기

# 사용할 LLM 모델 목록 (GPT 모델 & Embedding 모델 구분)
GPT_MODELS = [name for name, model in gpt_model_dict.items() if model.pricing.input_per_1M_tokens is not None]
EMBEDDING_MODELS = [name for name, model in gpt_model_dict.items() if model.pricing.cost_per_1M_tokens is not None]

# Streamlit UI 구성
st.title("🪙 Token Cost Calculator")

# 초기 입력 필드 리스트
if "input_fields" not in st.session_state:
    st.session_state.input_fields = [{"text": "", "llm": "gpt-4o", "type": "Input"}]  # 기본 1개

# 입력 필드 추가 함수
def add_input():
    st.session_state.input_fields.append({"text": "", "llm": "gpt-4o", "type": "Input"})

# 입력 필드 삭제 함수
def remove_input(index):
    if len(st.session_state.input_fields) > 1:
        st.session_state.input_fields.pop(index)

# 입력 필드 UI
st.subheader("📝 입력 필드")
for index, field in enumerate(st.session_state.input_fields):
    col1, col2, col3 = st.columns([4.5, 1.5, 0.5])

    with col1:
        st.session_state.input_fields[index]["text"] = st.text_area(
            f"입력 {index + 1}", field["text"], key=f"text_{index}", height=128
        )

    with col2:
        selected_llm = st.selectbox(
            "모델 선택",
            GPT_MODELS + EMBEDDING_MODELS,
            index=(GPT_MODELS + EMBEDDING_MODELS).index(field["llm"]),
            key=f"llm_{index}",
        )
        st.session_state.input_fields[index]["llm"] = selected_llm

        # 선택된 모델이 GPT 모델인지, Embedding 모델인지 판별
        if selected_llm in GPT_MODELS:
            valid_types = ["Input", "Output"]
        else:
            valid_types = ["Cost"]

        # 기존 선택이 유효하지 않다면, 기본값 변경
        if field["type"] not in valid_types:
            st.session_state.input_fields[index]["type"] = valid_types[0]

        st.session_state.input_fields[index]["type"] = st.selectbox(
            "유형 선택",
            valid_types,
            index=valid_types.index(st.session_state.input_fields[index]["type"]),
            key=f"type_{index}",
        )

    with col3:
        if st.button("❌", key=f"remove_{index}"):
            remove_input(index)
            st.rerun()

st.button("➕ 추가", on_click=add_input)

# 비용 계산
st.subheader("💰 비용 계산")
total_cost: float = 0.0

for field in st.session_state.input_fields:
    text = field["text"]
    model = field["llm"]
    input_type = field["type"]

    if input_type == "Input":
        total_cost += calc_input(text, model)
    elif input_type == "Output":
        total_cost += calc_output(text, model)
    elif input_type == "Cost":
        total_cost += calc_cost(text, model)

# 소수점 조절 옵션 추가
if st.toggle("🔍 소숫점 끝까지 보기", False):
    st.markdown(f"### 총 비용: **${total_cost:,}**")
else:
    st.markdown(f"### 총 비용: **${total_cost:,.2f}**")
