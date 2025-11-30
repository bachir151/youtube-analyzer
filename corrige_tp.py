import streamlit as st

# Configuration de la page
st.set_page_config(page_title="CinéStream", page_icon="🎬", layout="wide")


films = [
    {
        "titre": "Inception",
        "genre": "Science-Fiction",
        "annee": 2010,
        "note": 8.8,
        "image": "https://m.media-amazon.com/images/I/91b3Xtjt0IL.jpg",
        "description": "Un voleur qui s'infiltre dans les rêves pour voler des secrets."
    },
    {
        "titre": "Titanic",
        "genre": "Romance",
        "annee": 1997,
        "note": 7.9,
        "image": "https://m.media-amazon.com/images/I/71kfzNYWKxL.jpg",
        "description": "L'histoire d'amour tragique à bord du célèbre paquebot."
    },
    {
        "titre": "Avatar",
        "genre": "Science-Fiction",
        "annee": 2009,
        "note": 7.8,
        "image": "https://m.media-amazon.com/images/I/71Wlt8dDfVL._AC_UF1000,1000_QL80_.jpg",
        "description": "Un marine paralysé découvre la planète Pandora."
    }

    ]

st.title("🎬 CinéStream")
st.markdown("### Regardez les meilleurs films en un clic")
st.info("Bienvenue sur CinéStream ! Découvrez des milliers de films et ajoutez vos favoris ❤️")

# === SÉLECTEUR DE THÈME DANS LA SIDEBAR ===
st.sidebar.markdown("### 🎨 Apparence")
theme_choice = st.sidebar.radio(
    "Thème",
    options=["Clair ☀️", "Sombre 🌙"],
    index=1  # 1 = Sombre par défaut
)

if "Sombre" in theme_choice:
    st._config.set_option("theme.base", "light")
else:
    st._config.set_option("theme.base", "dark")

film = films[0]
st.image(films[0]["image"], width=200)
st.subheader(film["titre"])
st.caption(film["description"])
st.write(f"**Genre :** {film['genre']}")
st.write(f"**Année :** {film['annee']}")
st.write(f"⭐ Note : {film['note']}/10")

st.header("📺 Films disponibles")

st.header("📺 Films disponibles")

for film in films:
    col1, col2 = st.columns([1, 2])

    with col1:
        st.image(film["image"], width=200)

    with col2:
        st.subheader(film["titre"])
        st.write(f"**Genre :** {film['genre']}")
        st.write(f"**Année :** {film['annee']}")
        st.write(f"⭐ Note : {film['note']}/10")

    st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.write("Colonne 1")
with col2:
    st.write("Colonne 2")
with col3:
    st.write("Colonne 3")


# Création de 3 colonnes
cols = st.columns(3)

# Parcours des films avec leur index
for idx, film in enumerate(films):
    with cols[idx % 3]:
        st.image(film["image"], use_container_width=True)
        st.subheader(film["titre"])
        st.write(f"⭐ {film['note']}/10")
        st.caption(f"{film['genre']} • {film['annee']}")
        st.markdown("---")