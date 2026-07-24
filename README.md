# Blog App

This is a Django-based blog application project. It is a test project created for learning, experimentation, and practice with Django, Docker, authentication flows, blog management, and testing.

## Features

- User authentication and account management
- Blog creation, display, and management
- Tag-based blog organization
- Docker-based local development setup
- Automated tests with pytest

## Tech Stack

- Python / Django
- PostgreSQL
- Redis
- Docker Compose
- pytest

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Run locally with Docker

1. Create the required environment files for development if needed.
2. Start the development environment:

   ```bash
   docker compose -f docker-compose.dev.yml up --build
   ```

3. Open the app in your browser at:

   ```text
   http://localhost:8000
   ```

### Run tests

```bash
docker compose -f docker-compose.dev.yml exec django pytest
```

## Note

This repository is a test project and is intended mainly for learning and development purposes.
