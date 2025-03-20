import streamlit as st
import openai

# Configurar la API Key (Reemplázala con tu clave real)
openai.api_key = "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"

# Configuración de la página
st.set_page_config(page_title="Chatbot ISO 55001", page_icon="🤖")
st.title("Chatbot de Gestión de Activos - ISO 55001")

# Inicializar historial de conversación si no existe
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "Eres un experto en gestión de activos basado en la ISO 55001."}
    ]

# Selección del modelo para optimización de costos
model = st.radio("Selecciona el modelo GPT:", ("gpt-4-turbo", "gpt-3.5-turbo"))

# Entrada del usuario
pregunta = st.text_input("Haz una pregunta sobre la ISO 55001:")
if st.button("Enviar") and pregunta:
    
    # Agregar la pregunta al historial
    st.session_state["messages"].append({"role": "user", "content": pregunta})
    
    # Llamar a la API de OpenAI
    response = openai.client.chat.completions.create(
        model=model,
        messages=st.session_state["messages"],
        max_tokens=500  # Limitar tokens para optimizar costos
    )
    
    respuesta = response["choices"][0]["message"]["content"]
    
    # Agregar la respuesta al historial
    st.session_state["messages"].append({"role": "assistant", "content": respuesta})
    
    # Mostrar respuesta
    st.write("**Chatbot:**", respuesta)

# Mostrar historial de conversación
st.subheader("Historial de Conversación")
for message in st.session_state["messages"]:
    if message["role"] != "system":  # Omitir mensajes del sistema
        st.write(f"**{message['role'].capitalize()}**: {message['content']}")
