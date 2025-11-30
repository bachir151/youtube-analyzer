import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Configuration de la page
st.set_page_config(
    page_title="Résolveur Mathématique O3",
    page_icon="🔢",
    layout="wide"
)

# Mot de passe requis
REQUIRED_PASSWORD = "honor55x"

# Initialiser les variables de session
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Page d'authentification
if not st.session_state.authenticated:
    st.title("🔐 Authentification requise")
    st.write("Veuillez entrer le mot de passe pour accéder à l'application")

    password = st.text_input("Mot de passe", type="password", key="password_input")

    if st.button("Se connecter"):
        if password == REQUIRED_PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("❌ Mot de passe incorrect")

    st.stop()

# Application principale (accessible uniquement après authentification)
st.title("🔢 Résolveur de Problèmes Mathématiques")
st.write("Powered by OpenAI O3")

# Bouton de déconnexion dans la sidebar
with st.sidebar:
    st.write("### Paramètres")
    if st.button("🚪 Se déconnecter"):
        st.session_state.authenticated = False
        st.session_state.messages = []
        st.rerun()

    st.write("---")
    st.write("### À propos")
    st.info(
        "Cette application utilise le modèle O3 d'OpenAI pour résoudre des problèmes mathématiques complexes avec raisonnement détaillé.")

# Vérifier la présence de la clé API
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("⚠️ La clé API OpenAI n'est pas configurée. Veuillez définir la variable d'environnement OPENAI_API_KEY")
    st.stop()

# Initialiser le client OpenAI
client = OpenAI(api_key=api_key)

# Afficher l'historique des messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Zone de saisie pour le problème mathématique
if prompt := st.chat_input("Posez votre problème mathématique..."):
    # Ajouter le message de l'utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Générer la réponse avec streaming
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            # Appel au modèle O3 avec streaming
            stream = client.chat.completions.create(
                model="o3-mini",  # Utilisez "o3" si vous avez accès au modèle complet
                messages=[
                    {"role": "system",
                     "content": "Tu es un expert en mathématiques. Résous les problèmes étape par étape avec des explications claires et détaillées."},
                    *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                ],
                reasoning_effort="high",  # Niveau de raisonnement élevé pour les maths
                stream=True
            )

            # Afficher le texte mot par mot
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)

        except Exception as e:
            st.error(f"❌ Erreur lors de l'appel à l'API: {str(e)}")
            full_response = f"Erreur: {str(e)}"

        # Ajouter la réponse à l'historique
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# Bouton pour effacer l'historique
if st.session_state.messages:
    if st.button("🗑️ Effacer l'historique"):
        st.session_state.messages = []
        st.rerun()