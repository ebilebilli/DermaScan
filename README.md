# 🏥 DermaScan - AI-Powered Skin Diagnosis Platform

<div align="center">

![Python](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.2-green?style=for-the-badge&logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?style=for-the-badge&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-7-red?style=for-the-badge&logo=redis&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-5.4-green?style=for-the-badge&logo=celery&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-blue?style=for-the-badge&logo=docker&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-purple?style=for-the-badge&logo=openai&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-Authentication-orange?style=for-the-badge&logo=jsonwebtokens&logoColor=white)

</div>


## 🎯 Overview

DermaScan is a platform that uses AI and computer vision to provide basic skin condition assessments. Users can upload skin images and get AI-generated diagnoses, product recommendations, and expert advice.

The project is currently in development, and the AI model will offer more accurate visual analysis in the future.
## ✨ Features

### 🔬 AI-Powered Diagnosis
- **Skin Image Analysis**: Upload skin images for AI analysis
- **Condition Detection**: Identify various skin conditions with confidence scores
- **Medical Descriptions**: Receive detailed, user-friendly explanations of detected conditions
- **GPT-4o Integration**: Advanced language model for comprehensive medical responses

### 👤 User Management
- **Custom User Model**: Extended user profiles with medical history
- **JWT Authentication**: Secure token-based authentication system
- **Social Authentication**: Google OAuth integration
- **User Dashboard**: Personalized health tracking and history

### 💬 Interactive Chat System
- **AI Dermatologist Chat**:Conversation with AI
- **Message History**: Persistent chat conversations
- **Contextual Responses**: AI responses based on user message and uploaded images

### 🛍️ Product Recommendations
- **Personalized Suggestions**: AI-driven product recommendations based on diagnosis
- **Condition-Specific Products**: Curated product lists for different skin conditions
- **User Preferences**: Customizable recommendation algorithms

### 🔧 Technical Features
- **RESTful API**: Comprehensive API endpoints for all functionality
- **Async Processing**: Celery-based background task processing
- **API Documentation**: Interactive Swagger/OpenAPI documentation

## 🛠️ Technology Stack

### Backend
- **Python 3.13**: Latest Python version for optimal performance
- **Django 5.2**: High-level web framework for rapid development
- **Django REST Framework**: Powerful toolkit for building Web APIs
- **Celery 5.4**: Distributed task queue for background processing
- **PostgreSQL 15**: Robust, open-source relational database
- **Redis 7**: In-memory data structure store for caching and message brokering

### AI & Machine Learning
- **OpenAI GPT-4o**: State-of-the-art language model for medical responses
- **Pillow**: Python Imaging Library for image processing
- **Custom AI Models**: Specialized models for skin condition detection

### Authentication & Security
- **JWT (JSON Web Tokens)**: Stateless authentication mechanism
- **Django Allauth**: Comprehensive authentication system
- **Google OAuth**: Social authentication integration

### DevOps & Deployment
- **Docker & Docker Compose**: Containerized application deployment
- **Gunicorn**: WSGI HTTP Server for production deployment
- **Health Checks**: Automated service health monitoring
- **Environment Management**: Secure configuration management

### Development Tools
- **Swagger/OpenAPI**: Interactive API documentation
- **Django Extensions**: Enhanced development utilities
- **Pipenv**: Dependency management and virtual environment
- **Git**: Version control system

## 🏗️ Architecture

```
DermaScan/
├── derma_scan/                 # Main Django project
│   ├── derma_scan/            # Project settings and configuration
│   ├── users/                 # Custom user management
│   ├── scans/                 # Skin image processing, diagnosis and product recommendation
│   ├── chats/                 # AI chat system
│   ├── ai/                    # AI task processing
│   └── apis/                  # REST API endpoints
│   
├── docker-compose.yml         # Multi-container orchestration
├── requirements.txt           # Python dependencies
├── Pipfile                    # Pipenv dependency management
└── README.md                  # Project documentation
```

### Service Architecture
- **Web Service**: Django application with Gunicorn
- **Celery Worker**: Background task processing
- **PostgreSQL Database**: Primary data storage
- **Redis**: Caching and message broker

