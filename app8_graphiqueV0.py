import streamlit as st

# Configuration de la page
st.set_page_config(page_title="CinéStream", page_icon="🎬", layout="wide")

# Initialisation des favoris dans session_state
if "favoris" not in st.session_state:
    st.session_state.favoris = []

# === Base de données des films (avec URLs d'images mises à jour) ===
# === Base de données des films (URLs corrigées seulement pour Avatar et Parasite) ===
films = [
    {
        "titre": "Inception",
        "genre": "Science-Fiction",
        "annee": 2010,
        "note": 8.8,
        "image": "https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_FMjpg_UX1000_.jpg",
        "description": "Un voleur qui s'infiltre dans les rêves pour voler des secrets."
    },
    {
        "titre": "Titanic",
        "genre": "Romance",
        "annee": 1997,
        "note": 7.9,
        "image": "https://image.tmdb.org/t/p/w500/9xjZS2rlVxm8SFx8kPC3aIGCOYQ.jpg",
        "description": "L'histoire d'amour tragique à bord du célèbre paquebot."
    },
    {
        "titre": "Avatar",
        "genre": "Science-Fiction",
        "annee": 2009,
        "note": 7.8,
        "image": "https://m.media-amazon.com/images/M/MV5BZDA0OGQxNTItMDZkMC00N2UyLTg3MzMtYTJmNjg3Nzk5MzRiXkEyXkFqcGdeQXVyMjUzOTY1NTc@._V1_FMjpg_UX1000_.jpg",
        "description": "Un marine paralysé découvre la planète Pandora."
    },
    {
        "titre": "Le Seigneur des Anneaux : La Communauté de l'Anneau",
        "genre": "Aventure",
        "annee": 2001,
        "note": 8.9,
        "image": "https://m.media-amazon.com/images/I/81EBp0vOZZL._AC_UF894,1000_QL80_.jpg",
        "description": "L'épopée fantastique commence avec l'Anneau Unique."
    },
    {
        "titre": "Interstellar",
        "genre": "Science-Fiction",
        "annee": 2014,
        "note": 8.7,
        "image": "https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg",
        "description": "Une mission spatiale pour sauver l'humanité."
    },
    {
        "titre": "The Matrix",
        "genre": "Science-Fiction",
        "annee": 1999,
        "note": 8.7,
        "image": "https://image.tmdb.org/t/p/w500/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg",
        "description": "Un hacker découvre que le monde est une simulation."
    },
    {
        "titre": "Parasite",
        "genre": "Thriller",
        "annee": 2019,
        "note": 8.5,
        "image": "https://m.media-amazon.com/images/M/MV5BYWZjMjk3ZTItODQ2ZC00NTY5LWE0ZDYtZTI3MjcwN2Q5NTVkXkEyXkFqcGdeQXVyODk4OTc3MTY@._V1_FMjpg_UX1000_.jpg",
        "description": "Une famille pauvre s'infiltre chez des riches."
    },
]

# === Titre principal ===
st.title("🎬 CinéStream")
st.markdown("### Regardez les meilleurs films en un clic")
st.info("Bienvenue sur CinéStream ! Découvrez des milliers de films et ajoutez vos favoris ❤️")

st.markdown("---")

# === Sidebar : Filtres ===
st.sidebar.header("🔍 Filtres")

# Recherche par titre
recherche = st.sidebar.text_input("Rechercher un film", "")
recherche = recherche.lower()

# Filtre par genre
genres_uniques = ["Tous"] + sorted({film["genre"] for film in films})
genre_choisi = st.sidebar.selectbox("Genre", genres_uniques)

# Filtre par note minimale
note_min = st.sidebar.slider("Note minimale", 0.0, 10.0, 7.0, 0.1)

st.sidebar.markdown("---")
st.sidebar.header("❤️ Mes Favoris")

# Affichage des favoris
if len(st.session_state.favoris) == 0:
    st.sidebar.info("Aucun favori pour le moment")
else:
    for fav in st.session_state.favoris:
        st.sidebar.write(f"• {fav}")

# Bouton pour vider les favoris
if st.sidebar.button("🗑️ Vider les favoris"):
    st.session_state.favoris = []
    st.sidebar.success("Favoris vidés !")

# === Statistiques ===
st.header("📊 Statistiques du catalogue")

col1, col2, col3 = st.columns(3)

# Nombre de films
col1.metric("Nombre de films", len(films))

# Note moyenne
note_moyenne = sum(film["note"] for film in films) / len(films)
col2.metric("Note moyenne", f"{note_moyenne:.1f}/10")

# Année la plus récente
annee_max = max(film["annee"] for film in films)
col3.metric("Film le plus récent", annee_max)

# Graphique de répartition par genre
st.markdown("---")
st.subheader("📊 Répartition par genre")

comptage_genres = {}
for film in films:
    genre = film["genre"]
    comptage_genres[genre] = comptage_genres.get(genre, 0) + 1

st.bar_chart(comptage_genres)

st.markdown("---")

# === Affichage des films en grille (3 par ligne) ===
st.header("🎥 Films disponibles")

# Filtrage des films
films_filtres = []
for film in films:
    titre_lower = film["titre"].lower()
    correspond_recherche = recherche in titre_lower
    correspond_genre = (genre_choisi == "Tous" or film["genre"] == genre_choisi)
    correspond_note = film["note"] >= note_min

    if correspond_recherche and correspond_genre and correspond_note:
        films_filtres.append(film)

# Affichage en grille
cols = st.columns(3)
for idx, film in enumerate(films_filtres):
    with cols[idx % 3]:
        st.image(film["image"], use_container_width=True)
        st.subheader(f"🎥 {film['titre']}")
        st.caption(film["description"])
        st.write(f"**Genre :** {film['genre']} | **Année :** {film['annee']} | ⭐ **{film['note']}/10**")

        # Bouton Regarder
        if st.button("▶️ Regarder", key=f"watch_{film['titre']}"):
            st.success(f"▶️ Lecture de **{film['titre']}** en cours...")

        # Bouton Favoris (amélioré)
        if film["titre"] not in st.session_state.favoris:
            if st.button("❤️ Ajouter aux favoris", key=f"fav_{film['titre']}"):
                st.session_state.favoris.append(film["titre"])
                st.success(f"❤️ {film['titre']} ajouté aux favoris !")
                st.rerun()
        else:
            st.button("💚 Déjà dans les favoris", key=f"fav_added_{film['titre']}", disabled=True)

# Message si aucun film ne correspond
if not films_filtres:
    st.warning("Aucun film ne correspond à vos critères de recherche.")