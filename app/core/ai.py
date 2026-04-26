# /app/core/ai.py

# dependencias
import os
from  groq import Groq
from dotenv import load_dotenv
import json 

# cogemos las variables de entorno
load_dotenv()


# definimos modelo IA 
client = Groq()

# Funcion que coge el texto escrito por el Usuario y lo "refina"
def enhance_text_with_AI(raw_text:str) -> str:
    
    # instrucciones para "refinar" la Pregunta del Usuario
    # Toma un texto escrito por un usuario no técnico y lo transforma en una pregunta
    # clara, estructurada y fácil de responder por expertos en el foro StackMind.

    prompt = f"""
Eres el asistente de redacción de 'StackMind', una comunidad donde personas SIN conocimientos de programación buscan aplicar herramientas de Inteligencia Artificial en su día a día.

Tu objetivo es leer la duda desordenada de un usuario novato y reescribirla de forma clara y estructurada para que los expertos del foro puedan entender exactamente qué necesita y recomendarle herramientas accesibles (no-code, ChatGPT, Claude, automatizaciones sencillas).

REGLAS ESTRICTAS:
1. NO ASUMAS QUE EL USUARIO SABE PROGRAMAR. No menciones Python, APIs, scripts, Machine Learning, OCR u otras tecnologías a menos que el usuario las haya mencionado explícitamente.
2. Céntrate en el CASO DE USO: Qué tiene el usuario (inputs) y qué quiere conseguir (outputs).
3. Mantén un tono amigable, directo y humano. 
4. No añadas complejidad, requisitos de escalabilidad o detalles que el usuario no haya pedido.

ESTRUCTURA DE SALIDA (JSON ESTRICTO):
Debes devolver tu respuesta EXCLUSIVAMENTE en formato JSON con la siguiente estructura, sin texto adicional antes o después:

{{
  "analisis_interno": "Breve resumen de qué quiere lograr el usuario y su punto de partida.",
  "pregunta_optimizada": "La duda original reformulada de forma directa y clara. Sin títulos ni comillas."
}}

DUDA ORIGINAL DEL USUARIO:
{raw_text}
"""
    # Uilizamos Llama 3 a través de Groq
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile", # gran español
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3, # Bajamos la temperatura para que sea más preciso y menos creativo
        response_format={"type": "json_object"} #devolvemos Json
    )
    # formateamos la respuesta
    response_text = completion.choices[0].message.content.strip()
    
    # devolvemos la Respuesta
    try:
        response_json = json.loads(response_text)
        
        # Devolvemos solo la pregunta optimizada accediendo a la clave del diccionario
        return response_json["pregunta_optimizada"]
        
    except json.JSONDecodeError:
        # Por si acaso la IA falla y no devuelve un JSON válido
        return "Error: La IA no devolvió el formato esperado."