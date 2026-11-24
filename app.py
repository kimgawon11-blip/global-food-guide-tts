import streamlit as st
from gtts import gTTS
import io

# 1. 리스트 및 데이터 구조 정의
regions = ["1. 아시아", "2. 유럽", "3. 영미"]

countries_by_region = {
    "1. 아시아": ["일본", "중국"],
    "2. 유럽": ["프랑스", "독일"],
    "3. 영미": ["영국", "미국"]
}

# 각 국가별 대표 주문 표현 및 음성 변환용 언어 코드(lang_code) 추가
# 데이터 구조: (현지어, 발음, 한국어 해석, gTTS 언어코드)
order_phrases = {
    "일본": [
        ("これをお願いします。", "코레오 오네가이시마스.", "이거 주세요. (이것으로 부탁합니다.)", "ja")
    ],
    "중국": [
        ("我要这个。", "워 야오 쩌거.", "이거 주세요. (나는 이것을 원합니다.)", "zh-CN")
    ],
    "프랑스": [
        ("Je voudrais ceci, s'il vous plaît.", "쥬 부드레 스시, 실 부 플레.", "이거 주세요. (이것을 원합니다, 부탁해요.)", "fr")
    ],
    "독일": [
        ("Ich möchte das hier, bitte.", "이히 뫼히테 다스 히어, 비테.", "이거 주세요. (여기 이것을 원합니다, 부탁해요.)", "de")
    ],
    "영국": [
        ("Could I have this one, please?", "쿠드 아이 해브 디스 원, 플리즈?", "이거 주세요. (이것으로 주시겠어요?)", "en")
    ],
    "미국": [
        ("Can I get this one?", "캔 아이 겟 디스 원?", "이거 주세요. (이걸로 할게요.)", "en")
    ]
}

# 2. 함수 정의: 텍스트를 음성 데이터(MP3)로 변환하는 함수
def generate_audio(text, lang_code):
    tts = gTTS(text=text, lang=lang_code)
    audio_bytes = io.BytesIO()
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    return audio_bytes

# 3. 함수 정의: 선택한 국가의 대표 주문 표현 및 오디오 출력
def display_phrases(country):
    st.subheader(f"🍽️ {country}의 '이거 주세요' 주문 표현")
    
    # 조건문: 해당 국가의 데이터가 있는지 확인
    if country in order_phrases:
        phrases = order_phrases[country]
        
        # 반복문: 리스트에 담긴 대표 표현 출력
        for local_lang, pronunciation, korean, lang_code in phrases:
            with st.container(border=True):
                st.markdown("**메뉴판을 가리키며 가장 많이 쓰는 표현**")
                st.markdown(f"🗣️ **현지어:** `{local_lang}`")
                st.markdown(f"🔊 **발음:** {pronunciation}")
                st.markdown(f"🇰🇷 **해석:** {korean}")
                
                # 음성 생성 및 오디오 플레이어 출력
                st.markdown("🎧 **현지어 발음 듣기:**")
                audio_data = generate_audio(local_lang, lang_code)
                st.audio(audio_data, format="audio/mp3")
    else:
        st.error("해당 국가의 표현 데이터가 없습니다.")

# 4. 메인 웹 앱 UI 구성 함수
def main():
    st.set_page_config(page_title="문화권별 음식 주문 가이드", page_icon="🌍")
    st.title("🌍 문화권별 음식 주문 표현 가이드")
    st.write("문화권 번호를 입력하고 국가를 선택해 현지에서 '이거 주세요'라고 말하는 법을 듣고 따라 해보세요!")
    
    st.divider()
    
    # 문화권 목록 안내 (반복문 활용)
    st.markdown("### 1단계: 문화권 번호 입력")
    cols = st.columns(3)
    for i, region in enumerate(regions):
        cols[i].info(region)
        
    # 사용자 입력 (번호 선택)
    region_num = st.number_input("문화권 번호를 입력하세요 (1: 아시아, 2: 유럽, 3: 영미)", min_value=1, max_value=3, step=1)
    
    # 조건문: 입력된 번호에 따라 문화권 매핑
    selected_region = ""
    if region_num == 1:
        selected_region = "1. 아시아"
    elif region_num == 2:
        selected_region = "2. 유럽"
    elif region_num == 3:
        selected_region = "3. 영미"
        
    # 해당 문화권의 국가 두 개 가져오기 (리스트)
    available_countries = countries_by_region[selected_region]
    
    st.divider()
    st.markdown(f"### 2단계: 국가 선택 ({selected_region})")
    st.write(f"선택 가능한 국가: **{available_countries[0]}**, **{available_countries[1]}**")
    
    # 라디오 버튼으로 국가 선택
    selected_country = st.radio("표현을 확인할 국가를 선택하세요:", available_countries, horizontal=True)
    
    st.divider()
    
    # 함수 호출하여 결과 출력
    display_phrases(selected_country)

if __name__ == "__main__":
    main()
