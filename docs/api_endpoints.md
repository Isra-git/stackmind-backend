# 📚 StackMind API - Endpoint Documentation (Postman Style)

> **Note for Frontend Developers:** > - The `{{base_url}}` variable in production is `https://stackmind-api.onrender.com`.
> 
> - For local development, use `http://127.0.0.1:8000`.
> - All protected endpoints require sending the JWT token in the **Headers** tab as: `Authorization: Bearer <your_token>`.

---

## 📁 1. Authentication (Auth)

### 🟢 User Registration

Creates a new user in the database.

- **Method:** `POST`
- **URL:** `{{base_url}}/auth/register`
- **Auth Required:** No

**Body (raw JSON):**

```json
{
  "email": "new@user.com",
  "username": "coder_junior",
  "full_name": "John Doe",
  "avatar_url": "[https://image-link.com/avatar.png](https://image-link.com/avatar.png)",
  "password": "MySecurePassword123"
}
```

**Response 201 (Created):** Returns the user data (excluding the password).
**Response 400 (Bad Request):** If the email or username is already registered.

---

### 🟢 User Login

Validates credentials and returns the JWT Access Token. *Note: Since this uses FastAPI's OAuth2, the body must be sent as Form-Data, not JSON.*

- **Method:** `POST`
- **URL:** `{{base_url}}/auth/login`
- **Auth Required:** No
- **Headers:** `Content-Type: application/x-www-form-urlencoded`

**Body (x-www-form-urlencoded):**

- `username`: new@user.com *(Yes, the key is called username even if you send the email)*
- `password`: MySecurePassword123

**Response 200 (OK):**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR...",
  "token_type": "bearer"
}
```

---

## 📁 2. Users

### 🔵 Get My Profile

Returns the logged-in user's data using their token.

- **Method:** `GET`
- **URL:** `{{base_url}}/auth/me`
- **Auth Required:** Yes (Bearer Token)

**Response 200 (OK):**

```json
{
  "email": "new@user.com",
  "username": "coder_junior",
  "full_name": "John Doe",
  "avatar_url": "https://...",
  "id": 1,
  "reputation": 0,
  "is_active": true,
  "created_at": "2026-03-28T20:00:00Z"
}
```

---

## 📁 3. Questions

### 🟢 Create a Question

Publishes a new question in the forum.

- **Method:** `POST`
- **URL:** `{{base_url}}/questions/`
- **Auth Required:** Yes (Bearer Token)

**Body (raw JSON):**

```json
{
  "title": "How do I start with Python?",
  "body": "I have no technical background and I want to learn AI..."
}
```

### 🔵 Get All Questions

Retrieves the main forum feed. Supports pagination.

- **Method:** `GET`
- **URL:** `{{base_url}}/questions/?skip=0&limit=20`
- **Auth Required:** No

### 🔵 Full-Text Search

Searches for keywords in question titles and bodies.

- **Method:** `GET`
- **URL:** `{{base_url}}/questions/search?query=learn`
- **Auth Required:** No

### 🔵 Read a Question (by ID)

Fetches the details of a specific question and automatically **adds +1 to its view counter**.

- **Method:** `GET`
- **URL:** `{{base_url}}/questions/1`
- **Auth Required:** No

---

## 📁 4. Answers

### 🟢 Answer a Question

Adds a response to an existing question.

- **Method:** `POST`
- **URL:** `{{base_url}}/answers/question/1` *(Where '1' is the Question ID)*
- **Auth Required:** Yes (Bearer Token)

**Body (raw JSON):**

```json
{
  "body": "I highly recommend starting with basic syntax...",
  "main_concept": "Basic Syntax"
}
```

### 🔵 Read Answers for a Question

Retrieves the discussion thread for a specific question.

- **Method:** `GET`
- **URL:** `{{base_url}}/answers/question/1?skip=0&limit=10`
- **Auth Required:** No

### 🟢 Vote on an Answer

Gamification: Awards points to the answer and reputation to its author.

- **Method:** `POST`
- **URL:** `{{base_url}}/answers/1/vote` *(Where '1' is the Answer ID)*
- **Auth Required:** Yes (Bearer Token)

**Body (raw JSON):**

```json
{
  "score": 4 
}
```

*(Note: The `score` must be an integer between 1 and 4. You cannot vote on your own answers).*

---

## 📁 5. Artificial Intelligence (AI)

### 🟢 Magic Button (Enhance Writing)

Sends raw, poorly formatted text to the AI (Llama 3) and returns a well-structured question.

- **Method:** `POST`
- **URL:** `{{base_url}}/ai/enhance-question`
- **Auth Required:** Yes (Bearer Token)

**Body (raw JSON):**

```json
{
  "raw_text": "hi how do i make chatgpt summarize a huge pdf that doesnt fit?"
}
```

**Response 200 (OK):**

```json
{
  "enhanced_text": "I am trying to use ChatGPT to summarize a large PDF file, but it exceeds the allowed character limit. \nWhat tools or strategies would you recommend for processing extensive documents with AI?"
}
```

--------------------------

# 📚 StackMind API - Documentación de Endpoints (Postman Style)

> **Nota para Frontend:** > - La variable `{{base_url}}` en producción es `https://stackmind-api.onrender.com`.
> 
> - En desarrollo local, usa `http://127.0.0.1:8000`.
> - Todos los endpoints protegidos requieren enviar el token JWT en la pestaña **Headers** como: `Authorization: Bearer <tu_token>`.

---

## 📁 1. Autenticación (Auth)

### 🟢 Registro de Usuario

Crea un usuario nuevo en la base de datos.

- **Método:** `POST`
- **URL:** `{{base_url}}/auth/register`
- **Auth Requerida:** No

**Body (raw JSON):**

```json
{
  "email": "nuevo@usuario.com",
  "username": "coder_junior",
  "full_name": "Juan Pérez",
  "avatar_url": "[https://link-a-imagen.com/avatar.png](https://link-a-imagen.com/avatar.png)",
  "password": "MiPasswordSeguro123"
}
```

**Respuesta 201 (Created):** Devuelve los datos del usuario sin la contraseña.
**Respuesta 400 (Bad Request):** Si el email o el username ya existen.

---

### 🟢 Iniciar Sesión (Login)

Valida las credenciales y devuelve el Token JWT. *Ojo: Como usa OAuth2 de FastAPI, el body va en formato Form-Data, no en JSON.*

- **Método:** `POST`
- **URL:** `{{base_url}}/auth/login`
- **Auth Requerida:** No
- **Headers:** `Content-Type: application/x-www-form-urlencoded`

**Body (x-www-form-urlencoded):**

- `username`: nuevo@usuario.com *(Sí, la clave se llama username aunque envíes el email)*
- `password`: MiPasswordSeguro123

**Respuesta 200 (OK):**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR...",
  "token_type": "bearer"
}
```

---

## 📁 2. Usuarios (Users)

### 🔵 Obtener mi perfil

Devuelve los datos del usuario logueado usando su token.

- **Método:** `GET`
- **URL:** `{{base_url}}/auth/me`
- **Auth Requerida:** Sí (Bearer Token)

**Respuesta 200 (OK):**

```json
{
  "email": "nuevo@usuario.com",
  "username": "coder_junior",
  "full_name": "Juan Pérez",
  "avatar_url": "https://...",
  "id": 1,
  "reputation": 0,
  "is_active": true,
  "created_at": "2026-03-28T20:00:00Z"
}
```

---

## 📁 3. Preguntas (Questions)

### 🟢 Crear una Pregunta

Publica una nueva duda en el foro.

- **Método:** `POST`
- **URL:** `{{base_url}}/questions/`
- **Auth Requerida:** Sí (Bearer Token)

**Body (raw JSON):**

```json
{
  "title": "¿Cómo empiezo con Python?",
  "body": "No tengo experiencia técnica y quiero aprender IA..."
}
```

### 🔵 Obtener todas las Preguntas

Lista el feed principal del foro. Soporta paginación.

- **Método:** `GET`
- **URL:** `{{base_url}}/questions/?skip=0&limit=20`
- **Auth Requerida:** No

### 🔵 Buscador Full-Text

Busca palabras clave en títulos y cuerpos de preguntas.

- **Método:** `GET`
- **URL:** `{{base_url}}/questions/search?query=aprender`
- **Auth Requerida:** No

### 🔵 Leer una Pregunta (por ID)

Obtiene los detalles de una pregunta y le **suma +1 al contador de visitas** automáticamente.

- **Método:** `GET`
- **URL:** `{{base_url}}/questions/1`
- **Auth Requerida:** No

---

## 📁 4. Respuestas (Answers)

### 🟢 Responder a una Pregunta

Añade una respuesta a una pregunta existente.

- **Método:** `POST`
- **URL:** `{{base_url}}/answers/question/1` *(El '1' es el ID de la pregunta)*
- **Auth Requerida:** Sí (Bearer Token)

**Body (raw JSON):**

```json
{
  "body": "Te recomiendo empezar por aprender sintaxis básica...",
  "main_concept": "Sintaxis Básica"
}
```

### 🔵 Leer respuestas de una Pregunta

Obtiene el hilo de respuestas.

- **Método:** `GET`
- **URL:** `{{base_url}}/answers/question/1?skip=0&limit=10`
- **Auth Requerida:** No

### 🟢 Votar una Respuesta

Gamificación: Da puntos a la respuesta y reputación a su autor.

- **Método:** `POST`
- **URL:** `{{base_url}}/answers/1/vote` *(El '1' es el ID de la respuesta)*
- **Auth Requerida:** Sí (Bearer Token)

**Body (raw JSON):**

```json
{
  "score": 4 
}
```

*(Nota: El `score` debe ser un número entero entre el 1 y el 4. No puedes votar tus propias respuestas).*

---

## 📁 5. Inteligencia Artificial (AI)

### 🟢 Botón Mágico (Mejorar Redacción)

Envía un texto mal redactado para que la IA (Llama 3) devuelva una pregunta bien estructurada.

- **Método:** `POST`
- **URL:** `{{base_url}}/ai/enhance-question`
- **Auth Requerida:** Sí (Bearer Token)

**Body (raw JSON):**

```json
{
  "raw_text": "ola como se ase para q chatgpt aga un resumen de un pdf grande q no me entra?"
}
```

**Respuesta 200 (OK):**

```json
{
  "enhanced_text": "Estoy intentando que ChatGPT me resuma un archivo PDF largo, pero supera el límite de texto permitido. \n¿Qué estrategias o herramientas recomendáis para procesar documentos extensos con IA?"
}
```