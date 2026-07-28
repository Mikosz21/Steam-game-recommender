#  Steam Game Recommender

System rekomendacji gier ze Steam oparty na content-based filtering — wybierz grę, którą lubisz, a aplikacja znajdzie podobne tytuły na podstawie gatunku, tagów i opisu.

** Aplikacja na żywo:** [steam-game-recommender-b4shdkarcl9dz66hyfrrfk.streamlit.app](https://steam-game-recommender-b4shdkarcl9dz66hyfrrfk.streamlit.app/)

## Jak to działa

1. Dane o ~2800 grach ze Steam (gatunek, tagi, opis) są łączone w jeden tekst dla każdej gry
2. Tekst jest zamieniany na wektory liczbowe przy pomocy **TF-IDF** (Term Frequency – Inverse Document Frequency)
3. Podobieństwo między grami liczone jest jako **cosine similarity** między wektorami
4. Dla wybranej gry zwracane są tytuły o najwyższym podobieństwie

## Technologie

- **Python** – logika aplikacji
- **pandas** – wczytywanie i przetwarzanie danych
- **scikit-learn** – TF-IDF i cosine similarity
- **Streamlit** – interfejs webowy i deployment

## Uruchomienie lokalnie

```bash
git clone https://github.com/Mikosz21/Steam-game-recommender.git
cd Steam-game-recommender
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Struktura projektu

```
├── app.py              # Interfejs Streamlit
├── recommender.py       # Logika: wczytywanie danych, TF-IDF, rekomendacje
├── data/games.csv        # Zbiór danych o grach ze Steam
└── requirements.txt      # Zależności projektu
```
