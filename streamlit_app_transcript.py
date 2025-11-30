import streamlit as st
import os
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
import re
from openai import OpenAI
import time

# Configuration de la page
st.set_page_config(
    page_title="Extracteur d'idées YouTube",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialiser session_state
if 'transcription' not in st.session_state:
    st.session_state['transcription'] = None
if 'video_id' not in st.session_state:
    st.session_state['video_id'] = None


# Fonction pour extraire l'ID de la vidéo YouTube
def extraire_video_id(url):
    """Extrait l'ID de la vidéo depuis différents formats d'URL YouTube"""
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:embed\/)([0-9A-Za-z_-]{11})',
        r'^([0-9A-Za-z_-]{11})$'
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


# Fonction pour obtenir la transcription
def obtenir_transcription(video_id):
    """Récupère la transcription d'une vidéo YouTube"""
    try:
        # Créer une instance de l'API
        api = YouTubeTranscriptApi()

        # Essayer d'abord en français, puis en anglais
        try:
            fetched_transcript = api.fetch(video_id, languages=['fr', 'en'])
        except:
            # Si ça échoue, essayer avec la langue par défaut
            fetched_transcript = api.fetch(video_id)

        # Récupérer le texte complet
        # Les objets FetchedTranscriptSnippet utilisent des attributs, pas des clés
        texte_complet = ' '.join([entry.text for entry in fetched_transcript])

        return texte_complet, None

    except TranscriptsDisabled:
        return None, "Les sous-titres sont désactivés pour cette vidéo."
    except NoTranscriptFound:
        return None, "Aucune transcription disponible pour cette vidéo."
    except Exception as e:
        return None, f"Erreur lors de la récupération : {str(e)}"


# Fonction pour analyser le texte avec OpenAI
def analyser_transcription(texte, api_key, max_tokens=1500):
    """Utilise OpenAI pour extraire les idées principales"""
    try:
        # Initialiser le client OpenAI avec juste la clé API
        client = OpenAI(api_key=api_key)

        prompt = f"""Analyse la transcription suivante et extrais les idées essentielles.

Organise ta réponse de la manière suivante :
1. Résumé principal (2-3 phrases)
2. Idées clés (liste à puces des points importants)
3. Concepts principaux abordés
4. Conclusions ou points à retenir

Transcription :
{texte[:15000]}"""  # Limiter la taille pour éviter de dépasser les tokens

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system",
                 "content": "Tu es un assistant expert en analyse de contenu qui extrait les idées essentielles de manière claire et structurée."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=max_tokens,
            stream=True  # Activer le streaming
        )

        return response, None

    except Exception as e:
        return None, f"Erreur lors de l'analyse : {str(e)}"


# Fonction pour nettoyer la transcription
def nettoyer_transcription(texte, api_key):
    """Nettoie la transcription sans modifier le contenu"""
    try:
        client = OpenAI(api_key=api_key)

        prompt = f"""Nettoie cette transcription YouTube sans modifier le contenu(
         Ne modifie PAS le contenu, ne résume PAS, ne traduis pas, enlève juste les détails qui ne font pas partie du texte)

, Voici la transcription :
{texte}"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system",
                 "content": "Tu es un assistant qui nettoie et formate des transcriptions sans en modifier le contenu."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=4000,
            stream=True
        )

        return response, None

    except Exception as e:
        return None, f"Erreur lors du nettoyage : {str(e)}"


# Interface Streamlit
st.title("🎥 Extracteur d'Idées YouTube")
st.markdown("Extraire la transcription d'une vidéo YouTube et analyser ses idées principales avec l'IA")

# Récupération de la clé API depuis les secrets
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except:
    st.error("⚠️ Clé API OpenAI non configurée. Veuillez ajouter OPENAI_API_KEY dans les secrets Streamlit.")
    st.stop()

# Sidebar avec paramètres
with st.sidebar:
    st.header("⚙️ Paramètres")

    # Toggle mode sombre/clair
    st.markdown("### 🎨 Apparence")
    theme = st.radio(
        "Mode d'affichage",
        ["💡 Clair", "🌙 Sombre"],
        horizontal=True,
        key="theme_selector"
    )

    # CSS pour le mode sombre avec force
    if theme == "🌙 Sombre":
        st.markdown("""
        <style>
        /* Mode sombre complet */
        [data-testid="stAppViewContainer"] {
            background-color: #0e1117 !important;
        }
        [data-testid="stSidebar"] {
            background-color: #262730 !important;
        }
        [data-testid="stHeader"] {
            background-color: #0e1117 !important;
        }
        .stApp {
            background-color: #0e1117 !important;
        }
        section[data-testid="stSidebar"] > div {
            background-color: #262730 !important;
        }
        /* Textes */
        .stMarkdown, p, span, div, label {
            color: #fafafa !important;
        }
        /* Boutons */
        .stButton button {
            background-color: #262730 !important;
            color: #fafafa !important;
            border: 1px solid #4a4a4a !important;
        }
        .stButton button:hover {
            background-color: #3a3a3a !important;
            border-color: #6a6a6a !important;
        }
        /* Inputs */
        .stTextInput input {
            background-color: #262730 !important;
            color: #fafafa !important;
            border-color: #4a4a4a !important;
        }
        /* Expanders */
        .streamlit-expanderHeader {
            background-color: #262730 !important;
            color: #fafafa !important;
        }
        /* Code blocks */
        .stCodeBlock {
            background-color: #1a1a1a !important;
        }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        /* Mode clair - Reset au thème par défaut */
        [data-testid="stAppViewContainer"] {
            background-color: #ffffff !important;
        }
        [data-testid="stSidebar"] {
            background-color: #f0f2f6 !important;
        }
        [data-testid="stHeader"] {
            background-color: #ffffff !important;
        }
        .stApp {
            background-color: #ffffff !important;
        }
        section[data-testid="stSidebar"] > div {
            background-color: #f0f2f6 !important;
        }
        /* Textes */
        .stMarkdown, p, span, div, label {
            color: #31333F !important;
        }
        /* Boutons */
        .stButton button {
            background-color: #ffffff !important;
            color: #31333F !important;
            border: 1px solid #d3d3d3 !important;
        }
        .stButton button:hover {
            background-color: #f0f2f6 !important;
        }
        /* Inputs */
        .stTextInput input {
            background-color: #ffffff !important;
            color: #31333F !important;
            border-color: #d3d3d3 !important;
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Slider pour les tokens
    st.markdown("### 🔧 Paramètres d'analyse")
    max_tokens = st.slider(
        "Nombre de tokens pour l'analyse",
        min_value=500,
        max_value=4000,
        value=1500,
        step=100,
        help="Plus de tokens = réponse plus détaillée (mais plus lent et coûteux)"
    )

    st.markdown("---")
    st.header("ℹ️ À propos")
    st.markdown("""
    Cette application permet de :
    - 📹 Extraire la transcription d'une vidéo YouTube
    - 🧹 Nettoyer la transcription
    - 🧠 Analyser le contenu avec l'IA
    - 📊 Obtenir un résumé des idées principales

    **Comment utiliser :**
    1. Collez l'URL d'une vidéo YouTube
    2. Cliquez sur "Analyser"
    3. Utilisez les boutons pour nettoyer ou analyser
    """)

    st.markdown("---")
    st.markdown("**Note :** La vidéo doit avoir des sous-titres disponibles.")

# Champ pour l'URL
url_youtube = st.text_input(
    "🔗 Entrez l'URL de la vidéo YouTube :",
    placeholder="https://www.youtube.com/watch?v=..."
)

# Bouton d'analyse principal
if st.button("🚀 Récupérer la transcription", type="primary"):
    if not url_youtube:
        st.warning("Veuillez entrer une URL YouTube.")
    else:
        # Extraire l'ID de la vidéo
        video_id = extraire_video_id(url_youtube)

        if not video_id:
            st.error("❌ URL YouTube invalide. Veuillez vérifier le lien.")
        else:
            # Étape 1 : Récupération de la transcription
            with st.spinner("📝 Récupération de la transcription..."):
                transcription, erreur = obtenir_transcription(video_id)

            if erreur:
                st.error(f"❌ {erreur}")
            else:
                st.success("✅ Transcription récupérée avec succès !")

                # Stocker la transcription dans session_state
                st.session_state['transcription'] = transcription
                st.session_state['video_id'] = video_id

# Si une transcription existe, afficher la vidéo et les options
if st.session_state['transcription']:
    # Afficher la vidéo
    if st.session_state['video_id']:
        st.video(f"https://www.youtube.com/watch?v={st.session_state['video_id']}")

    # Afficher la transcription dans un expander
    with st.expander("📄 Voir la transcription brute", expanded=False):
        st.text_area(
            "Transcription",
            st.session_state['transcription'],
            height=300,
            disabled=True,
            key="raw_transcript"
        )

        # Bouton copier
        st.code(st.session_state['transcription'], language=None)

    st.markdown("---")

    # Section avec boutons d'action - MAINTENANT PERSISTANTS
    st.markdown("### 🎯 Actions disponibles")
    col1, col2 = st.columns(2)

    with col1:
        # Bouton pour nettoyer la transcription
        if st.button("🧹 Nettoyer la transcription", use_container_width=True, key="btn_clean"):
            with st.spinner("🤖 Nettoyage en cours..."):
                response_stream, erreur_nettoyage = nettoyer_transcription(
                    st.session_state['transcription'],
                    api_key
                )

            if erreur_nettoyage:
                st.error(f"❌ {erreur_nettoyage}")
            else:
                st.success("✅ Transcription nettoyée !")

                # Afficher avec streaming
                st.markdown("## 🧹 Transcription Nettoyée")
                transcription_nettoyee_container = st.empty()
                transcription_nettoyee = ""

                for chunk in response_stream:
                    if chunk.choices[0].delta.content:
                        transcription_nettoyee += chunk.choices[0].delta.content
                        transcription_nettoyee_container.markdown(transcription_nettoyee)

                # Stocker dans session state
                st.session_state['transcription_nettoyee'] = transcription_nettoyee

                # Bouton de téléchargement
                st.download_button(
                    label="📥 Télécharger la transcription nettoyée",
                    data=transcription_nettoyee,
                    file_name="transcription_nettoyee.txt",
                    mime="text/plain",
                    key="download_clean"
                )

    with col2:
        # Bouton pour analyser
        if st.button("💡 Extraire les idées essentielles", use_container_width=True, key="btn_analyze"):
            with st.spinner("🤖 Analyse en cours avec l'IA..."):
                response_stream, erreur_analyse = analyser_transcription(
                    st.session_state['transcription'],
                    api_key,
                    max_tokens
                )

            if erreur_analyse:
                st.error(f"❌ {erreur_analyse}")
            else:
                st.success("✅ Analyse terminée !")

                # Afficher l'analyse avec streaming
                st.markdown("## 💡 Idées Essentielles")
                analyse_container = st.empty()
                analyse_complete = ""

                for chunk in response_stream:
                    if chunk.choices[0].delta.content:
                        analyse_complete += chunk.choices[0].delta.content
                        analyse_container.markdown(analyse_complete)

                # Stocker dans session state
                st.session_state['analyse'] = analyse_complete

                # Bouton de téléchargement
                st.download_button(
                    label="📥 Télécharger l'analyse",
                    data=analyse_complete,
                    file_name="analyse_youtube.txt",
                    mime="text/plain",
                    key="download_analyze"
                )

    # Afficher les résultats précédents s'ils existent
    if 'transcription_nettoyee' in st.session_state and st.session_state['transcription_nettoyee']:
        with st.expander("📋 Dernière transcription nettoyée", expanded=False):
            st.markdown(st.session_state['transcription_nettoyee'])
            st.download_button(
                label="📥 Télécharger",
                data=st.session_state['transcription_nettoyee'],
                file_name="transcription_nettoyee.txt",
                mime="text/plain",
                key="download_clean_prev"
            )

    if 'analyse' in st.session_state and st.session_state['analyse']:
        with st.expander("📊 Dernière analyse", expanded=False):
            st.markdown(st.session_state['analyse'])
            st.download_button(
                label="📥 Télécharger",
                data=st.session_state['analyse'],
                file_name="analyse_youtube.txt",
                mime="text/plain",
                key="download_analyze_prev"
            )