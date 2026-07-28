import streamlit as st
import pandas as pd
from recommender import load_data, build_model, get_recommendations

st.set_page_config(page_title="Steam Game Recommender", page_icon="🎮", layout="wide")

st.title("🎮 Steam Game Recommender")
st.write("Wybierz grę, którą lubisz, a znajdziemy Ci podobne tytuły na podstawie gatunku, tagów i opisu.")

@st.cache_data
def get_data_and_model():
    df = load_data()
    cosine_sim = build_model(df)
    return df, cosine_sim

df, cosine_sim = get_data_and_model()

game_titles = sorted(df['title'].unique())

selected_game = st.selectbox("Wybierz grę:", game_titles)

top_n = st.slider("Ile rekomendacji chcesz zobaczyć?", min_value=3, max_value=15, value=5)

if st.button("Znajdź podobne gry"):
    recommendations = get_recommendations(selected_game, df, cosine_sim, top_n=top_n)

    if recommendations is None:
        st.error("Nie znaleziono tej gry w bazie.")
    else:
        st.subheader(f"Gry podobne do: {selected_game}")

        for _, row in recommendations.iterrows():
            col1, col2 = st.columns([1, 3])

            with col1:
                if pd.notna(row['image']):
                    st.image(row['image'], use_container_width=True)

            with col2:
                st.markdown(f"### {row['title']}")
                st.write(f"**Gatunek:** {row['genre']}")
                st.write(f"**Podobieństwo:** {row['podobienstwo']}%")
                st.write(row['about_game'][:200] + "...")
                st.markdown(f"[Zobacz na Steam]({row['Link']})")

            st.divider()