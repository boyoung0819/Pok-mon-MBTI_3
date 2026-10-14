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

# 도감 스타일: 크림색 종이, 빨간 도감 테두리, 타입별 발광 효과
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Jua&family=Noto+Sans+KR:wght@400;500;700;900&display=swap');
    :root { --ink:#44352b; --paper:#fffaf0; --red:#d94d43; --gold:#f5ce64; }
    .stApp {
      background:
        radial-gradient(circle at 10% 2%, rgba(255,222,134,.42), transparent 24rem),
        linear-gradient(180deg,#fff8e8 0%,#fff0c9 100%);
      color:var(--ink); font-family:'Noto Sans KR',sans-serif;
    }
    h1,h2,h3,p,label,.stMarkdown,.stCaption { color:var(--ink) !important; }
    h1,h2,h3 { font-family:'Jua','Noto Sans KR',sans-serif !important; }
    h1 { font-size:clamp(2.1rem,6vw,3.1rem)!important; text-align:center; }
    h2 { font-size:clamp(1.45rem,4vw,2rem)!important; }
    p,li,label,.stCaption { font-size:1.08rem!important; line-height:1.75!important; }
    .dex-shell {
      border:5px solid #c9433b; border-radius:30px; padding:14px;
      background:linear-gradient(135deg,#e75d51,#c93832);
      box-shadow:0 10px 0 rgba(112,48,34,.15); margin-bottom:1.2rem;
    }
    .dex-top { display:flex; align-items:center; gap:10px; padding:3px 6px 13px; color:white; font-weight:900; }
    .dex-lens { width:31px; height:31px; border-radius:50%; background:radial-gradient(circle at 35% 30%,#fff 0 9%,#8fe8ff 11% 36%,#2786bc 60%,#16557d 100%); border:3px solid #f8eee0; box-shadow:0 0 0 3px #9c2925; }
    .dex-light { width:10px; height:10px; border-radius:50%; background:#ffdd69; border:1px solid #fff2bc; }
    .dex-screen {
      background:linear-gradient(145deg,#fffdf4,#f8f0d8); border:4px solid #8b2e2a;
      border-radius:20px; padding:1.1rem; text-align:center;
    }
    .hero-kicker { font-size:.95rem; letter-spacing:.12em; font-weight:900; color:#a23c34; }
    .hero-subtitle { font-size:1.08rem; line-height:1.8; }
    .panel {
      background:rgba(255,253,246,.92); border:2px solid #e6c66c; border-radius:20px;
      padding:1rem 1.1rem; margin:.6rem 0;
      box-shadow:0 5px 0 rgba(171,129,50,.10);
    }
    .panel-title { display:inline-block; background:#ffe7a0; border:1px solid #e4c45f;
      border-radius:9px; padding:.35rem .7rem; font-weight:900; margin-bottom:.5rem; }
    .dex-number { color:#8d7862; font-weight:900; letter-spacing:.08em; font-size:.9rem; }
    .type-pill { display:inline-block; padding:.32rem .75rem; border-radius:999px;
      background:#fff0b9; border:1px solid #e6c45d; color:#59421c; font-weight:900;
      margin:.18rem; font-size:.95rem; }
    .main-pokemon-name { font-size:1.65rem; font-weight:900; line-height:1.4; }
    .main-pokemon-name small { font-size:1rem; font-weight:700; }
    .reason-box { background:#fff3c9; border-left:5px solid #e4b83e; border-radius:12px;
      padding:.8rem 1rem; line-height:1.9; margin-top:.5rem; }
    .result-banner {
      position:relative; overflow:hidden; border-radius:18px; padding:1rem .7rem;
      margin:.4rem 0 1rem; text-align:center; border:2px solid var(--type-color,#f4c84e);
      background:linear-gradient(120deg,rgba(255,255,255,.9),var(--type-pale,#fff0b5));
      box-shadow:0 0 0 4px rgba(255,255,255,.55),0 6px 0 rgba(119,87,41,.10);
      animation: dex-pop .55s ease-out both;
    }
    .result-banner:before,.result-banner:after {
      content:"✦  ✧  ·  ✦"; position:absolute; color:var(--type-color,#f4c84e);
      font-size:1.6rem; opacity:.8; animation: sparkle-drift 2.5s ease-in-out infinite alternate;
    }
    .result-banner:before { top:8px; left:8px; }
    .result-banner:after { bottom:8px; right:8px; animation-delay:.4s; }
    .effect-symbol { display:inline-block; font-size:1.7rem; margin:0 .2rem;
      color:var(--type-color,#e4b83e); animation:type-bounce .9s ease-in-out infinite alternate; }
    .effect-symbol:nth-child(2) { animation-delay:.2s; }
    .effect-symbol:nth-child(3) { animation-delay:.4s; }
    @keyframes dex-pop { from { transform:scale(.94); opacity:.2; } to { transform:scale(1); opacity:1; } }
    @keyframes sparkle-drift { from { transform:translateY(0) rotate(-7deg); } to { transform:translateY(-5px) rotate(8deg); } }
    @keyframes type-bounce { from { transform:translateY(0) scale(.9); } to { transform:translateY(-5px) scale(1.12); } }
    .similar-card { background:#fffdf5; border:2px solid #ead38b; border-radius:17px;
      padding:.7rem; height:100%; text-align:center; }
    .similar-name { font-size:1rem; font-weight:900; line-height:1.5; }
    .similar-desc { font-size:.91rem; line-height:1.65; text-align:left; margin-top:.4rem; }
    div.stButton > button {
      border:2px solid #a9342e; border-radius:13px; color:#4e3024;
      background:linear-gradient(180deg,#ffe58e,#f8c94f); font-size:1.08rem;
      font-weight:900; min-height:3rem; box-shadow:0 4px 0 #c28a31;
    }
    div.stButton > button:hover { color:#4e3024; background:linear-gradient(180deg,#fff0b6,#ffda6b); }
    [data-testid="stImage"] img { filter:drop-shadow(0 5px 4px rgba(71,54,35,.12)); }
    footer,#MainMenu { visibility:hidden; }
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


MBTI_TRAITS = {
    "ISTJ": "현실적이고 책임감이 강해요. 계획을 세우고 약속과 규칙을 꾸준히 지키는 편이에요.",
    "ISFJ": "세심하고 다정해요. 주변 사람의 필요를 잘 알아차리고 안정적인 환경을 소중히 여겨요.",
    "INFJ": "통찰력과 공감 능력이 뛰어나요. 의미 있는 목표와 사람들의 마음을 깊이 생각해요.",
    "INTJ": "독립적이고 전략적이에요. 큰 그림을 보며 논리적으로 계획하고 개선하는 걸 좋아해요.",
    "ISTP": "관찰력이 좋고 실용적이에요. 직접 해 보며 원리를 파악하고 침착하게 해결책을 찾아요.",
    "ISFP": "감각적이고 온화해요. 자신만의 취향을 소중히 여기고 자유롭게 표현하는 편이에요.",
    "INFP": "상상력이 풍부하고 가치관이 뚜렷해요. 진심과 가능성을 중요하게 생각해요.",
    "INTP": "호기심이 많고 분석적이에요. 궁금한 주제의 원리와 개념을 깊이 탐구해요.",
    "ESTP": "활동적이고 대담해요. 현재 상황을 빠르게 읽고 직접 행동하며 경험하는 걸 좋아해요.",
    "ESFP": "밝고 친근해요. 사람들과 함께 즐거움을 나누고 생생한 경험을 즐기는 편이에요.",
    "ENFP": "열정적이고 창의적이에요. 새로운 가능성을 발견하고 사람들과 아이디어를 나누는 걸 좋아해요.",
    "ENTP": "재치 있고 아이디어가 풍부해요. 다양한 관점에서 생각하고 새로운 방법을 시험해 보는 편이에요.",
    "ESTJ": "체계적이고 추진력이 있어요. 목표를 분명히 정하고 일을 효율적으로 이끌어요.",
    "ESFJ": "협력적이고 사교적이에요. 사람들을 세심하게 챙기고 모두가 편안한 분위기를 만들어요.",
    "ENFJ": "공감과 소통에 강점이 있어요. 다른 사람의 장점을 발견하고 함께 성장하도록 응원해요.",
    "ENTJ": "결단력과 추진력이 있어요. 도전적인 목표를 세우고 방향을 정해 팀을 이끄는 편이에요.",
}

# [한글 이름, 영어 이름, 도감 번호, 타입, 포켓몬의 특징]
SIMILAR_POKEMON = {
    "ISTJ": [
        ["꼬부기","Squirtle",7,["물"],"차분하고 꾸준하게 성장하는 이미지"],
        ["모래두지","Sandshrew",27,["땅"],"단단한 방어와 성실한 인상"],
        ["아머까오","Corviknight",823,["비행","강철"],"믿음직하고 든든한 수호자"],
    ],
    "ISFJ": [
        ["이브이","Eevee",133,["노말"],"다양한 가능성과 친근한 매력"],
        ["토게틱","Togetic",176,["페어리","비행"],"행복을 나누는 다정한 이미지"],
        ["다부니","Audino",531,["노말"],"주변을 세심하게 살피는 돌봄"],
    ],
    "INFJ": [
        ["뮤","Mew",151,["에스퍼"],"신비롭고 깊은 가능성을 지닌 포켓몬"],
        ["에브이","Espeon",196,["에스퍼"],"예리한 감각과 차분한 분위기"],
        ["세레비","Celebi",251,["에스퍼","풀"],"생명과 미래를 떠올리게 하는 이미지"],
    ],
    "INTJ": [
        ["뮤츠","Mewtwo",150,["에스퍼"],"강력한 지능과 분석적인 이미지"],
        ["후딘","Alakazam",65,["에스퍼"],"뛰어난 지능과 빠른 판단력"],
        ["폴리곤Z","Porygon-Z",474,["노말"],"독특한 방식으로 진화한 연구 대상 같은 포켓몬"],
    ],
    "ISTP": [
        ["핫삼","Scizor",212,["벌레","강철"],"침착하고 정확한 움직임"],
        ["앱솔","Absol",359,["악"],"상황을 빠르게 감지하는 이미지"],
        ["엘레이드","Gallade",475,["에스퍼","격투"],"필요할 때 정확히 행동하는 전사"],
    ],
    "ISFP": [
        ["피카츄","Pikachu",25,["전기"],"개성 있고 친근한 매력"],
        ["리피아","Leafeon",470,["풀"],"자연스럽고 부드러운 분위기"],
        ["파비코리","Altaria",334,["드래곤","비행"],"포근하고 감성적인 이미지"],
    ],
    "INFP": [
        ["치코리타","Chikorita",152,["풀"],"순수하고 평화로운 분위기"],
        ["쉐이미","Shaymin",492,["풀"],"자연과 희망을 떠올리게 하는 이미지"],
        ["따라큐","Mimikyu",778,["고스트","페어리"],"자기만의 이야기를 가진 신비로운 포켓몬"],
    ],
    "INTP": [
        ["메타몽","Ditto",132,["노말"],"모습을 바꾸는 독특한 능력"],
        ["폴리곤","Porygon",137,["노말"],"디지털 세계와 과학적 호기심을 떠올리게 하는 포켓몬"],
        ["란쿨루스","Reuniclus",579,["에스퍼"],"복잡한 생각과 연구를 연상시키는 이미지"],
    ],
    "ESTP": [
        ["망나뇽","Dragonite",149,["드래곤","비행"],"힘과 활동성을 겸비한 포켓몬"],
        ["초염몽","Infernape",392,["불꽃","격투"],"빠르고 역동적인 에너지"],
        ["윈디","Arcanine",59,["불꽃"],"용감하고 거침없는 인상"],
    ],
    "ESFP": [
        ["아차모","Torchic",255,["불꽃"],"밝고 활기찬 에너지"],
        ["플러시","Plusle",311,["전기"],"응원과 즐거움을 전하는 이미지"],
        ["라이츄","Raichu",26,["전기"],"활발하고 에너지 넘치는 모습"],
    ],
    "ENFP": [
        ["비크티니","Victini",494,["에스퍼","불꽃"],"밝은 에너지와 가능성을 상징하는 포켓몬"],
        ["쉐이미","Shaymin",492,["풀"],"새로운 시작과 희망을 떠올리게 해요"],
        ["님피아","Sylveon",700,["페어리"],"따뜻하고 표현력 있는 매력"],
    ],
    "ENTP": [
        ["팬텀","Gengar",94,["고스트","독"],"장난기와 재치가 돋보이는 포켓몬"],
        ["깜까미","Sableye",302,["악","고스트"],"예측하기 어려운 독특한 매력"],
        ["칼라마네로","Malamar",687,["악","에스퍼"],"독특한 능력과 반전 매력"],
    ],
    "ESTJ": [
        ["괴력몬","Machamp",68,["격투"],"힘과 꾸준한 훈련을 떠올리게 해요"],
        ["아머까오","Corviknight",823,["비행","강철"],"강인하고 믿음직한 수호자"],
        ["번치코","Blaziken",257,["불꽃","격투"],"목표를 향해 나아가는 추진력"],
    ],
    "ESFJ": [
        ["픽시","Clefable",36,["페어리"],"친근하고 다정한 분위기"],
        ["럭키","Chansey",113,["노말"],"다른 포켓몬을 돌보는 이미지"],
        ["삐","Cleffa",173,["페어리"],"사랑스럽고 친근한 분위기로 다가가는 포켓몬"],
    ],
    "ENFJ": [
        ["가디","Growlithe",58,["불꽃"],"친구를 지키는 충직한 이미지"],
        ["비조도","Mienshao",620,["격투"],"수련과 성장을 떠올리게 하는 모습"],
        ["가디안","Gardevoir",282,["에스퍼","페어리"],"소중한 존재를 지키려는 이미지"],
    ],
    "ENTJ": [
        ["마기라스","Tyranitar",248,["바위","악"],"압도적인 존재감과 힘"],
        ["엘레이드","Gallade",475,["에스퍼","격투"],"결단력 있게 움직이는 전사"],
        ["메타그로스","Metagross",376,["강철","에스퍼"],"전략적이고 지능적인 이미지"],
    ],
}

TYPE_STYLE = {
    "물": ("#399be0", "#d9f0ff", "💧"),
    "불꽃": ("#f07838", "#ffe0c5", "🔥"),
    "전기": ("#d9a900", "#fff1a6", "⚡"),
    "풀": ("#54a85a", "#dff5d7", "🍃"),
    "얼음": ("#5dbecb", "#dcfaff", "❄️"),
    "격투": ("#cf6550", "#ffe0d8", "💥"),
    "독": ("#9b69c6", "#eedcff", "🫧"),
    "땅": ("#b28b52", "#f1e1c5", "🪨"),
    "비행": ("#7194d8", "#e1eaff", "🪽"),
    "에스퍼": ("#cf6a9e", "#ffe0f0", "✨"),
    "벌레": ("#8aa33c", "#edf5c7", "🌿"),
    "바위": ("#a38b66", "#eee3d2", "🪨"),
    "고스트": ("#8170bd", "#e9e3ff", "👻"),
    "드래곤": ("#6c78d8", "#e2e5ff", "🐉"),
    "악": ("#786a68", "#e8dfdd", "🌑"),
    "강철": ("#7b9baa", "#e0edf2", "⚙️"),
    "페어리": ("#d987b2", "#ffe5f2", "🌸"),
    "노말": ("#a79c87", "#eee9df", "⭐"),
}

MBTI_TYPES = list(POKEMON.keys())

# Streamlit의 rerun 사이에 선택값 유지
if "selected_mbti" not in st.session_state:
    st.session_state.selected_mbti = None
if "celebrate" not in st.session_state:
    st.session_state.celebrate = False

st.markdown(
    """
    <div class="dex-shell">
      <div class="dex-top">
        <span class="dex-lens"></span><span style="font-size:1.15rem">POKÉDEX</span>
        <span class="dex-light"></span><span class="dex-light" style="background:#9de0a3"></span>
        <span style="margin-left:auto;font-size:.8rem">MBTI FIELD GUIDE</span>
      </div>
      <div class="dex-screen">
        <div class="hero-kicker">PERSONALITY × POKÉMON</div>
        <h1>나의 단짝 포켓몬 도감</h1>
        <div class="hero-subtitle">MBTI를 선택하면 나와 닮은 포켓몬을 찾아요.<br>도감에서 나만의 파트너를 확인해 보세요!</div>
        <div style="font-size:1.8rem;margin-top:.5rem">📕 ✨ 🔎</div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("## 🔎 트레이너의 MBTI 등록")
st.caption("16가지 유형 중 하나를 선택해 도감을 열어 보세요.")

for start in range(0, len(MBTI_TYPES), 4):
    cols = st.columns(4, gap="small")
    for col, mbti in zip(cols, MBTI_TYPES[start:start + 4]):
        with col:
            label = f"✓ {mbti}" if st.session_state.selected_mbti == mbti else mbti
            if st.button(label, key=f"mbti_{mbti}", use_container_width=True):
                st.session_state.selected_mbti = mbti
                st.session_state.celebrate = True
                st.rerun()

selected = st.session_state.selected_mbti

if selected:
    data = POKEMON[selected]
    main_type = data["types"][0]
    type_color, type_pale, type_symbol = TYPE_STYLE.get(main_type, ("#e4b83e", "#fff0b5", "✨"))
    st.markdown("---")

    st.markdown(
        f"""
        <div class="result-banner" style="--type-color:{type_color};--type-pale:{type_pale}">
          <div class="dex-number">NO. {list(POKEMON.keys()).index(selected)+1:03d} · PERSONALITY SCAN COMPLETE</div>
          <div style="font-size:1.15rem;font-weight:900;margin:.3rem 0">🎉 {selected} 트레이너의 단짝 발견!</div>
          <div><span class="effect-symbol">{type_symbol}</span><span class="effect-symbol">✦</span><span class="effect-symbol">{type_symbol}</span></div>
          <div style="font-size:.95rem">타입의 기운이 반짝이며 단짝을 축하해요!</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.session_state.celebrate = False

    st.markdown(f"<div class='panel'><div class='dex-number'>MAIN PARTNER · NO. {data['id']:03d}</div></div>", unsafe_allow_html=True)
    with st.container(border=True):
        st.image(
            f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{data['id']}.png",
            width=260,
        )
        st.markdown(
            f"<div class='main-pokemon-name'>{data['name']} <small>({data['english']})</small></div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            " ".join([f"<span class='type-pill'>{TYPE_STYLE.get(t, ('#aaa','#eee','🔹'))[2]} {t} 타입</span>" for t in data["types"]]),
            unsafe_allow_html=True,
        )
        st.markdown("<div class='panel-title'>📖 포켓몬 특징</div>", unsafe_allow_html=True)
        st.write(data["traits"])
        st.markdown("<div class='panel-title'>💛 이 MBTI와 잘 어울리는 이유</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='reason-box'>{data['reason'].replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)

    st.markdown("## 🧠 MBTI 성격 도감")
    with st.container(border=True):
        st.markdown(f"<div class='panel-title'>유형 코드: {selected}</div>", unsafe_allow_html=True)
        st.write(MBTI_TRAITS[selected])
        st.caption("MBTI 설명은 일반적인 성향을 재미로 정리한 것이며, 사람마다 다를 수 있어요.")

    st.markdown("## 🔍 나와 비슷한 포켓몬 3마리")
    st.caption("메인 단짝과는 다른 포켓몬 중에서, 성향이나 분위기가 닮은 친구들을 골랐어요.")
    similar_cols = st.columns(3, gap="small")
    for col, pokemon in zip(similar_cols, SIMILAR_POKEMON[selected]):
        name, english, pokedex_id, types, feature = pokemon
        with col:
            with st.container(border=True):
                st.markdown(f"<div class='dex-number'>NO. {pokedex_id:03d}</div>", unsafe_allow_html=True)
                st.image(
                    f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{pokedex_id}.png",
                    use_container_width=True,
                )
                st.markdown(f"<div class='similar-name'>{name}<br><span style='font-weight:500'>({english})</span></div>", unsafe_allow_html=True)
                st.markdown(
                    " ".join([f"<span class='type-pill'>{t}</span>" for t in types]),
                    unsafe_allow_html=True,
                )
                st.markdown(f"<div class='similar-desc'><b>특징</b><br>{feature}</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(
        f"<div class='panel' style='text-align:center'><div class='panel-title'>🤝 궁합 참고</div><br><b>{selected}</b>와 잘 어울리는 유형으로는 <b>{data['match']}</b>를 골랐어요.<br><span style='font-size:.9rem'>MBTI 궁합과 포켓몬 연결은 재미를 위한 창작 설정이에요.</span></div>",
        unsafe_allow_html=True,
    )
    if st.button("🔄 다른 MBTI로 도감 다시 열기", use_container_width=True):
        st.session_state.selected_mbti = None
        st.session_state.celebrate = False
        st.rerun()
else:
    st.info("👆 MBTI 버튼을 누르면 포켓몬 도감이 열려요!")

st.markdown(
    """
    <div style="text-align:center;padding:1.2rem 0 .5rem;color:#8a7047;line-height:1.8">
      📕 나만의 포켓몬 도감 · 트레이너 기록 완료<br>
      <span style="font-size:.85rem">포켓몬 이미지는 PokeAPI 공식 아트워크 저장소에서 불러옵니다.</span>
    </div>
    """,
    unsafe_allow_html=True,
)
