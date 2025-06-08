# chat_spa_demo.py

import os
import panel as pn
import openai
from datetime import datetime

# Cargar tu API Key
openai.api_key = os.getenv("OPENAI_API_KEY") or "sk-tu_clave_aqui"
client = openai.OpenAI(api_key=openai.api_key)

# Estilo global
pn.extension()

# Prompt inicial
messages = [
    {
        "role": "system",
        "content": (
            "Eres un asistente virtual para un spa de lujo."
            " Tu tono es cálido, profesional y relajante."
            " Puedes informar sobre tratamientos, precios y agendar citas si el cliente proporciona detalles."
        ),
    }
]

# Panel de conversación
conversation_md = pn.pane.Markdown(
    "### 💆‍♀️ Bienvenida a *GlamSpa*\n¿En qué puedo ayudarte hoy?",
    sizing_mode="stretch_both",
    styles={
        "fontSize": "16px",
        "backgroundColor": "#f8f8f8",
        "padding": "12px",
        "border": "1px solid #ddd",
        "borderRadius": "8px",
    },
)

input_box = pn.widgets.TextAreaInput(placeholder="Escribe tu mensaje…", height=120)
send_button = pn.widgets.Button(name="Enviar 💬", button_type="primary", width=100)
clear_button = pn.widgets.Button(name="Nuevo chat 🔄", button_type="warning", width=120)

# Función para obtener respuesta

def get_ai_response(user_text):
    messages.append({"role": "user", "content": user_text})
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7,
            max_tokens=500,
        )
        reply = response.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})
        return reply
    except Exception as e:
        return f"Error: {e}"

# Callbacks

def send_callback(event):
    user_text = input_box.value.strip()
    if not user_text:
        return
    conversation_md.object += f"\n\n**🧑‍💻 Cliente:** {user_text}"
    input_box.value = ""
    reply = get_ai_response(user_text)
    conversation_md.object += f"\n\n**🤖 GlamBot:** {reply}"

def clear_callback(event):
    global messages
    messages = messages[:1]  # solo system
    conversation_md.object = "### 💆‍♀️ Bienvenida a *GlamSpa*\n¿En qué puedo ayudarte hoy?"
    input_box.value = ""

send_button.on_click(send_callback)
clear_button.on_click(clear_callback)

# Layout
app = pn.Column(
    pn.pane.HTML("""
        <h2 style='color:#b30059; text-align:center;'>GlamSpa - Asistente Virtual</h2>
        <p style='text-align:center; font-style:italic;'>Consulta tratamientos, precios y agenda tu cita</p>
    """),
    conversation_md,
    pn.Row(input_box),
    pn.Row(send_button, clear_button),
    sizing_mode="stretch_width",
)

# Servir si se ejecuta como script
if __name__ == "__main__":
    pn.serve(app, port=8000, show=True)
