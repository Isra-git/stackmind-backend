# StackMind - Backend API 🧠

This repository contains the backend service for **StackMind**, an AI-focused community forum built to help non-technical users implement Artificial Intelligence in their daily lives. 

This project was developed as the Capstone Project for the Devcamp Full-Stack Bootcamp.

## 🚀 Overview

The API provides a complete StackOverflow-style Q&A system. It handles user authentication, question and answer management, a reputation point system, and native PostgreSQL full-text search. 

Additionally, it integrates an **AI Writing Assistant** powered by Groq (Llama 3) to help users format and improve their questions before publishing.

## 🛠️ Tech Stack

* **Framework:** FastAPI (Python)
* **Database:** PostgreSQL (Hosted on Supabase)
* **ORM:** SQLAlchemy
* **Authentication:** JWT (JSON Web Tokens) & bcrypt password hashing
* **AI Integration:** Groq API (Llama-3.3-70b-versatile model)
* **Deployment:** Render

## ✨ Key Features

* **Secure Authentication:** User registration and login using JWT bearer tokens.
* **Q&A Engine:** Full CRUD operations for questions and answers.
* **Reputation System:** Users gain or lose reputation points based on how others rate their answers (1-4 scale).
* **View Counter:** Automatically tracks how many times a question has been viewed.
* **Full-Text Search:** Optimized Spanish search engine using PostgreSQL's native `tsvector` and `tsquery`.
* **Magic AI Button:** An endpoint that receives raw user text and returns a professional, well-structured question ready to be posted.

## 💻 Local Setup & Installation

Follow these steps to run the backend locally on your machine.

**1. Clone the repository**

```bash
git clone [https://github.com/Isra-git/stackmind-backend.git](https://github.com/Isra-git/stackmind-backend.git)
cd stackmind-backend
```

**2. Create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Environment Variables**
Create a `.env` file in the root directory and add the following keys:

```text
DATABASE_URL=postgresql://<user>:<password>@<host>:5432/<db_name>
JWT_SECRET=your_super_secret_jwt_string
ALGORITHM=HS256
GROQ_API_KEY=your_groq_api_key_here
```

**5. Run the development server**

```bash
fastapi dev main.py
```

*The API will be available at `http://127.0.0.1:8000`*

## 📚 API Documentation

Please refer to the `API_DOCS.md` file (or the Postman collection provided in the `/docs` folder) for detailed endpoint usage.


