""" 

    Generador de Tags en Base al body (Json) de la Respuesta
    
"""

import re 
from collections import Counter

# Lista de  palabras que se repiten mucho pero no aportan contexto técnico.
STOPWORDS_ES = {
    "el", "la", "los", "las", "un", "una", "unos", "unas", "y", "o", "pero", "si", 
    "de", "del", "a", "al", "en", "por", "con", "para", "como", "su", "sus", "que", 
    "es", "son", "este", "esta", "esto", "se", "lo", "te", "me", "nos", "mi", "mis", 
    "tu", "tus", "muy", "más", "mas", "sin", "sobre", "ya", "cuando", "donde", "quien", 
    "desde", "hasta", "paso", "ejemplo", "código", "hacer", "puedes", "tiene", "hola",
    "gracias", "saludos", "así", "solo", "también", "hay", "todo", "nada", "bien"
    ,"cómo", "resolver", "duda","seguro", "puede","diferencias","cómo", "resolver", "duda",
    "què"
}

# Analiza los bloques de StackMindEditor y devuelve max -> 3 tags clave
def generar_tags_automaticos(steps:list)-> str:
    
    # extraemos el texto, ignorando los bloques de codigo
    textos=[]
    for step in steps:
        if step.get("type") != "code":
            textos.append(step.get("content", ""))
    
    # unimos todos los textos en una sola cadena
    texto_completo = ' '.join(textos)
    
    # Expresion Regular -> Pasamos a Minusculas y cogemos palabras de 3+ Letras
    # [a-záéíóúñ] asegura que cogemos palabras en español sin números ni símbolos extraños
    palabras = re.findall(r'\b[a-záéíóúñ]{3,}\b', texto_completo.lower())

    # Filtramos las palabras de STOPWOrds
    palabras_utiles=[palabra for palabra in palabras if palabra not in STOPWORDS_ES]
    
    # Si la respuesta no tiene Nada INteresante-> Devolvemos algo generico
    if not palabras_utiles:
        return "solucion, comunidad, ayuda"
    
    # Contamos la Frecuencia y sacamos las 3 mas frecuentes
    mas_comunes=Counter(palabras_utiles).most_common(3)
    
    # formateamos el Resultado -> ['agente','bucle'] -> "agente, bucle"
    tags=[palabra_format for palabra_format, cuenta in mas_comunes]
    resultado=", ".join(tags)
    
    # devolvemos max-> 60 caracteres
    return resultado[:60]

# Ejemplo de uso:
# texto = "Estoyas aprendiendo a programar y tienes dudas sobre cómo hacer un bucle. ¿Podrías ayudarme?"
# tags = get_tags(texto)
# print(tags) # Output: "agente, bucle"