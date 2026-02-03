# Celebrity AI - Backend (Django REST Framework)

![Django](https://img.shields.io/badge/Django-4.x-092E20?logo=django)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql)
![Swagger](https://img.shields.io/badge/Swagger-85EA2D?logo=swagger&logoColor=black)
![License](https://img.shields.io/badge/License-Private-red)

This is the backend for the Celebrity AI project. It provides a REST API for user management, celebrity profiles, chat sessions, messaging, and AI integration. The backend is built with Django REST Framework, supporting JWT authentication and social logins (Google, Facebook, Discord), with Django Channels and Daphne for real-time features.

## 📚 API Documentation
**Interactive API documentation** is available via Swagger/OpenAPI:

- **Swagger UI**: `/swagger/` - Interactive API testing
- **ReDoc**: `/redoc/` - Alternative documentation view
- **OpenAPI Schema**: `/swagger.json` - Machine-readable schema

![Swagger Preview](https://via.placeholder.com/800x400/4A90E2/FFFFFF?text=Swagger+API+Documentation)

## ✨ Features

### 👤 User Management
- JWT authentication (access + refresh tokens)
- Social login: Google, Facebook, Discord
- Users can only see/update/delete their own accounts

### 🌟 Celebrity Management
- Public and private celebrity profiles
- Search, filter, and ordering capabilities
- Private celebrities visible only to the creator

### 💬 Chat System
- Create chat sessions per celebrity
- Users can send messages only in their own sessions
- Real-time AI streaming via SmolAgents + DeepSeek

### 📁 Category Management
- CRUD operations for categories

### 🤖 AI Integration
- DeepSeek + SmolAgents streaming agent
- Async-safe database access
- Instructions-based AI responses

## 🛠️ Tech Stack
- **Backend**: Django 4.x, Django REST Framework
- **API Documentation**: drf-yasg (Swagger/OpenAPI 3.0)
- **Real-time**: Django Channels, Daphne (ASGI server)
- **Database**: PostgreSQL (recommended), SQLite (development)
- **Authentication**: SimpleJWT, dj-rest-auth + AllAuth
- **AI Framework**: SmolAgents + DeepSeek API
- **Task Queue**: Redis (for channels layer)

## 🔌 API Endpoints

### Quick Reference
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/swagger/` | Swagger UI documentation |
| `GET`  | `/redoc/` | ReDoc documentation |

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/auth/login/` | JWT Token pair |
| `POST` | `/api/auth/refresh/` | Refresh token |
| `POST` | `/api/auth/social/` | Social login |

### Celebrities
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/api/celebrities/` | List all celebrities |
| `POST` | `/api/celebrities/` | Create celebrity (admin) |

**Full interactive documentation available at `/swagger/`**

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 14+ (or SQLite for development)
- Redis (recommended for production)

### Installation
```bash
# Clone repository
git clone https://github.com/ZennadAkram/celebrity-ai-backend/
cd celebrity_ai_backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings
