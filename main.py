import random
import streamlit as st
import streamlit.components.v1 as components

# ------------------------------------------------------------
# MBTI 단짝 포켓몬 찾기 - 한 파일로 실행하는 Streamlit 앱
# 이미지 출처: PokeAPI 공식 아트워크 저장소
# ------------------------------------------------------------

st.set_page_config(
    page_title="MBTI 단짝 포켓몬 찾기",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# 따뜻한 크림·노란색 테마와 큰 글씨
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Jua&family=Noto+Sans+KR:wght@400;500;700;900&display=swap');

    :root {
        --cream: #fff9e9;
        --yellow: #ffe08a;
        --yellow-deep: #f6c84b;
        --brown: #5b4427;
        --orange: #f29f45;
        --card: #fffdf6;
    }
    .stApp {
        background:
          radial-gradient(circle at 10% 4%, rgba(255,224,138,.45), transparent 24rem),
          linear-gradient(180deg, #fff9e9 0%, #fff5d7 100%);
        color: var(--brown);
        font-family: 'Noto Sans KR', sans-serif;
    }
    h1, h2, h3, p, label, .stMarkdown, .stCaption {
        color: var(--brown) !important;
    }
    h1, h2, h3 { font-family: 'Jua', 'Noto Sans KR', sans-serif !important; }
    h1 { font-size: clamp(2.2rem, 6vw, 3.3rem) !important; text-align: center; }
    h2 { font-size: clamp(1.55rem, 4vw, 2rem) !important; }
    p, li, label, .stSelectbox div, .stRadio label { font-size: 1.12rem !important; }
    .hero {
        text-align: center;
        padding: 1.2rem 1rem 1.5rem;
        background: rgba(255,255,255,.62);
        border: 2px solid #f8d978;
        border-radius: 28px;
        box-shadow: 0 8px 0 rgba(219, 171, 62, .15);
        margin-bottom: 1.25rem;
    }
    .hero .sparkle { font-size: 2.4rem; }
    .hero .subtitle { font-size: 1.15rem; line-height: 1.8; }
    .pokemon-card {
        background: var(--card);
        border: 2px solid #f6d777;
        border-radius: 26px;
        padding: 1.25rem;
        text-align: center;
        box-shadow: 0 8px 0 rgba(219, 171, 62, .15);
        margin: .5rem 0 1rem;
    }
    .pokemon-card img {
        width: min(100%, 260px);
        height: auto;
        image-rendering: auto;
        filter: drop-shadow(0 7px 4px rgba(91,68,39,.12));
    }
    .type-pill {
        display: inline-block;
        background: #ffedb5;
        color: #694b18;
        border: 1px solid #f0ca63;
        padding: .35rem .85rem;
        border-radius: 999px;
        font-weight: 800;
        margin: .2rem;
        font-size: 1rem;
    }
    .reason-box {
        background: #fff4c9;
        border-left: 6px solid #f3bf35;
        padding: 1rem 1.15rem;
        border-radius: 14px;
        line-height: 1.9;
        font-size: 1.08rem;
        margin-top: .8rem;
    }
    .section-label {
        background: #ffe7a1;
        border-radius: 14px;
        padding: .55rem .8rem;
        font-weight: 900;
        display: inline-block;
        margin: .4rem 0;
    }
    div.stButton > button {
        border: 0;
        border-radius: 16px;
        background: linear-gradient(180deg, #ffdf79, #ffca4b);
        color: #573d13;
        font-size: 1.15rem;
        font-weight: 900;
        min-height: 3.2rem;
        box-shadow: 0 5px 0 #e6ae32;
        transition: transform .12s ease, box-shadow .12s ease;
    }
    div.stButton > button:hover {
        background: linear-gradient(180deg, #ffe99d, #ffd45e);
        transform: translateY(-2px);
        box-shadow: 0 7px 0 #e6ae32;
        color: #573d13;
    }
    div.stButton > button:active { transform: translateY(2px); box-shadow: 0 2px 0 #e6ae32; }
    [data-testid="stSelectbox"] > label { font-size: 1.2rem !important; font-weight: 900 !important; }
    [data-testid="stAlert"] { border-radius: 16px; }
    footer { visibility: hidden; }
    #MainMenu { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)

# 포켓몬 정보: PokeAPI official artwork 번호를 이용해 이미지 표시
POKEMON = {
    "ISTJ": {
        "match": "ESFP",
        "name": "거북왕", "english": "Blastoise", "id": 9,
        "types": ["물"], "traits": "책임감이 강하고 차분하며, 맡은 일을 끝까지 해내는 든든한 타입이에요.",
        "reason": "거북왕은 침착하고 단단한 모습으로 믿음직한 ISTJ와 잘 어울려요.\n차근차근 상황을 살피고 팀을 지켜 주는 든든한 단짝이 될 수 있어요."
    },
    "ISFJ": {
        "match": "ESTP",
        "name": "럭키", "english": "Chansey", "id": 113,
        "types": ["노말"], "traits": "주변을 세심하게 살피고, 소중한 사람을 따뜻하게 챙기는 타입이에요.",
        "reason": "럭키는 다른 포켓몬을 보살피는 다정한 이미지가 있어요.\n작은 변화도 잘 알아차리고 친구를 챙기는 ISFJ의 마음과 닮았어요."
    },
    "INFJ": {
        "match": "ENFP",
        "name": "가디안", "english": "Gardevoir", "id": 282,
        "types": ["에스퍼", "페어리"], "traits": "의미와 가치를 중요하게 생각하고, 다른 사람의 마음을 깊이 이해하려는 타입이에요.",
        "reason": "가디안은 소중한 존재를 지키려는 마음을 상징하는 포켓몬이에요.\n사람의 감정을 이해하고 진심으로 돕고 싶어 하는 INFJ와 잘 어울려요."
    },
    "INTJ": {
        "match": "ENTP",
        "name": "메타그로스", "english": "Metagross", "id": 376,
        "types": ["강철", "에스퍼"], "traits": "큰 그림을 보고 전략을 세우며, 논리적으로 문제를 해결하는 데 강점이 있는 타입이에요.",
        "reason": "메타그로스는 뛰어난 지능과 전략적인 이미지가 특징이에요.\n계획을 세우고 복잡한 문제를 분석하는 INTJ의 성향과 잘 맞아요."
    },
    "ISTP": {
        "match": "ESFJ",
        "name": "루카리오", "english": "Lucario", "id": 448,
        "types": ["격투", "강철"], "traits": "직접 해 보며 원리를 파악하고, 침착하게 해결 방법을 찾는 실용적인 타입이에요.",
        "reason": "루카리오는 상황을 빠르게 파악하고 행동하는 모습이 매력적이에요.\n말보다 행동으로 문제를 해결하는 ISTP의 실용적인 면과 닮았어요."
    },
    "ISFP": {
        "match": "ESTJ",
        "name": "님피아", "english": "Sylveon", "id": 700,
        "types": ["페어리"], "traits": "자신만의 취향과 감각을 소중히 여기고, 부드럽고 자유롭게 표현하는 타입이에요.",
        "reason": "님피아는 섬세하고 다정한 분위기를 가진 포켓몬이에요.\n자신만의 감각을 지키면서 주변과 조화를 이루는 ISFP와 잘 어울려요."
    },
    "INFP": {
        "match": "ENFJ",
        "name": "세레비", "english": "Celebi", "id": 251,
        "types": ["에스퍼", "풀"], "traits": "상상력이 풍부하고 자신만의 가치관을 중요하게 여기며, 진심을 담아 행동하는 타입이에요.",
        "reason": "세레비는 자연과 생명을 떠올리게 하는 신비로운 포켓몬이에요.\n이상과 가능성을 소중히 여기는 INFP의 상상력과 따뜻한 마음에 어울려요."
    },
    "INTP": {
        "match": "ENTJ",
        "name": "폴리곤2", "english": "Porygon2", "id": 233,
        "types": ["노말"], "traits": "궁금한 것을 깊이 파고들고, 원리와 개념을 분석하는 것을 좋아하는 타입이에요.",
        "reason": "폴리곤2는 인공적으로 만들어진 독특한 포켓몬이에요.\n새로운 개념을 탐구하고 논리적으로 생각하는 INTP의 호기심과 잘 맞아요."
    },
    "ESTP": {
        "match": "ISFJ",
        "name": "리자몽", "english": "Charizard", "id": 6,
        "types": ["불꽃", "비행"], "traits": "에너지가 넘치고 행동이 빠르며, 눈앞의 상황에 적극적으로 뛰어드는 타입이에요.",
        "reason": "리자몽은 대담하고 역동적인 에너지가 돋보여요.\n기회를 빠르게 포착하고 직접 부딪혀 보는 ESTP의 활동적인 면과 잘 어울려요."
    },
    "ESFP": {
        "match": "ISTJ",
        "name": "피카츄", "english": "Pikachu", "id": 25,
        "types": ["전기"], "traits": "밝고 친근하며, 사람들과 함께 즐거운 순간을 만드는 데 능한 타입이에요.",
        "reason": "피카츄는 활기차고 친근해서 함께 있으면 분위기가 밝아지는 포켓몬이에요.\n사람들과 즐거움을 나누고 순간을 즐기는 ESFP와 찰떡궁합이에요."
    },
    "ENFP": {
        "match": "INFJ",
        "name": "토게키스", "english": "Togekiss", "id": 468,
        "types": ["페어리", "비행"], "traits": "새로운 가능성을 발견하는 것을 좋아하고, 열정과 호기심으로 주변에 활기를 주는 타입이에요.",
        "reason": "토게키스는 행복과 좋은 기운을 전해 주는 이미지가 있어요.\n새로운 아이디어를 나누고 주변 사람을 응원하는 ENFP와 잘 어울려요."
    },
    "ENTP": {
        "match": "INTJ",
        "name": "조로아크", "english": "Zoroark", "id": 571,
        "types": ["악"], "traits": "기발한 아이디어를 내고 여러 관점에서 생각하며, 토론과 새로운 시도를 즐기는 타입이에요.",
        "reason": "조로아크는 환상을 활용하는 영리하고 재치 있는 포켓몬이에요.\n틀에 얽매이지 않고 색다른 가능성을 찾는 ENTP의 창의성과 닮았어요."
    },
    "ESTJ": {
        "match": "ISFP",
        "name": "윈디", "english": "Arcanine", "id": 59,
        "types": ["불꽃"], "traits": "목표를 정하고 체계적으로 추진하며, 팀을 이끌고 일을 정리하는 데 강점이 있는 타입이에요.",
        "reason": "윈디는 용감하고 믿음직한 이미지가 돋보이는 포켓몬이에요.\n목표를 향해 꾸준히 나아가고 주변을 이끄는 ESTJ와 잘 어울려요."
    },
    "ESFJ": {
        "match": "ISTP",
        "name": "푸린", "english": "Jigglypuff", "id": 39,
        "types": ["노말", "페어리"], "traits": "사람들과 어울리는 것을 좋아하고, 분위기를 살피며 모두가 편안하도록 돕는 타입이에요.",
        "reason": "푸린은 노래로 주변을 즐겁게 하려는 사랑스러운 포켓몬이에요.\n사람들을 챙기고 함께하는 분위기를 중요하게 생각하는 ESFJ와 잘 맞아요."
    },
    "ENFJ": {
        "match": "INFP",
        "name": "밀로틱", "english": "Milotic", "id": 350,
        "types": ["물"], "traits": "사람들의 장점을 발견하고 응원하며, 함께 목표를 이루도록 이끄는 타입이에요.",
        "reason": "밀로틱은 아름답고 차분한 분위기로 주변을 안정시키는 포켓몬이에요.\n다른 사람에게 용기를 주고 조화로운 관계를 만들려는 ENFJ와 어울려요."
    },
    "ENTJ": {
        "match": "INTP",
        "name": "갸라도스", "english": "Gyarados", "id": 130,
        "types": ["물", "비행"], "traits": "결단력이 있고 도전적인 목표를 세우며, 큰 흐름을 주도하는 데 강점이 있는 타입이에요.",
        "reason": "갸라도스는 강력한 에너지와 추진력을 상징하는 포켓몬이에요.\n어려운 목표에도 과감하게 도전하고 방향을 이끄는 ENTJ와 잘 어울려요."
    },
}

MBTI_TYPES = list(POKEMON.keys())

# Streamlit의 rerun 사이에 선택값 유지
if "selected_mbti" not in st.session_state:
    st.session_state.selected_mbti = None
if "celebrate" not in st.session_state:
    st.session_state.celebrate = False

st.markdown(
    """
    <div class="hero">
      <div class="sparkle">✨ ⚡ 🌼 ✨</div>
      <h1>MBTI 단짝 포켓몬 찾기!</h1>
      <div class="subtitle">
        내 성격과 잘 어울리는 포켓몬은 누구일까요?<br>
        MBTI를 선택하고 나만의 단짝을 만나 보세요!
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("## 🌟 나의 MBTI를 골라 주세요")
st.caption("아래에서 하나만 선택하면 포켓몬을 찾아드려요.")

# 4열 버튼 그리드
for start in range(0, len(MBTI_TYPES), 4):
    cols = st.columns(4, gap="small")
    for col, mbti in zip(cols, MBTI_TYPES[start:start + 4]):
        with col:
            if st.button(mbti, key=f"mbti_{mbti}", use_container_width=True):
                st.session_state.selected_mbti = mbti
                st.session_state.celebrate = True
                st.rerun()

selected = st.session_state.selected_mbti

if selected:
    data = POKEMON[selected]
    st.markdown("---")
    if st.session_state.celebrate:
        st.balloons()
        st.snow()
        st.session_state.celebrate = False

    st.markdown(
        f"<h2 style='text-align:center'>🎉 {selected}의 단짝 포켓몬을 찾았어요! 🎉</h2>",
        unsafe_allow_html=True,
    )

    image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{data['id']}.png"

    st.markdown("<div class='pokemon-card'>", unsafe_allow_html=True)
    st.image(image_url, width=260)
    st.markdown(f"<h2>{data['name']} <span style='font-size:1.2rem'>({data['english']})</span></h2>", unsafe_allow_html=True)
    type_html = " ".join([f"<span class='type-pill'>🔸 {t} 타입</span>" for t in data["types"]])
    st.markdown(type_html, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-label'>💛 포켓몬의 특징</div>", unsafe_allow_html=True)
    st.markdown(data["traits"])

    st.markdown("<div class='section-label'>🤝 왜 잘 어울릴까요?</div>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='reason-box'>{data['reason'].replace(chr(10), '<br>')}</div>",
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown(
        f"<h3 style='text-align:center'>💫 궁합이 좋은 MBTI: {data['match']}</h3>",
        unsafe_allow_html=True,
    )
    st.caption("MBTI 궁합과 포켓몬 연결은 재미를 위한 창작 설정이에요!")

    if st.button("🔄 다른 MBTI로 다시 찾아보기", use_container_width=True):
        st.session_state.selected_mbti = None
        st.session_state.celebrate = False
        st.rerun()
else:
    st.info("👇 MBTI 버튼을 누르면 결과가 여기에 나타나요!")

st.markdown(
    """
    <div style="text-align:center; padding:1.2rem 0 .5rem; color:#8a7047; line-height:1.8">
      🌼 포켓몬과 함께 즐거운 하루! 🌼<br>
      <span style="font-size:.9rem">포켓몬 이미지는 PokeAPI 공식 아트워크 이미지 URL을 사용합니다.</span>
    </div>
    """,
    unsafe_allow_html=True,
)
