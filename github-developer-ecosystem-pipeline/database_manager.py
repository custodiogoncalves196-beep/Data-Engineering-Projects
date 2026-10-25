import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

load_dotenv(override=True)


class DatabaseManager:

    def __init__(self):
        self.database_name = "meu_pipeline"
        self.connection = None

        self.db_config = {
            "host": os.getenv("POSTGRES_HOST", "localhost"),
            "port": int(os.getenv("POSTGRES_PORT", "5432")),
            "user": os.getenv("POSTGRES_USER"),
            "password": os.getenv("POSTGRES_PASSWORD")
        }

    # ========================================================
    # 1. CREATE DATABASE
    # ========================================================

    def create_database(self):
        connection = psycopg2.connect(
            dbname="postgres",
            **self.db_config
        )

        try:
            connection.autocommit = True

            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT 1 FROM pg_database WHERE datname = %s",
                    (self.database_name,)
                )

                database_exists = cursor.fetchone()

                if database_exists is None:
                    cursor.execute(
                        sql.SQL("CREATE DATABASE {}").format(
                            sql.Identifier(self.database_name)
                        )
                    )

                    print(
                        f"Database '{self.database_name}' created!"
                    )
                else:
                    print(
                        f"Database '{self.database_name}' already exists."
                    )

        finally:
            connection.close()

    # ========================================================
    # 2. CONNECT TO DATABASE
    # ========================================================

    def connect(self):
        self.connection = psycopg2.connect(
            dbname=self.database_name,
            **self.db_config
        )

        print("Connected to PostgreSQL!")

    # ========================================================
    # 3. CREATE TABLES
    # ========================================================

    def create_tables(self):
        try:
            with self.connection.cursor() as cursor:

                # REPOSITORIES
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS repositories (
                        id BIGINT PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        owner_login VARCHAR(255) NOT NULL,
                        language VARCHAR(100),
                        star INTEGER NOT NULL,
                        fork INTEGER NOT NULL,
                        open INTEGER NOT NULL,
                        pushed_at TIMESTAMPTZ
                    );
                """)

                # COMMITS
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS commits (
                        sha VARCHAR(40) NOT NULL,
                        repository_id BIGINT NOT NULL,
                        message TEXT,
                        committed_at TIMESTAMPTZ,
                        PRIMARY KEY (repository_id, sha),
                        FOREIGN KEY (repository_id)
                            REFERENCES repositories(id)
                    );
                """)

                # ISSUES
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS issues (
                        id BIGINT PRIMARY KEY,
                        repository_id BIGINT NOT NULL,
                        number INTEGER NOT NULL,
                        title TEXT,
                        state VARCHAR(50),
                        created_at TIMESTAMPTZ,
                        closed_at TIMESTAMPTZ,
                        FOREIGN KEY (repository_id)
                            REFERENCES repositories(id)
                    );
                """)

                # PULL REQUESTS
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS pull_requests (
                        id BIGINT PRIMARY KEY,
                        repository_id BIGINT NOT NULL,
                        number INTEGER NOT NULL,
                        title TEXT,
                        state VARCHAR(50),
                        created_at TIMESTAMPTZ,
                        merged_at TIMESTAMPTZ,
                        FOREIGN KEY (repository_id)
                            REFERENCES repositories(id)
                    );
                """)

            self.connection.commit()
            print("All four tables are ready!")

        except Exception:
            self.connection.rollback()
            raise

    # ========================================================
    # 4. LOAD REPOSITORY
    # ========================================================

    def load_repository(self, data_transform):
        columns = list(data_transform.keys())
        values = list(data_transform.values())

        query = sql.SQL("""
            INSERT INTO repositories ({columns})
            VALUES ({placeholders})
            ON CONFLICT (id)
            DO UPDATE SET
                name = EXCLUDED.name,
                owner_login = EXCLUDED.owner_login,
                language = EXCLUDED.language,
                star = EXCLUDED.star,
                fork = EXCLUDED.fork,
                open = EXCLUDED.open,
                pushed_at = EXCLUDED.pushed_at;
        """).format(
            columns=sql.SQL(", ").join(
                map(sql.Identifier, columns)
            ),
            placeholders=sql.SQL(", ").join(
                sql.Placeholder() for _ in values
            )
        )

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, values)

            self.connection.commit()
            print("Repository loaded successfully!")

        except Exception:
            self.connection.rollback()
            raise

    # ========================================================
    # 5. LOAD COMMITS
    # ========================================================

    def load_commits(self, commits):
        query = """
            INSERT INTO commits (
                sha, repository_id, message, committed_at
            )
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (repository_id, sha)
            DO UPDATE SET
                message = EXCLUDED.message,
                committed_at = EXCLUDED.committed_at;
        """

        try:
            with self.connection.cursor() as cursor:
                for commit in commits:
                    cursor.execute(query, (
                        commit["sha"],
                        commit["repository_id"],
                        commit["message"],
                        commit["committed_at"]
                    ))

            self.connection.commit()
            print(f"{len(commits)} commits loaded successfully!")

        except Exception:
            self.connection.rollback()
            raise

    # ========================================================
    # 6. LOAD ISSUES
    # ========================================================

    def load_issues(self, issues):
        query = """
            INSERT INTO issues (
                id, repository_id, number, title,
                state, created_at, closed_at
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id)
            DO UPDATE SET
                repository_id = EXCLUDED.repository_id,
                number = EXCLUDED.number,
                title = EXCLUDED.title,
                state = EXCLUDED.state,
                created_at = EXCLUDED.created_at,
                closed_at = EXCLUDED.closed_at;
        """

        try:
            with self.connection.cursor() as cursor:
                for issue in issues:
                    cursor.execute(query, (
                        issue["id"],
                        issue["repository_id"],
                        issue["number"],
                        issue["title"],
                        issue["state"],
                        issue["created_at"],
                        issue["closed_at"]
                    ))

            self.connection.commit()
            print(f"{len(issues)} issues loaded successfully!")

        except Exception:
            self.connection.rollback()
            raise

    # ========================================================
    # 7. LOAD PULL REQUESTS
    # ========================================================

    def load_pull_requests(self, pull_requests):
        query = """
            INSERT INTO pull_requests (
                id, repository_id, number, title,
                state, created_at, merged_at
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id)
            DO UPDATE SET
                repository_id = EXCLUDED.repository_id,
                number = EXCLUDED.number,
                title = EXCLUDED.title,
                state = EXCLUDED.state,
                created_at = EXCLUDED.created_at,
                merged_at = EXCLUDED.merged_at;
        """

        try:
            with self.connection.cursor() as cursor:
                for pull_request in pull_requests:
                    cursor.execute(query, (
                        pull_request["id"],
                        pull_request["repository_id"],
                        pull_request["number"],
                        pull_request["title"],
                        pull_request["state"],
                        pull_request["created_at"],
                        pull_request["merged_at"]
                    ))

            self.connection.commit()
            print(
                f"{len(pull_requests)} pull requests loaded successfully!"
            )

        except Exception:
            self.connection.rollback()
            raise

    # ========================================================
    # 8. SHOW REPOSITORIES
    # ========================================================

    def show_repositories(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT *
                FROM repositories
                ORDER BY id;
            """)

            results = cursor.fetchall()

        for row in results:
            print(row)

        return results

    # ========================================================
    # 9. CLOSE CONNECTION
    # ========================================================

    def close_connection(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

            print("PostgreSQL connection closed.")