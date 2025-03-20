import streamlit as st
import openai
import os

# ✅ Configurar la API Key correctamente
api_key = os.getenv("OPENAI_API_KEY")  # Usa variables de entorno para mayor seguridad

# Si no tienes la API Key en una variable de entorno, puedes ponerla manualmente:
# api_key = "tu-clave-api-aquí"

if not api_key:
    st.error("⚠️ Error: No se encontró la API Key de OpenAI. Asegúrate de configurarla.")
    st.stop()

# ✅ Crear el cliente de OpenAI correctamente
client = openai.OpenAI(api_key=api_key)

# ✅ Configuración de la página
st.set_page_config(page_title="Chatbot ISO 55001", page_icon="🤖")
st.title("Chatbot de Gestión de Activos - ISO 55001")

# ✅ Inicializar historial de conversación si no existe
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "Eres un experto en gestión de activos basado en la ISO 55001."}
    ]

# ✅ Selección del modelo para optimización de costos
model = st.radio("Selecciona el modelo GPT:", ("gpt-4-turbo", "gpt-3.5-turbo"))

# ✅ Entrada del usuario
pregunta = st.text_input("Haz una pregunta sobre la ISO 55001:")

if st.button("Enviar") and pregunta:
    
    # ✅ Asegurar que messages esté en el estado de sesión
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # ✅ Agregar la pregunta al historial
    st.session_state["messages"].append({"role": "user", "content": pregunta})
    
    try:
        # ✅ Llamar a la API de OpenAI
        response = client.chat.completions.create(
            model=model,
            messages=st.session_state["messages"],
            max_tokens=500  # Limitar tokens para optimizar costos
        )

        # ✅ Extraer la respuesta correctamente
        respuesta = response.choices[0].message.content

        # ✅ Agregar la respuesta al historial
        st.session_state["messages"].append({"role": "assistant", "content": respuesta})

        # ✅ Mostrar respuesta
        st.write("**Chatbot:**", respuesta)
    
    except Exception as e:
        st.error(f"⚠️ Error al llamar a OpenAI: {str(e)}")

# ✅ Mostrar historial de conversación
st.subheader("Historial de Conversación")
for message in st.session_state["messages"]:
    if message["role"] != "system":  # Omitir mensajes del sistema
        st.write(f"**{message['role'].capitalize()}**: {message['content']}")
