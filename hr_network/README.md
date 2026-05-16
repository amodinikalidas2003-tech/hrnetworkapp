# HR Network Application (Django)

This project is a comprehensive HR management system built with **Django**.
It includes modules for organization management, dynamic form building, employee assessments, and file archiving.

## Features

- **Organization Management**: Manage departments and employee profiles hierarchically.
- **No-Code Form Builder**: Create dynamic forms (surveys, assessments) with a flexible JSON schema.
- **Assessments**: Evaluate employees based on custom criteria and store scores.
- **File Archive**: Securely upload and manage documents associated with users.
- **HR Dashboard**: Centralized view of key metrics and quick actions.

## Tech Stack

- **Backend/Frontend**: Django 5.0 (MVT Architecture)
- **Database**: SQLite (Default) / PostgreSQL (Recommended for production)
- **Template Engine**: Django Templates + Bootstrap 5 (Vuexy Theme)

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd hr_network
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run migrations:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5.  **Create a superuser:**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```

7.  **Access the application:**
    Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

## Project Structure

- `apps/`: Contains all Django apps.
    - `organization`: Department & Employee models.
    - `forms`: Dynamic form logic (Schema & Submission).
    - `assessments`: Scoring logic.
    - `files`: File management.
    - `hr_dashboard`: Dashboard views.
- `config/`: Project settings and configuration.
- `templates/`: HTML templates (extending the base theme).
- `static/`: Static assets (CSS, JS, Images).

## License

Commercial License (as per Vuexy Template).
