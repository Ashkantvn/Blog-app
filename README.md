# 📝 Django Blog App

A blogging platform built with **Django 5.2.6**.  

It’s designed as a **portfolio-ready** project to showcase backend development, task automation, and clean code practices.

---

## 🚀 Features

- **User Authentication** – Activation, registration, login, and profile management.  
- **Post Management** – Create, update, delete, and view blog posts with media uploads.  
- **Admin Dashboard** – Using Django’s built-in admin panel.  
- **Media Handling** –  Media uploads and cleanup using `Pillow` and `django-cleanup`.  
- **Asynchronous Tasks** – Background processing and scheduled jobs via `Celery` and `Celery-beat`.  
- **Queues** – Integrated `Redis` for fast task queuingt.  
- **Testing & Quality** – Automated tests with `pytest` and `pytest-django`, formatted with `black`, and linted via `flake8`.  
- **Environment Variables** – Secure and flexible settings using `python-decouple`.  
- **Database** – Powered by PostgreSQL for production-grade reliability.

---

## 🛠️ Tech Stack

| Category | Tools Used |
|-----------|-------------|
| **Framework** | Django 5.2.6 |
| **Database** | PostgreSQL |
| **Task Queue** | Celery, Redis, django-celery-beat |
| **Media Handling** | Pillow, django-cleanup |
| **Testing** | pytest |
| **Code Quality** | black, flake8 |
| **Configuration** | python-decouple |
| **Deployment / Server** | Gunicorn, Nginx |


---

## 🏁 License

This project is licensed under the MIT License.
