# 🚀 GitHub Developer Ecosystem Pipeline

### End-to-End ETL Pipeline | Python • GitHub REST API • PostgreSQL

## 📌 Project Overview

This project implements an Extract, Transform, Load (ETL) pipeline that collects public data from GitHub repositories, transforms API responses into structured records, and stores the results in a relational PostgreSQL database.

The project was developed as part of my Data Engineering portfolio to demonstrate practical skills in data extraction, transformation, database management, and pipeline development.

### 🎯 Project Objectives

- Extract repository metadata, commits, issues, and pull requests.
- Transform and normalize data collected from the GitHub REST API.
- Store structured data in PostgreSQL.
- Implement UPSERT operations to support repeated executions.
- Implement logging and exception handling.
- Validate data transformation logic through automated unit tests.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | ETL pipeline development |
| GitHub REST API | Data extraction |
| PostgreSQL | Relational data storage |
| psycopg2 | PostgreSQL connectivity |
| Requests | HTTP requests |
| pytest | Automated unit testing |
| Python Logging | Pipeline monitoring |
| python-dotenv | Environment configuration |

---

## 🏗️ Pipeline Architecture

```text
       GitHub REST API
              |
              v
     EXTRACT — Python
              |
              v
    TRANSFORM — Python
              |
              v
      LOAD — PostgreSQL
              |
              v
       Relational Tables
```

The pipeline follows three main stages.

**1. Extract**

Retrieves public information from selected GitHub repositories, including:

- Repository metadata
- Commits
- Issues
- Pull requests

**2. Transform**

Processes API responses and converts them into structured records suitable for relational storage.

The transformation stage also filters pull requests from issue records to avoid incorrect classification.

**3. Load**

Stores the transformed data in PostgreSQL using relational tables and UPSERT operations.

UPSERT operations allow the pipeline to update existing records or insert new records when necessary.

---

## 🗄️ Database Structure

The PostgreSQL database contains four main tables.

| Table | Description |
|---|---|
| repositories | Repository metadata |
| commits | Commit information |
| issues | Repository issues |
| pull_requests | Pull request information |

The commits, issues, and pull_requests tables reference the repositories table through `repository_id`.

The commits table uses a composite primary key consisting of `repository_id` and `sha`.

---

## 📂 Project Structure

```text
github-developer-ecosystem-pipeline/
│
├── tests/
│   └── test_transform.py
│
├── data_manager.py
├── database_manager.py
├── logger_config.py
├── main.py
├── transform.py
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

### Main Components

- **data_manager.py:** GitHub API communication and data extraction.
- **transform.py:** Data transformation and issue filtering.
- **database_manager.py:** Database operations, table creation, and UPSERT.
- **main.py:** ETL pipeline orchestration.
- **logger_config.py:** Logging configuration.
- **tests/test_transform.py:** Unit tests for transformation logic.

---

## 📊 Execution Results

The pipeline was successfully executed on October 25, 2026.

Five public GitHub repositories were processed.

| Repository | Commits | Valid Issues | Pull Requests |
|---|---:|---:|---:|
| microsoft/vscode | 300 | 173 | 300 |
| pandas-dev/pandas | 300 | 52 | 300 |
| psf/requests | 300 | 52 | 300 |
| python/cpython | 300 | 62 | 300 |
| django/django | 300 | 0 | 300 |
| **Total** | **1,500** | **339** | **1,500** |

**Total: 3,339 related records processed, plus five repository records.**

These figures represent records reported as processed during execution, not necessarily newly inserted database rows.

The pipeline completed successfully, and the PostgreSQL connection was closed correctly.

---

## 🧪 Testing and Validation

Automated unit tests were implemented using pytest.

The following tests passed:

- `test_transform_commits`
- `test_transform_issues`
- `test_transform_pull_requests`
- `test_transform_empty_lists`

**Test results: 4 passed.**

These tests validate transformation behavior using test data.

Automated integration tests for the GitHub API and PostgreSQL database are not yet included.

---

## 📋 Logging and Error Handling

The pipeline includes logging functionality to track execution.

Implemented features include:

- Timestamped INFO messages.
- Pipeline execution monitoring.
- Logging to the terminal and a log file.
- Warnings when GitHub API request limits are low.
- Exception logging and propagation.
- PostgreSQL connection cleanup.

---

## ⚙️ Installation and Execution

### 1. Clone the repository

Clone the repository after it has been published on GitHub.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate the virtual environment.

**Windows:**

```powershell
.\.venv\Scripts\Activate.ps1
```

**Linux/macOS:**

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file using `.env.example` as a template.

Configure the required GitHub API and PostgreSQL credentials.

Never commit real credentials to the repository.

### 5. Configure PostgreSQL

Create the required PostgreSQL database and ensure that the connection settings match the application's configuration.

### 6. Run the pipeline

```bash
python main.py
```

### 7. Run the tests

```bash
python -m pytest -v
```

**Note:** These instructions assume that Python, PostgreSQL, and the required database configuration are available. The exact environment variable names and database initialization requirements should be verified against the source code before publication.

---

## 🔮 Future Improvements

Potential improvements include:

- Database validation using SQL queries.
- Automated integration tests.
- Additional API failure scenarios.
- Improved logging consistency.
- Enhanced API pagination.
- Additional data quality checks.

---

## 📄 Technical Documentation

A complete technical report is available in Portuguese.

The report documents the architecture, database model, execution results, testing, limitations, and future improvements.

---

## 👨‍💻 Author

**Custódio Gonçalves**

Computer Engineering Student — Universidade Aberta, Portugal

Aspiring Data Engineer

[LinkedIn](https://www.linkedin.com/in/custodio-goncalves-981876370/)

---

⭐ *Building practical Data Engineering skills through real-world projects.*