# Celebrity AI - Backend (Django REST Framework)

This is the **backend** for the Celebrity AI project. It provides a REST API for user management, celebrity profiles, chat sessions, messaging, and AI integration. The backend is built with **Django REST Framework**, supporting JWT authentication and social logins (Google, Facebook, Discord), with **Django Channels** and **Daphne** for real-time features.

---

## Features

- **User Management**
  - JWT authentication (access + refresh tokens)
  - Social login: Google, Facebook, Discord
  - Users can only see/update/delete their own accounts

- **Celebrity Management**
  - Public and private celebrity profiles
  - Search, filter, and ordering
  - Private celebrities visible only to the creator

- **Chat System**
  - Create chat sessions per celebrity
  - Users can send messages only in their own sessions
  - Real-time AI streaming via SmolAgents + DeepSeek

- **Category Management**
  - CRUD operations for categories

- **AI Integration**
  - DeepSeek + SmolAgents streaming agent
  - Async-safe database access
  - Instructions-based AI responses

---

## Tech Stack

- Python 3.11+
- Django 4.x
- Django REST Framework
- Django Channels (async / WebSocket support)
- Daphne (ASGI server for production)
- SimpleJWT for JWT authentication
- dj-rest-auth + AllAuth for social login
- PostgreSQL (recommended)
- SmolAgents + DeepSeek for AI-powered chat

---

## Getting Started

### Clone the Repository

```bash
git clone https://github.com/<your_username>/celebrity-ai.git
cd celebrity-ai/backend
