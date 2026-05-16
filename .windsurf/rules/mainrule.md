---
trigger: always_on
---


# Engineering Rules
### Django (Python) Development Standards

This document defines the engineering standards for the HR Network Application using Django.
All generated code and manual contributions must follow these rules.

---

# A. Architecture & Code Structure

## 1. MVT Architecture (Model-View-Template)

The project follows the standard Django MVT pattern:

- **Models (`models.py`)**: Data structure and database interactions.
- **Views (`views.py`)**: Business logic and request handling.
- **Templates (`templates/`)**: Presentation layer (HTML/Django Template Language).
- **URLs (`urls.py`)**: URL routing.
- **Forms (`forms.py`)**: Input validation and HTML form generation.

Avoid putting business logic inside Templates. Keep Views thin by using Services or Model methods where appropriate.

---

## 2. App Structure

Organize functionality into modular Django apps.
Suggested apps:
- `authentication`: User management and auth.
- `organization`: Department and structure management.
- `forms`: Dynamic form builder and renderer (No-Code engine).
- `assessments`: Scoring and evaluation logic.
- `dashboard`: Analytics and reporting.
- `files`: File archiving and management.

---

## 3. Data Models

- Use Django's ORM.
- Use `UUIDField` as primary key for better scalability and security.
- Use `JSONField` (supported in PostgreSQL/SQLite) for dynamic schemas (Form Builder).
- Define `__str__` methods for all models.

---

# B. Internationalization & Messages

## 4. Translation

Use Django's translation system (`gettext`).
- Wrap user-facing strings in `_()` or `gettext_lazy`.
- Maintain `locale/` directories for different languages (en, fa).

---

# C. Security Standards

## 5. Authentication & Authorization

- Use Django's built-in `User` model (extended if necessary) or a custom user model.
- Use `decorators` (`@login_required`, `@permission_required`) for view protection.
- Use Class-Based Views (CBVs) with `LoginRequiredMixin`.

---

## 6. Input Validation

- Always use Django `Forms` or `ModelForms` for data validation.
- Never blindly trust `POST` data.
- CSRF protection is enabled by default; ensure `{% csrf_token %}` is present in all forms.

---

# D. Database & Persistence

## 7. Optimization

- Use `select_related` and `prefetch_related` to avoid N+1 query problems.
- Use database indexes on frequently filtered columns.

---

# E. Code Quality

## 8. Style Guide

- Follow **PEP 8** standards.
- Use meaningful variable and function names.
- Docstrings for complex classes and functions.

---

# F. Frontend Integration (Django Templates)

- Use the provided theme's layout (`base.html`, `auth_base.html`).
- Extend base templates for consistency.
- Use `{% static %}` for loading assets.
- Keep JavaScript logic in separate files or `{% block scripts %}`.

---

اگر دستوری رو می تونی خودت ران کنی، اصلا نباید به من بگی