# 🗄️ StackMind - Database Schema

This document outlines the relational database schema for the StackMind backend. The database is powered by **PostgreSQL** (hosted on Supabase) and managed via SQLAlchemy ORM.

## Entity Relationship Overview

- A **User** can create multiple **Questions** (1:N).
- A **User** can write multiple **Answers** (1:N).
- A **Question** can have multiple **Answers** (1:N). 
  - *Cascade Delete Rule:* If a Question is deleted, all its related Answers are automatically deleted (orphan removal).

---

## Tables

### 1. `users`

Stores user authentication details, profile information, and forum gamification metrics.

| Column Name       | Data Type    | Constraints             | Description                                           |
|:----------------- |:------------ |:----------------------- |:----------------------------------------------------- |
| `id`              | Integer      | **Primary Key**, Index  | Unique identifier for the user.                       |
| `email`           | String       | Unique, Index, Not Null | User's email address for login.                       |
| `hashed_password` | String       | Not Null                | Bcrypt hashed password.                               |
| `username`        | String       | Unique, Index, Not Null | Unique alias/display name in the forum.               |
| `full_name`       | String       | Nullable                | User's real name (optional).                          |
| `avatar_url`      | String       | Nullable                | URL pointing to the user's profile picture.           |
| `reputation`      | Integer      | Default: 0              | Total reputation points earned via upvotes.           |
| `is_active`       | Boolean      | Default: True           | Soft-delete flag. False means account is deactivated. |
| `created_at`      | DateTime(tz) | Default: `now()`        | Timestamp of account creation.                        |

### 2. `questions`

Stores the questions posted by users. Includes a view counter for analytics.

| Column Name  | Data Type    | Constraints                  | Description                                  |
|:------------ |:------------ |:---------------------------- |:-------------------------------------------- |
| `id`         | Integer      | **Primary Key**, Index       | Unique identifier for the question.          |
| `title`      | String(200)  | Not Null                     | The headline/summary of the question.        |
| `body`       | Text         | Not Null                     | The full detailed content of the question.   |
| `views`      | Integer      | Default: 1, Not Null         | Counter for how many times it has been read. |
| `author_id`  | Integer      | **Foreign Key** (`users.id`) | Links to the User who created the question.  |
| `created_at` | DateTime(tz) | Default: `now()`             | Timestamp of question publication.           |

### 3. `answers`

Stores the responses to questions. Includes the rating system for gamification.

| Column Name    | Data Type    | Constraints                      | Description                                         |
|:-------------- |:------------ |:-------------------------------- |:--------------------------------------------------- |
| `id`           | Integer      | **Primary Key**, Index           | Unique identifier for the answer.                   |
| `body`         | Text         | Not Null                         | The main content/solution provided.                 |
| `main_concept` | Text         | Nullable (Max: 60)               | A brief summary/tag of the answer's core topic.     |
| `rating`       | Integer      | Default: 0                       | Total score calculated from user votes (1-4 scale). |
| `author_id`    | Integer      | **Foreign Key** (`users.id`)     | Links to the User who wrote the answer.             |
| `question_id`  | Integer      | **Foreign Key** (`questions.id`) | Links to the parent Question.                       |
| `created_at`   | DateTime(tz) | Default: `now()`                 | Timestamp of answer publication.                    |

-------------

# 🗄️ StackMind - Esquema de Base de Datos

Este documento detalla el esquema de la base de datos relacional para el backend de StackMind. La base de datos utiliza **PostgreSQL** (alojada en Supabase) y se gestiona a través del ORM SQLAlchemy.

## Resumen de Relaciones (Entidad-Relación)

- Un **Usuario** puede crear múltiples **Preguntas** (1:N).
- Un **Usuario** puede escribir múltiples **Respuestas** (1:N).
- Una **Pregunta** puede tener múltiples **Respuestas** (1:N). 
  - *Regla de Borrado en Cascada:* Si se elimina una Pregunta, todas sus Respuestas asociadas se eliminan automáticamente de la base de datos.

---

## Tablas

### 1. `users` (Usuarios)

Almacena los datos de autenticación, el perfil del usuario y las métricas de gamificación del foro.

| Nombre de Columna | Tipo de Dato | Restricciones           | Descripción                                            |
|:----------------- |:------------ |:----------------------- |:------------------------------------------------------ |
| `id`              | Integer      | **Primary Key**, Index  | Identificador único del usuario.                       |
| `email`           | String       | Unique, Index, Not Null | Correo electrónico de acceso.                          |
| `hashed_password` | String       | Not Null                | Contraseña encriptada con Bcrypt.                      |
| `username`        | String       | Unique, Index, Not Null | Alias único del usuario en el foro.                    |
| `full_name`       | String       | Nullable                | Nombre real del usuario (opcional).                    |
| `avatar_url`      | String       | Nullable                | URL de la imagen de perfil.                            |
| `reputation`      | Integer      | Default: 0              | Puntos de reputación ganados por votos.                |
| `is_active`       | Boolean      | Default: True           | Control de baja. 'False' significa cuenta desactivada. |
| `created_at`      | DateTime(tz) | Default: `now()`        | Fecha y hora de creación de la cuenta.                 |

### 2. `questions` (Preguntas)

Almacena las preguntas publicadas por los usuarios. Incluye un contador de visitas para analíticas.

| Nombre de Columna | Tipo de Dato | Restricciones                | Descripción                               |
|:----------------- |:------------ |:---------------------------- |:----------------------------------------- |
| `id`              | Integer      | **Primary Key**, Index       | Identificador único de la pregunta.       |
| `title`           | String(200)  | Not Null                     | El título o resumen principal de la duda. |
| `body`            | Text         | Not Null                     | El contenido detallado de la pregunta.    |
| `views`           | Integer      | Default: 1, Not Null         | Contador de cuántas veces ha sido leída.  |
| `author_id`       | Integer      | **Foreign Key** (`users.id`) | Enlace al Usuario creador de la pregunta. |
| `created_at`      | DateTime(tz) | Default: `now()`             | Fecha y hora de publicación.              |

### 3. `answers` (Respuestas)

Almacena las respuestas aportadas. Incluye el sistema de puntuación para la gamificación.

| Nombre de Columna | Tipo de Dato | Restricciones                    | Descripción                                             |
|:----------------- |:------------ |:-------------------------------- |:------------------------------------------------------- |
| `id`              | Integer      | **Primary Key**, Index           | Identificador único de la respuesta.                    |
| `body`            | Text         | Not Null                         | El contenido principal de la solución.                  |
| `main_concept`    | Text         | Nullable (Max: 60)               | Breve resumen o etiqueta del concepto principal.        |
| `rating`          | Integer      | Default: 0                       | Puntuación total calculada a través de los votos (1-4). |
| `author_id`       | Integer      | **Foreign Key** (`users.id`)     | Enlace al Usuario que redactó la respuesta.             |
| `question_id`     | Integer      | **Foreign Key** (`questions.id`) | Enlace a la Pregunta a la que pertenece.                |
| `created_at`      | DateTime(tz) | Default: `now()`                 | Fecha y hora de publicación.                            |

---
