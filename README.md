# Personal Portfolio Website

![GitHub last commit](https://img.shields.io/github/last-commit/jimmyMsh/PE-portfolio)
![GitHub license](https://img.shields.io/github/license/jimmyMsh/PE-portfolio)

## Overview
This is a full-stack personal portfolio website developed with Flask and Jinja, designed to showcase my production engineering skills. The project was created as part of the MLH Fellowship in collaboration with Meta, demonstrating proficiency in full-stack development, Docker containerization, and CI/CD pipelines.

## Features
- **Full-Stack Web Application**: Built using Flask, Jinja, and MySQL.
- **Containerized Deployment**: Deployed using Docker and orchestrated with Docker Compose.
- **CI/CD Integration**: Automated testing and deployment pipelines via GitHub Actions.
- **Interactive Frontend**: Responsive design with Bulma CSS and interactive elements using JavaScript.
- **API Endpoints**: RESTful API for managing timeline posts.
- **Secure Deployment**: NGINX configured as a reverse proxy with SSL termination.

## Tech Stack
- **Backend**: Flask, Jinja, Python
- **Frontend**: Bulma CSS, Leaflet.js, JavaScript
- **Database**: MySQL with Peewee ORM
- **Containerization**: Docker, Docker Compose
- **Web Server**: NGINX with SSL via Certbot
- **CI/CD**: GitHub Actions
- **Testing**: Python `unittest`, Bash scripts for E2E testing

## Architecture
The application follows a microservices architecture:
1. **Flask Application**: Handles routing, API endpoints, and serves the frontend.
2. **MySQL Database**: Stores timeline posts and user data.
3. **Nginx**: Acts as a reverse proxy and handles SSL termination.
4. **Certbot**: Automates the process of obtaining and renewing Let's Encrypt SSL certificates.

## CI/CD and Security Features

GitHub Actions workflows are set up for:

- **Continuous Integration**: Runs tests on every push and pull request.
- **Continuous Deployment**: Automatically deploys to VPS on successful merge to the `main` branch.

Security features include:

- **Rate limiting** on API endpoints.
- **Secure handling** of environment variables.
- **SSL/TLS encryption** using Let's Encrypt.

## Project Structure

- **[`app/`](app/)**: Contains the main Flask application code.
  - **[`__init__.py`](app/__init__.py)**: Initializes the Flask app and its configurations.
  - **[`static/`](app/static/)**: Contains static files.
    - **[`img/`](app/static/img/)**: Icons and images.
    - **[`js/`](app/static/js/)**: JavaScript files.
    - **[`styles/`](app/static/styles/)**: CSS files.
  - **[`templates/`](app/templates/)**: Jinja2 templates for rendering HTML.
- **[`scripts/`](scripts/)**: Bash scripts for automation tasks like testing and deployment.
- **[`Dockerfile`](Dockerfile)**: Dockerfile for building the application image.
- **[`docker-compose.prod.yml`](docker-compose.prod.yml)**: Docker Compose configuration for production.
- **[`docker-compose.local.yml`](docker-compose.local.yml)**: Docker Compose configuration for local development.
- **[`tests/`](tests/)**: Unit tests for the application.
- **[`.github/workflows/`](.github/workflows/)**: Contains GitHub Actions workflows for CI/CD.
  - **[`deploy.yaml`](.github/workflows/deploy.yaml)**: Workflow for deploying the application to a VPS.
  - **[`test.yaml`](.github/workflows/test.yaml)**: Workflow for running automated tests.
- **[`user_conf.d/`](user_conf.d/)**: Custom NGINX configuration files.
  - **[`myportfolio.conf`](user_conf.d/myportfolio.conf)**: NGINX configuration for rate limiting and SSL setup.


## Getting Started
### Prerequisites
- Docker and Docker Compose installed.

1. Clone the repository:

    ```bash
    git clone https://github.com/jimmyMsh/PE-portfolio.git
    cd PE-portfolio
    ```

2. Create a `.env` file in the root directory with the variables defined in the [`example.env`](example.env) file.

3. Build and run the Docker container with the `docker-compose.local.yml` file in the root directory:

    ```bash
    docker compose -f docker-compose.local.yml up --build
    ```

4. Access the application at `http://localhost:5000`.

    > **Note:** This setup bypasses Nginx and runs the Flask application directly, making it easier to test locally without SSL configuration.

5. To stop the application, use:

    ```bash
    docker compose -f docker-compose.local.yml down
    ```

    > **Note:** This local setup is for development purposes only. For production deployment, use the original `docker-compose.prod.yml` configuration with proper SSL and Nginx setup.


## Acknowledgements

- **MLH Fellowship Program**: For providing the opportunity to develop this project.
- **Meta**: For guidance and support during the project.
