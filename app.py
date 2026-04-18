import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Page setup
st.set_page_config(page_title="Sentiment Dashboard", layout="wide")

# Title
st.title("🔥 Amazon Review Sentiment Dashboard")
st.write("Analyze customer opinions using NLP")

# Upload
uploaded_file = st.file_uploader("📂 Upload Amazon Reviews CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # 🔥 IMPORTANT: reduce size (FAST)
    df = df.head(5000)

    st.subheader("📌 Raw Data Preview")
    st.dataframe(df.head())

    # Detect review column
    text_column = None
    for col in df.columns:
        if "review" in col.lower():
            text_column = col

    if text_column is None:
        text_column = st.selectbox("Select Review Column", df.columns)

    st.success(f"Using column: {text_column}")

    # 🔥 USE LABEL (NO TEXTBLOB - FAST)
    if 'Label' in df.columns:
        df['Sentiment'] = df['Label'].map({1: 'Positive', 0: 'Negative'})
    else:
        st.error("Label column not found!")
        st.stop()

    # Counts
    counts = df['Sentiment'].value_counts()

    # Metrics
    st.subheader("📊 Sentiment Summary")
    col1, col2 = st.columns(2)
    col1.metric("😊 Positive", counts.get("Positive", 0))
    col2.metric("😡 Negative", counts.get("Negative", 0))

    # Charts
    st.subheader("📈 Visualization")

    col3, col4 = st.columns(2)

    with col3:
        fig1, ax1 = plt.subplots()
        counts.plot(kind='bar', ax=ax1)
        plt.title("Sentiment Distribution")
        st.pyplot(fig1)

    with col4:
        fig2, ax2 = plt.subplots()
        counts.plot(kind='pie', autopct='%1.1f%%', ax=ax2)
        plt.ylabel("")
        st.pyplot(fig2)

    # WordCloud
    st.subheader("☁️ Word Cloud")
    text = " ".join(df[text_column].astype(str))

    wc = WordCloud(width=800, height=400, background_color="white").generate(text)

    fig3, ax3 = plt.subplots()
    ax3.imshow(wc)
    ax3.axis("off")
    st.pyplot(fig3)

    # Filter
    st.subheader("🔍 Filter Reviews")
    option = st.selectbox("Choose Sentiment", ["All", "Positive", "Negative"])

    if option != "All":
        filtered_df = df[df['Sentiment'] == option]
        st.dataframe(filtered_df)
    else:
        st.dataframe(df)

    # Download
    st.subheader("⬇️ Download Results")
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV", csv, "sentiment_results.csv")

else:
    st.info("👆 Upload a CSV file to start analysis")