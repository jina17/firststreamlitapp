import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 데이터 로드
@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path)
    return data[['학번', '전공현황.1', '전공현황.2', '전공현황.3']]

data_file = 'indivi_major.csv'
data = load_data(data_file)

# 학번별 첫 번째 전공현황.3 값 추출
first_major = data.groupby('학번')['전공현황.3'].first().reset_index()
first_major_list = first_major['전공현황.3'].tolist()

# 학번별 두 번째 전공현황.3 값 추출
def second_occurrence(series):
    return series.dropna().iloc[1] if len(series.dropna()) > 1 else None

second_major = data.groupby('학번')['전공현황.3'].apply(second_occurrence).reset_index(name='전공현황.3')
second_major_list = second_major['전공현황.3'].dropna().tolist()

# 앱 제목
st.title("Indivi Major Data Analysis")

# 데이터 미리보기
st.header("Dataset Preview")
st.write(data.head())

# 데이터 요약 정보
st.header("Data Overview")
st.write("Number of Rows:", data.shape[0])
st.write("Number of Columns:", data.shape[1])
st.write("Columns:", list(data.columns))
st.write("Missing Values:")
st.write(data.isnull().sum())

# 통계 정보
st.header("Descriptive Statistics")
st.write(data.describe())

# 사용자 선택에 따른 데이터 시각화
st.header("Data Visualization")
columns = data.select_dtypes(include=['float64', 'int64']).columns
if columns.any():
    selected_column = st.selectbox("Select a numeric column to visualize:", columns)
    
    # 히스토그램
    st.subheader(f"Histogram of {selected_column}")
    fig, ax = plt.subplots()
    data[selected_column].hist(ax=ax, bins=20, color='skyblue', edgecolor='black')
    ax.set_title(f"Histogram of {selected_column}")
    ax.set_xlabel(selected_column)
    ax.set_ylabel("Frequency")
    st.pyplot(fig)

    # 박스플롯
    st.subheader(f"Boxplot of {selected_column}")
    fig, ax = plt.subplots()
    ax.boxplot(data[selected_column].dropna(), vert=False)
    ax.set_title(f"Boxplot of {selected_column}")
    ax.set_xlabel(selected_column)
    st.pyplot(fig)

else:
    st.write("No numeric columns found in the dataset for visualization.")

# 사용자 필터링 기능
st.header("Filter Data")
for column in data.select_dtypes(include=['object']).columns:
    unique_values = data[column].unique()
    selected_value = st.selectbox(f"Filter by {column}", options=["All"] + list(unique_values))
    if selected_value != "All":
        data = data[data[column] == selected_value]

st.write("Filtered Data:")
st.write(data)

# 학번별 첫 번째 전공현황.3 리스트 출력
st.header("First Major by 학번")
st.write(first_major)
st.write("First Major List:", first_major_list)

# 학번별 두 번째 전공현황.3 리스트 출력
st.header("Second Major by 학번")
st.write(second_major)
st.write("Second Major List:", second_major_list)
