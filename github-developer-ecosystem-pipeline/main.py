
from datetime import datetime, timezone
from data_manager import DataManager
from transform import DataTransformer
from database_manager import DatabaseManager
from logger_config import setup_logger

logger = setup_logger()

# ============================================================
# 1. GITHUB REPOSITORY CONFIGURATION
# ============================================================

REPOSITORIES = [
    ("microsoft", "vscode"),
    ("pandas-dev", "pandas"),
    ("psf", "requests"),
    ("python", "cpython"),
    ("django", "django")
]


# ============================================================
# 2. PREPARE POSTGRESQL CONNECTION
# ============================================================

db = DatabaseManager()

try:
    logger.info("ETL pipeline started")

    db.create_database()
    db.connect()
    db.create_tables()

    logger.info("PostgreSQL connection and tables ready")

    # ========================================================
    # 3. PROCESS MULTIPLE GITHUB REPOSITORIES
    # ========================================================

    for owner, repo in REPOSITORIES:

        logger.info(f"Processing repository: {owner}/{repo}")

        # Initialize GitHub API manager
        github = DataManager(owner, repo)

        # ====================================================
        # EXTRACT
        # ====================================================

        data = github.get_github_data()
        commits = github.get_github_commits()
        issues = github.get_github_issues()
        pulls = github.get_github_pulls()

        logger.info(f"Repository: {owner}/{repo}")
        logger.info(f"Commits extracted: {len(commits)}")
        logger.info(f"Issues extracted: {len(issues)}")
        logger.info(f"Pull requests extracted: {len(pulls)}")

        # ====================================================
        # TRANSFORM
        # ====================================================

        transformer = DataTransformer(data)

        data_transform = transformer.transform_repository()
        repository_id = data_transform["id"]

        commits_transform = transformer.transform_commits(
            commits,
            repository_id
        )

        issues_transform = transformer.transform_issues(
            issues,
            repository_id
        )

        pulls_transform = transformer.transform_pull_requests(
            pulls,
            repository_id
        )

        logger.info(
            f"Commits transformed: {len(commits_transform)}"
        )
        logger.info(
            f"Issues transformed: {len(issues_transform)}"
        )
        logger.info(
            f"Pull requests transformed: {len(pulls_transform)}"
        )

        # ====================================================
        # LOAD
        # ====================================================

        db.load_repository(data_transform)

        db.load_commits(commits_transform)
        db.load_issues(issues_transform)
        db.load_pull_requests(pulls_transform)

        logger.info(f"ETL completed: {owner}/{repo}")

        # ====================================================
        # GET API RATE LIMIT INFORMATION
        # ====================================================

        rate_limit = github.get_rate_limit()

        logger.info(f"GitHub API Rate Limit: {rate_limit}")

        if rate_limit and rate_limit.get("reset"):
            reset_time = datetime.fromtimestamp(
                int(rate_limit["reset"]),
                tz=timezone.utc
            )

            logger.info(
                f"Rate limit reset (UTC): {reset_time}"
            )

        if rate_limit and rate_limit.get("remaining") is not None:
            if int(rate_limit["remaining"]) < 100:
                logger.warning(
                    "GitHub API rate limit is running low"
                )

    # ========================================================
    # 4. VERIFY DATA IN POSTGRESQL
    # ========================================================

    db.show_repositories()

    logger.info("ETL pipeline completed successfully!")

except Exception:
    logger.exception("ETL pipeline failed")
    raise

finally:
    # ========================================================
    # 5. CLOSE POSTGRESQL CONNECTION
    # ========================================================

    db.close_connection()
    logger.info("PostgreSQL connection closed")
