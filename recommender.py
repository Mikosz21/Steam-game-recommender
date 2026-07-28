import pandas as pd
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def clean_tags(raw_tags):
    try:
        outer = ast.literal_eval(raw_tags)
        inner = ast.literal_eval(outer[0])
        return inner
    except (ValueError, SyntaxError, IndexError):
        return []


def build_content(row):
    genre_text = row['genre']
    tags_text = ' '.join(row['tags_clean'])
    about_text = row['about_game']
    return f"{genre_text} {genre_text} {tags_text} {tags_text} {about_text}"


def load_data(path='data/games.csv'):
    df = pd.read_csv(path, index_col=0)
    df = df[df['genre'] != 'Unknown']
    df = df.dropna(subset=['genre', 'about_game'])
    df['tags_clean'] = df['tags'].apply(clean_tags)
    df['content'] = df.apply(build_content, axis=1)
    df = df.reset_index(drop=True)
    return df


def build_model(df):
    tfidf = TfidfVectorizer(max_features=5000, stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['content'])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    return cosine_sim


def get_recommendations(title, df, cosine_sim, top_n=5):
    indices = pd.Series(df.index, index=df['title']).drop_duplicates()

    if title not in indices:
        return None

    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:top_n + 1]

    game_indices = [i[0] for i in sim_scores]
    results = df.iloc[game_indices][['title', 'genre', 'about_game', 'image', 'Link']].copy()
    results['podobienstwo'] = [round(score * 100, 1) for _, score in sim_scores]
    return results


if __name__ == '__main__':
    df = load_data()
    cosine_sim = build_model(df)
    print(get_recommendations('Synthwave Driver', df, cosine_sim))