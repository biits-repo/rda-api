# RDA API - OCR Media Access API

A Django REST API for accessing PDF and audio files based on ISBN numbers. This API provides endpoints for downloading media files and includes comprehensive API documentation with Swagger/OpenAPI integration.

## Features

- 📚 **PDF File Access**: Download PDF files by ISBN number
- 🎵 **Audio File Access**: Download audio files (MP3) by ISBN number
- 🔐 **Token Authentication**: Secure API access with token-based authentication
- 📖 **API Documentation**: Interactive Swagger UI and ReDoc documentation
- 🚀 **Django REST Framework**: Built with industry-standard DRF
- 📊 **OpenAPI Schema**: Full OpenAPI 3.0 specification support

## Technology Stack

- **Backend**: Django 5.2.3
- **API Framework**: Django REST Framework
- **Documentation**: drf-spectacular (Swagger/OpenAPI)
- **Database**: SQLite (development)
- **Authentication**: Token-based authentication
- **Python**: 3.11+

## Project Structure

```
rda-api/
├── app/                                              # Django application
│   ├── api/                                          # API application
│   │   └── v1/                                       # API version 1
│   │       ├── views.py                              # API endpoints
│   │       ├── serializers.py
│   │       └── urls.py
│   ├── app/                                          # Django project settings
│   ├── docs/                                         # API documentation schemas
│   └── manage.py                                     # Django management script
├── media/                                            # Media files storage
│   ├── pdfs/                                         # PDF files
│   └── audio/                                        # Audio files
├── venv/                                             # Virtual environment
├── .gitignore
└── README.md
```

## Installation

### Prerequisites

- Python 3.11.9
- pip 25.1.1(Python package manager)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd rda-api
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install django djangorestframework drf-spectacular
   ```

4. **Navigate to the app directory**
   ```bash
   cd app
   ```

5. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the development server**
   ```bash
   cd app
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000/`

## API Endpoints

### Base URL
```
http://localhost:8000/
```

### Media Access Endpoints

#### Download PDF
```
POST /api/get-pdf/
```
Download a PDF file by ISBN number.

**Request Body:**
```json
{
    "isbn_number": "1234567890"
}
```

#### Download Audio
```
POST /api/get-audio/
```
Download an audio file by ISBN number.

**Request Body:**
```json
{
    "isbn_number": "1234567890"
}
```

### Documentation Endpoints

- **Swagger UI**: `http://localhost:8000/docs/`
- **ReDoc**: `http://localhost:8000/redoc/`
- **OpenAPI Schema**: `http://localhost:8000/api/schema/`
- **Admin Panel**: `http://localhost:8000/admin/`



### Adding Media Files
Place PDF files in `media/pdfs/` and audio files in `media/audio/` with filenames matching the ISBN format (e.g., `1234567890.pdf`).

## Configuration

### Environment Variables
Create a `.env` file in the project root for environment-specific settings:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Production Settings
For production deployment:
- Set `DEBUG=False`
- Configure a production database (PostgreSQL recommended)
- Set up proper static file serving
- Configure HTTPS
- Set secure `SECRET_KEY`

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
