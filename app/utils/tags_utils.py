""" 

    Generador de Tags en Base al body (Json) de la Respuesta
    
"""

import re 
from collections import Counter

# Lista Blanca  -> Solo aceptamos estas palabras como Tags
# abarcar IA, herramientas, profesiones y negocios -> usuarios no técnicos
ALLOWED_TAGS = {
    # Conceptos clave de IA
    "ia", "ai", "chatgpt", "gemini", "copilot", "claude", "midjourney", "dalle",
    "prompt", "prompts", "bot", "asistente", "agente", "algoritmo", "tokens",
    
    # Casos de uso y acciones del día a día
    "productividad", "creatividad", "automatizacion", "resumen", "traduccion",
    "texto", "imagenes", "audio", "video", "analisis", "redaccion",
    
    # Herramientas y Sistemas Operativos
    "excel", "word", "powerpoint", "notion", "canva", "windows", "mac", 
    "linux", "android", "ios", "app", "web", "google", "microsoft","powerpoint", "excel","word", "notion", "canva", "windows", "mac", "linux", "android", "ios", "app", "web
    
    # Negocios, Profesiones y Sectores
    "marketing", "ventas", "seo", "ecommerce", "pymes", "negocio", "finanzas",
    "educacion", "profesor", "abogado", "medico", "diseño", "copywriting",
    "programacion", "recursos-humanos", "rrhh", "estudiante", "salud", "marketing", "diseño", "copywriting", "programacion", "recursos-humanos", "rrhh", "estudiante", "salud"
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
    
    # Expresion Regular -> Pasamos a Minusculas y cogemos palabras
    # [a-záéíóúñ0-9-] acepta 2+ letras, guiones y números para pillar "ia", "rrhh" o "recursos-humanos"
    palabras = re.findall(r'\b[a-záéíóúñ0-9-]{2,}\b', texto_completo.lower())

    # Filtramos dejando SOLO las palabras que estan en la Lista Blanca
    palabras_utiles=[palabra for palabra in palabras if palabra in ALLOWED_TAGS]
    
    # Si la respuesta no tiene Nada INteresante-> Devolvemos algo generico
    if not palabras_utiles:
        return "comunidad, ayuda, tutorial"
    
    # Contamos la Frecuencia y sacamos las 3 mas frecuentes (esto ya asegura que sean unicas)
    mas_comunes=Counter(palabras_utiles).most_common(3)
    
    # formateamos el Resultado -> ['chatgpt','marketing'] -> "chatgpt, marketing"
    tags=[palabra_format for palabra_format, cuenta in mas_comunes]
    resultado=", ".join(tags)
    
    # devolvemos max-> 60 caracteres
    return resultado[:60]

# Ejemplo de uso:
# texto = "Uso ChatGPT para mejorar el marketing de mi pyme y hacer diseño en Canva."
# tags = generar_tags_automaticos([{"type": "paragraph", "content": texto}])
# print(tags) # Output: "chatgpt, marketing, canva"