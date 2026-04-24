""" 

    Generador de Tags en Base al body (Json) de la Respuesta
    
"""

import re 
from collections import Counter

# Lista Blanca  -> Solo aceptamos estas palabras como Tags
# abarcar IA, herramientas, profesiones y negocios -> usuarios no técnicos
# Lista Blanca (Whitelist) -> Solo aceptamos estas palabras como Tags
# Lista Blanca (Whitelist) -> Solo aceptamos estas palabras como Tags
# Mega-diccionario optimizado para StackMind (Técnicos + No Técnicos + Casos de Uso)
ALLOWED_TAGS = {
    # MODELOS, EMPRESAS Y MARCAS IA
    "ia", "ai", "chatgpt", "gpt-3", "gpt-4", "gpt-4o", "gemini", "copilot", 
    "claude", "anthropic", "midjourney", "dalle", "stable-diffusion", 
    "llama", "meta", "mistral", "huggingface", "perplexity", "sora", 
    "runway", "elevenlabs", "heygen", "suno", "udio", "cursor", "openai", 
    "google", "microsoft", "apple-intelligence",

    # CONCEPTOS CLAVE DE INTELIGENCIA ARTIFICIAL (Técnicos y Divulgativos)
    "prompt", "prompts", "prompting", "prompt-engineering", "bot", "asistente", 
    "agente", "agentes", "algoritmo", "tokens", "llm", "nlp", "machine-learning", 
    "deep-learning", "redes-neuronales", "dataset", "entrenamiento", "inferencia", 
    "alucinacion", "sesgo", "fine-tuning", "rag", "contexto", "parametros", 
    "open-source", "codigo-abierto", "agi", "api-key",

    # TECNOLOGÍA, PROGRAMACIÓN Y DESPLIEGUE (Para los que se animan a programar)
    "python", "javascript", "js", "typescript", "html", "css", "sql", "react", 
    "angular", "vue", "node", "api", "backend", "frontend", "fullstack", 
    "base-de-datos", "postgres", "sqlite", "mysql", "mongodb", "github", 
    "git", "docker", "aws", "azure", "google-cloud", "render", "vercel", 
    "supabase", "firebase", "vscode", "jupyter", "colab", "json",

    #  HERRAMIENTAS DEL DÍA A DÍA, OFIMÁTICA Y NO-CODE
    "excel", "word", "powerpoint", "office", "windows", "mac", "linux", "ios", 
    "android", "google-docs", "sheets", "workspace", "notion", "canva", "figma", 
    "photoshop", "premiere", "zapier", "make", "n8n", "trello", "asana", "slack", 
    "discord", "wordpress", "shopify", "app", "web", "navegador", "extension", "plugin",

    #  CASOS DE USO Y ACCIONES
    "productividad", "creatividad", "automatizacion", "automatizar", "resumen", 
    "traduccion", "traducir", "redaccion", "escribir", "copywriting", "texto", 
    "imagenes", "fotografia", "audio", "musica", "video", "analisis", "datos", 
    "analitica", "seo", "investigacion", "estudiar", "aprender", "programar", 
    "diseño", "dibujar", "voz",

    # PROFESIONES, SECTORES Y NEGOCIOS 
    "marketing", "ventas", "ecommerce", "finanzas", "contabilidad", "educacion", 
    "emprendedor", "pyme", "pymes", "startup", "negocio", "empresa", "profesor", 
    "estudiante", "abogado", "medico", "ingeniero", "arquitecto", "diseñador", 
    "programador", "desarrollador", "marketer", "ceo", "rrhh", "recursos-humanos", 
    "periodista", "escritor", "creador-de-contenido", "youtuber", "influencer", "salud", "legal",

    # DUDAS COMUNES, TROUBLESHOOTING Y CONCEPTOS DE COMUNIDAD
    "error", "bug", "fallo", "solucion", "ayuda", "tutorial", "guia", "curso", 
    "precio", "gratis", "premium", "suscripcion", "limite", "privacidad", 
    "seguridad", "legalidad", "copyright", "derechos-de-autor", "alternativa", 
    "comparativa", "cual-es-mejor", "integracion", "comunidad", "principiante", "experto"
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