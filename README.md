# Recipe Management API

This is a Django REST Framework API for managing recipes.

## Features
- User authentication (Token Authentication)
- CRUD operations for recipes
- Categorize recipes
- Add ingredients to recipes

## Tech Stack
- Python
- Django
- Django REST Framework
- SQLite (development)

## Setup Instructions

### 1. Clone the repo
```bash
git clone https://github.com/MaudleenTech/Recipe-Management-API
cd Recipe_Management_API

2. Create and activate virtual environment
python -m venv venv
source venv/Scripts/activate

3. Install dependencies
pip install -r requirements.txt

4. Run migrations
python manage.py migrate

5. Run the server
python manage.py runserver

API Base URL
http://127.0.0.1:8000/api/