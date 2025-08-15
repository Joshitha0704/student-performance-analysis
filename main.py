import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Student Performance Analytics", layout="wide")
st.title("📚 Student Performance Analytics Dashboard")

uploaded_file = st.file_uploader("📂 Upload your CSV file", type="csv")

# File loading logic
df = None
if uploaded_file is None:
    st.warning("Or load from Google Drive path below 👇")
    path = st.text_input("Enter full path to CSV in Google Drive:")
    if path:
        try:
            df = pd.read_csv(path)
            st.success("✅ File loaded from Drive!")
        except Exception as e:
            st.error(f"❌ Could not load file. Check path. Error: {e}")
else:
    # If user uploads file
    df = pd.read_csv(uploaded_file, sep=';')

# Display analytics if data is loaded
if df is not None:
    st.subheader("🔍 Data Preview")
    st.dataframe(df.head())

    st.subheader("📊 Summary Statistics")
    st.write(df.describe())

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🎓 Average Final Grade by Gender")
        avg_by_gender = df.groupby('sex')['G3'].mean().reset_index()
        plt.figure(figsize=(5, 3))
        sns.barplot(x='sex', y='G3', data=avg_by_gender)
        st.pyplot(plt.gcf())
        plt.clf()

    with col2:
        st.markdown("### 📈 Study Time vs Final Grade")
        plt.figure(figsize=(5, 3))
        sns.scatterplot(data=df, x='studytime', y='G3')
        st.pyplot(plt.gcf())
        plt.clf()

    col3, col4 = st.columns(2)
    with col3:
        st.markdown("### 🚸 Absences Impact on Grades")
        plt.figure(figsize=(5, 3))
        sns.boxplot(x='G3', y='absences', data=df)
        st.pyplot(plt.gcf())
        plt.clf()

    with col4:
        st.markdown("### 👨‍👩‍👧‍👦 Parent Education vs Final Grade")
        df['parent_avg'] = (df['Medu'] + df['Fedu']) / 2
        plt.figure(figsize=(5, 3))
        sns.scatterplot(data=df, x='parent_avg', y='G3')
        plt.xlabel('Average Parent Education Level')
        st.pyplot(plt.gcf())
        plt.clf()

    col5, col6 = st.columns(2)
    with col5:
        st.markdown("### 🎯 Pass vs Fail Ratio")
        df['result'] = df['G3'].apply(lambda x: 'Pass' if x >= 10 else 'Fail')
        result_counts = df['result'].value_counts()
        fig, ax = plt.subplots(figsize=(3, 3))
        ax.pie(result_counts, labels=result_counts.index, autopct='%1.1f%%', startangle=90)
        st.pyplot(fig)

    with col6:
        st.markdown("### 📘 Final Grade Distribution")
        plt.figure(figsize=(5, 3))
        sns.histplot(df['G3'], bins=10, kde=True, color='skyblue')
        plt.xlabel("Final Grade (G3)")
        plt.ylabel("Frequency")
        st.pyplot(plt.gcf())
        plt.clf()
