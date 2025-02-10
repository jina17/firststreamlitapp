import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 설치된 폰트 확인 및 출력 (디버깅용)
available_fonts = [f.name for f in fm.fontManager.ttflist]
st.write("Available fonts:", available_fonts)

# Mac 한글 폰트 설정 시도
try:
    plt.rcParams['font.family'] = ['Malgun Gothic', 'AppleGothic', 'Arial Unicode MS']
    plt.rcParams['font.sans-serif'] = ['Malgun Gothic', 'AppleGothic', 'Arial Unicode MS']
    plt.rcParams['axes.unicode_minus'] = False
    
    # 폰트 캐시 재생성
    fm._rebuild()
except:
    st.error("한글 폰트 설정에 실패했습니다.")

def load_data():
    # 데이터 로드
    indivi_major = pd.read_csv("indivi_major.csv")
    major_total = pd.read_csv("major_total.csv")
    return indivi_major, major_total

def plot_major_distribution(df, selected_major):
    # 선택한 전공이 등장한 위치에 따라 나머지 전공들의 분포 확인
    first_major_mask = df['첫번째 전공'] == selected_major
    second_major_mask = df['두번째 전공'] == selected_major
    third_major_mask = df['세번째 전공'] == selected_major
    
    distributions = {}
    
    if first_major_mask.sum() > 0:
        distributions['첫번째 전공에서 등장'] = df.loc[first_major_mask, '두번째 전공'].value_counts()
    if second_major_mask.sum() > 0:
        distributions['두번째 전공에서 등장'] = df.loc[second_major_mask, '첫번째 전공'].value_counts()
    if third_major_mask.sum() > 0:
        distributions['세번째 전공에서 등장'] = df.loc[third_major_mask, '첫번째 전공'].value_counts()
    
    return distributions

def main():
    st.title("전공 분포 분석")
    
    # 데이터 로드
    indivi_major, major_total = load_data()
    
    # 전공 선택
    major_list = major_total['전공'].unique()
    selected_major = st.selectbox("전공 선택", major_list)
    
    # 데이터 필터링 및 그래프 생성
    distributions = plot_major_distribution(indivi_major, selected_major)
    
    for title, dist in distributions.items():
        st.subheader(title)
        # 그래프 생성 전에 한글 폰트 명시적 설정
        with plt.style.context('default'):
            fig, ax = plt.subplots(figsize=(10, 8))
            wedges, texts, autotexts = ax.pie(dist, 
                                            labels=dist.index, 
                                            autopct='%1.1f%%', 
                                            startangle=90)
            
            # 폰트 속성 직접 설정
            font_prop = fm.FontProperties(family=['Malgun Gothic', 'AppleGothic', 'Arial Unicode MS'])
            plt.setp(autotexts, size=8, fontproperties=font_prop)
            plt.setp(texts, size=8, fontproperties=font_prop)
            
            ax.axis('equal')
            st.pyplot(fig)
            plt.close(fig)

if __name__ == "__main__":
    main()
