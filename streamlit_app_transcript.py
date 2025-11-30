import streamlit as st
import os
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
import re
from openai import OpenAI

# Configuration de la page
st.set_page_config(
    page_title="Extracteur d'idées YouTube",
    page_icon="🎥",
    layout="wide"
)


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
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        # Essayer d'abord d'obtenir une transcription en français
        try:
            transcript = transcript_list.find_transcript(['fr'])
        except:
            # Sinon, prendre la transcription générée automatiquement ou en anglais
            try:
                transcript = transcript_list.find_generated_transcript(['fr', 'en'])
            except:
                transcript = transcript_list.find_transcript(['en'])

        # Récupérer le texte complet
        transcript_data = transcript.fetch()
        texte_complet = ' '.join([entry['text'] for entry in transcript_data])

        return texte_complet, None

    except TranscriptsDisabled:
        return None, "Les sous-titres sont désactivés pour cette vidéo."
    except NoTranscriptFound:
        return None, "Aucune transcription disponible pour cette vidéo."
    except Exception as e:
        return None, f"Erreur lors de la récupération : {str(e)}"


# Fonction pour analyser le texte avec OpenAI
def analyser_transcription(texte, api_key):
    """Utilise OpenAI pour extraire les idées principales"""
    try:
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
            max_tokens=1500
        )

        return response.choices[0].message.content, None

    except Exception as e:
        return None, f"Erreur lors de l'analyse : {str(e)}"


# Interface Streamlit
st.title("🎥 Extracteur d'Idées YouTube")
st.markdown("Extraire la transcription d'une vidéo YouTube et analyser ses idées principales avec l'IA")

# Récupération de la clé API depuis les secrets
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except:
    st.error("⚠️ Clé API OpenAI non configurée. Veuillez ajouter OPENAI_API_KEY dans les secrets Streamlit.")
    st.stop()

# Champ pour l'URL
url_youtube = st.text_input(
    "🔗 Entrez l'URL de la vidéo YouTube :",
    placeholder="https://www.youtube.com/watch?v=..."
)

# Bouton d'analyse
if st.button("🚀 Analyser la vidéo", type="primary"):
    if not url_youtube:
        st.warning("Veuillez entrer une URL YouTube.")
    else:
        # Extraire l'ID de la vidéo
        video_id = extraire_video_id(url_youtube)

        if not video_id:
            st.error("❌ URL YouTube invalide. Veuillez vérifier le lien.")
        else:
            # Afficher la vidéo
            st.video(url_youtube)

            # Étape 1 : Récupération de la transcription
            with st.spinner("📝 Récupération de la transcription..."):
                transcription, erreur = obtenir_transcription(video_id)

            if erreur:
                st.error(f"❌ {erreur}")
            else:
                st.success("✅ Transcription récupérée avec succès !")

                # Afficher la transcription dans un expander
                with st.expander("📄 Voir la transcription complète"):
                    st.text_area(
                        "Transcription",
                        transcription,
                        height=300,
                        disabled=True
                    )

                # Étape 2 : Analyse avec OpenAI
                with st.spinner("🤖 Analyse en cours avec l'IA..."):
                    analyse, erreur_analyse = analyser_transcription(transcription, api_key)

                if erreur_analyse:
                    st.error(f"❌ {erreur_analyse}")
                else:
                    st.success("✅ Analyse terminée !")

                    # Afficher l'analyse
                    st.markdown("## 💡 Idées Essentielles")
                    st.markdown(analyse)

                    # Bouton de téléchargement
                    st.download_button(
                        label="📥 Télécharger l'analyse",
                        data=analyse,
                        file_name="analyse_youtube.txt",
                        mime="text/plain"
                    )

# Informations dans la sidebar
with st.sidebar:
    st.header("ℹ️ À propos")
    st.markdown("""
    Cette application permet de :
    - 📹 Extraire la transcription d'une vidéo YouTube
    - 🧠 Analyser le contenu avec l'IA
    - 📊 Obtenir un résumé des idées principales

    **Comment utiliser :**
    1. Collez l'URL d'une vidéo YouTube
    2. Cliquez sur "Analyser"
    3. Consultez les résultats
    """)

    st.markdown("---")
    st.markdown("**Note :** La vidéo doit avoir des sous-titres disponibles.")