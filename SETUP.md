# ProfileGen Setup Instructions

## Project Overview
ProfileGen is a Django web application that allows users to generate professional profiles by:
1. Uploading a PDF resume and automatically extracting information
2. Manually filling out a form with personal details

## Quick Setup

### 1. Prerequisites
- Python 3.8+ installed

### 2. Create Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply Database Migrations
```bash
python manage.py migrate
```

### 5. Run the Application
```bash
python manage.py runserver 8080
```

### 6. Access the Application
Open your web browser and go to: `http://127.0.0.1:8080`

## Features
- **Homepage**: Overview of the application with modern UI
- **Form**: Manual entry of profile information
- **File Upload**: Upload PDF resume for automatic parsing
- **Dashboard**: View extracted profile information with improved readability

## Enhanced OCR Features
- **Smart Text Extraction**: Uses PyPDF2 with improved error handling
- **Section Detection**: Automatically identifies Education, Experience, Skills, and Projects
- **Projects Handling**: Projects are correctly placed in the Experience section
- **Contact Information**: Extracts name, email, and phone number with validation

## Project Structure
- `HRMS/`: Django project settings
- `Home/`: Main application with views, models, and URLs
- `templates/`: HTML templates
- `static/`: CSS, JavaScript, and image assets
- `files/`: Directory for uploaded resume files (auto-created)

## Dependencies
- Django 4.1.5
- PyPDF2 3.0.1
- Pillow 9.1.0

## Database
The project uses SQLite database (`db.sqlite3`) which is created automatically when migrations are applied.

## File Support
- **PDF**: Primary format for resume uploads
- **Validation**: Only PDF files are accepted for upload

## Troubleshooting
- If port 8080 is in use, try a different port: `python manage.py runserver 8081`
- Ensure the virtual environment is activated before running commands
- Check that all dependencies are installed: `pip list`
- For migration issues, try: `python manage.py makemigrations` then `python manage.py migrate`
