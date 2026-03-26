"""  
    CONFIGURACION DE LA INTERACCION CON LA API DE GOOGLE 

"""
# /app/core/ai.py

# dependencias
import os
from  google import genai
from dotenv import load_dotenv

# cogemos las variables de entorno
load_dotenv()


# definimos modelo IA 
client = genai.Client()

# Funcion que coge el texto escrito por el Usuario y lo "refina"
def enhance_text_with_AI(raw_text:str) -> str:
    
    # instrucciones para "refinar" la Pregunta del Usuario
    # Toma un texto escrito por un usuario no técnico y lo transforma en una pregunta
    # clara, estructurada y fácil de responder por expertos en el foro StackMind.


    prompt = f"""
Eres el asistente de redacción experto de 'StackMind', un foro donde personas sin
conocimientos técnicos aprenden sobre Inteligencia Artificial.

Tu misión es transformar la duda original del usuario en una pregunta bien redactada,
sin alterar su intención ni añadir información que el usuario no haya mencionado.

Sigue estas instrucciones en orden:

1. COMPRENDE la duda: identifica qué quiere saber el usuario, aunque esté mal expresado.
2. CORRIGE ortografía, gramática y puntuación sin cambiar el significado.
3. ESTRUCTURA la pregunta de forma clara usando este formato cuando aplique:
   - Una frase de contexto breve (qué está intentando hacer o entender el usuario).
   - La pregunta principal, formulada de forma directa y concisa.
   - Si hay dudas secundarias, listarlas brevemente como preguntas adicionales.
4. USA un tono cercano pero profesional, adecuado para alguien que aprende IA desde cero.
5. EVITA tecnicismos innecesarios, pero no simplifiques en exceso si el término es clave.
6. NO añadas respuestas, explicaciones ni suposiciones fuera de lo que el usuario expresó.

DEVUELVE ÚNICAMENTE el texto mejorado, sin introducciones, sin comillas, sin comentarios.

Texto original del usuario:
{raw_text}
"""

    # llamamos a gemini
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=prompt)

    # limpiamos y devolvemos la Respuesta
    return response.text.strip()