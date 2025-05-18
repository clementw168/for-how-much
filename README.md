# 🚀 for_how_much

[![Powered by UV](https://img.shields.io/badge/Powered%20by-UV-%2300C2D7)](https://github.com/astral-sh/uv)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![GitHub Template](https://img.shields.io/badge/template-available-brightgreen?logo=github)](https://github.com/clementw168/python-uv-template/generate)
[![CodeQL](https://github.com/clementw168/for-how-much/actions/workflows/codeql.yml/badge.svg)](https://github.com/clementw168/for-how-much/actions)
[![Lint and tests](https://github.com/clementw168/for-how-much/actions/workflows/check_and_tests.yml/badge.svg)](https://github.com/clementw168/for-how-much/actions)
[![Open Issues](https://img.shields.io/github/issues/clementw168/for-how-much)](https://github.com/clementw168/for-how-much/issues)


Game with some friends

---

A game where friends debate about how much they would pay to do something.

## Setup

1. **Prerequisites**
   - Python 3.11+
   - MySQL database
   - UV package manager

2. **Install UV**:
   - For Linux/MacOS:
      ```bash
      curl -LsSf https://astral.sh/uv/install.sh | sh
      ```
   - Other platforms: [See UV docs](https://docs.astral.sh/uv/getting-started/installation/)

3. **MySQL Database Initialization**:
   ```bash
   # Install MySQL if not already installed
   # For MacOS (using Homebrew):
   brew install mysql
   
   # Start MySQL service
   brew services start mysql
   
   # Create the database
   mysql -u root -p
   ```

4. **Set up Python environment**:
   ```bash
   # Install and pin Python version
   uv python install 3.11
   uv python pin 3.11

   # Create and activate virtual environment
   uv venv
   uv sync --all-extras
   ```

5. **Database Setup**
   Create a `.env` file in the root directory with the following content:
   ```
   DB_USER=your_username
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=for_how_much
   ```
   Replace the values with your MySQL database credentials.

6. **Run the database initialization and load questions from `data/data_source.csv`**:
   ```bash
   uv run src/for_how_much/migrate/init_db.py
   uv run src/for_how_much/migrate/load_questions.py
   ```

7. **Run the application**:
   ```bash
   uv run uvicorn main:app --reload
   ```

The API will be available at `http://localhost:8000`
API documentation will be available at `http://localhost:8000/docs`

## Database Schema

### Users
- id: Primary Key
- questions_seen: Number of questions viewed
- answered_questions: List of question IDs already answered

### Questions
- id: Primary Key
- text: Question text
- image_url: URL to associated image
- type: Question type (choice or slider)
- min_value: Minimum value for slider
- max_value: Maximum value for slider
- price_unit: Unit of price (e.g., $, €)
- category: Question category

### Stats
- question_id: Foreign Key to Questions
- average_answer: Average answer value 

## 📚 Table of Contents

- [Overview](#-overview)
- [Quick Start](#️-quick-start)
- [Project Structure](#️-project-structure)
- [Development Workflow](#️-development-workflow)
  - [Running Python scripts](#️-running-python-scripts)
  - [Package Management](#-package-management)
  - [Development Tools](#️-development-tools)
  - [Testing](#-testing-with-pytest)
  - [CI/CD](#-continuous-integration-and-continuous-deployment-cicd)
  - [Build locally](#-build-locally)
  - [Scripting](#-scripting)
- [Best Practices](#-best-practices)
- [Troubleshooting](#-troubleshooting)
- [Need Help?](#-need-help)

---

## 📝 Overview

This project leverages **modern Python development** best practices for maintainability, scalability, and developer happiness.

---

## ⚡️ Quick Start

### Prerequisites

- [Python 3.11+](https://www.python.org/downloads/)
- [UV](https://docs.astral.sh/uv/getting-started/installation/) (superfast Python package manager)
- [Git](https://git-scm.com/)

### 🚦 Initial Setup

1. **Clone this repository:**
   ```bash
   git clone https://github.com/<username>/for-how-much.git
   cd for-how-much
   ```

2. **Install UV**:
   - For Linux/MacOS:
      ```bash
      curl -LsSf https://astral.sh/uv/install.sh | sh
      ```
   - Other platforms: [See UV docs](https://docs.astral.sh/uv/getting-started/installation/).


3. **Set up Python environment**:
   ```bash
   # Install and pin Python version
   uv python install 3.11
   uv python pin 3.11

   # Create and activate virtual environment
   uv venv
   uv sync --all-extras
   ```
## 🗂️ Project Structure

```
for-how-much/
├── .github/           # GitHub Actions workflows
│   └── workflows/
├── scripts/           # Bash scripts
├── src/               # Source code
│   └── for_how_much/
│       └── hello_world.py
├── tests/             # Tests
│   └── src/
│       └── for_how_much/
│           └── test_hello_world.py
├── .gitignore         # Git ignore rules
├── .python-version    # Python version
├── Dockerfile         # Docker configuration for building the package
├── Makefile           # Makefile for running commands
├── pyproject.toml     # Python project configuration
└── README.md          # Project documentation
``` 

This project uses the [recommended structure for packaging in Python](https://packaging.python.org/en/latest/tutorials/packaging-projects/).

## 🛠️ Development Workflow

### ▶️ Running Python scripts

Run a Python script (e.g., hello world):
```bash
uv run src/for_how_much/hello_world.py
```

🔗 [UV scripts guide](https://docs.astral.sh/uv/getting-started/features/#scripts)

### 📦 Package Management

- Add dependencies:
```bash
uv add <package-name>
```

- Update dependencies:
```bash
uv sync --all-extras
```

- Upgrade all:
```bash
uv sync --upgrade
```

- Troubleshoot:
   If you have issues, try:
   ```
   rm uv.lock
   rm -rf .venv
   uv venv
   uv sync --all-extras
   ```
   More help: [UV docs](https://docs.astral.sh/uv/)



### ⚙️ Development Tools

All tools are configured in `pyproject.toml` and integrated into the Makefile:

- **Format**: `uv run black .`
- **Type-check**: `uv run mypy .`
- **Lint**: `uv run ruff check .`

✔️ Run all checks with:
```bash
make check
```


### 🧪 Testing with pytest

Testing is handled with `pytest`. Put [Unit tests](https://docs.pytest.org/en/stable/how-to/unittest.html) in the `tests/src/for_how_much/` folder. 

- Run all tests: 
```bash
make test
```
- Coverage report:
```bash
make test-coverage
```
→ Open `coverage/index.html` for details


### 🔄 Continuous Integration and Continuous Deployment (CI/CD)


- GitHub Actions handle testing, linting, and type checks.
- Workflows are in `.github/workflows/`.
- Default branch: The template uses `main_` to avoid auto-triggering at the start of the project.
   👉 Change to `main` if you want default CI/CD on pushes.

By default, this project includes GitHub Actions workflows for:
- Vulnerability scanning ([only available for free for public repositories](https://docs.github.com/en/code-security/code-scanning/troubleshooting-code-scanning/advanced-security-must-be-enabled))
- Lint, type check and unit testing


### 📦 Build locally

Build your Python package in Docker:
```bash
make build
```
Find the result in the `dist/` folder.


### 📄 Scripting

Place Bash scripts in `scripts/`.

Example: 
```bash
scripts/script_demo.sh
```

Customize or add `make` commands in the `Makefile`.

## 🌟 Best Practices

1. **Code Style**
   - Follow [PEP 8 guidelines](https://pep8.org/)
   - Use type hints
   - Write docstrings for all public functions

2. **Git Workflow**
   - Create feature branches
   - Write meaningful commit messages
   - Keep PRs focused and small

3. **Testing**
   - Write unit tests for new features
   - Maintain test coverage
   - Use pytest [fixtures](https://docs.pytest.org/en/stable/reference/fixtures.html)

## 🧩 Troubleshooting

**Virtual environment issues**
   ```bash
   # Recreate virtual environment
   rm uv.lock
   rm -rf .venv
   uv venv
   uv sync --all-extras
   ```

**Dependency conflicts**
   ```bash
   uv sync --upgrade
   ```

## 💡 Need Help?

- [UV docs](https://docs.astral.sh/uv/)
- [Python best practices](https://packaging.python.org/en/latest/)
- [GitHub Actions docs](https://docs.github.com/en/actions)


---

> **This project was generated using the [Python UV Project Template](https://github.com/clementw168/python-uv-template/).  
> If you'd like to create a similar project, check out the template on GitHub!**

---