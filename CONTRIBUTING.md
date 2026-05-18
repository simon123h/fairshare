# Contributing to FairShare CLI

Thank you for your interest in contributing to FairShare CLI! This document provides guidelines for setting up your development environment and contributing to the project.

## Development Setup

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-repo/fairshare.git
    cd fairshare
    ```

2.  **Install dependencies:**
    It is recommended to use a virtual environment.
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

## Quality Assurance

### Tests & Coverage

The project includes unit tests to ensure mathematical correctness and valid data handling.

```bash
# Run tests
python3 -m unittest discover tests

# Check test coverage
coverage run -m unittest discover tests
coverage report -m
```

### Linting & Formatting

We use **Ruff** for fast linting and automatic code formatting. Please ensure your code follows these standards before submitting a pull request.

```bash
# Format code
ruff format .

# Check and fix linting errors
ruff check . --fix
```

## CI/CD Pipeline

The project uses **GitLab CI/CD** and **GitHub Actions**. Each push automatically triggers:

1.  Linting and formatting checks (Ruff).
2.  Unit tests.
3.  Code coverage reports.

Ensure all checks pass in your pull request.
