# Test OpenAI - À exécuter pour vérifier la connexion

import streamlit as st
from openai import OpenAI

st.title("Test de connexion OpenAI")

# Récupérer la clé
try:
    api_key = st.secrets["OPENAI_API_KEY"]
    st.success("✅ Clé API trouvée dans les secrets")
except:
    st.error("❌ Clé API non trouvée")
    st.stop()

# Tester la connexion
if st.button("Tester OpenAI"):
    try:
        st.info("Tentative de connexion...")
        client = OpenAI(api_key=api_key)

        st.info("Client créé, envoi d'une requête test...")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": "Dis juste 'Connexion réussie!'"}
            ],
            max_tokens=50
        )

        st.success("✅ OpenAI fonctionne !")
        st.write(response.choices[0].message.content)

    except Exception as e:
        st.error(f"❌ Erreur: {e}")
        st.write("Type d'erreur:", type(e).__name__)