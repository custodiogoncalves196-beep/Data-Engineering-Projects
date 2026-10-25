import pandas as pd


class DataTransformer:

    def __init__(self, data):
        self.data = data

    def transform_repository(self):
        # Select repository fields
        data_repository = {
            "id": self.data["id"],
            "name": self.data["name"],
            "owner_login": self.data["owner"]["login"],
            "language": self.data["language"],
            "star": self.data["stargazers_count"],
            "fork": self.data["forks_count"],
            "open": self.data["open_issues_count"],
            "pushed_at": self.data["pushed_at"]
        }

        # Create a DataFrame
        df = pd.DataFrame([data_repository])

        # Convert timestamp to UTC datetime
        df["pushed_at"] = pd.to_datetime(
            df["pushed_at"],
            utc=True
        )

        # Convert the transformed row to a dictionary
        data_transform = df.iloc[0].to_dict()

        return data_transform
    def transform_commits(self, commits, repository_id):
        transformed_commits = []

        for commit in commits:
            commit_info = commit.get("commit") or {}
            author_info = commit_info.get("author") or {}

            transformed_commits.append({
                "sha": commit.get("sha"),
                "repository_id": repository_id,
                "message": commit_info.get("message"),
                "committed_at": author_info.get("date")
            })

        return transformed_commits


    def transform_issues(self, issues, repository_id):
        transformed_issues = []

        for issue in issues:

            # A API de issues também pode devolver pull requests
            if "pull_request" in issue:
                continue

            transformed_issues.append({
                "id": issue.get("id"),
                "repository_id": repository_id,
                "number": issue.get("number"),
                "title": issue.get("title"),
                "state": issue.get("state"),
                "created_at": issue.get("created_at"),
                "closed_at": issue.get("closed_at")
            })

        return transformed_issues


    def transform_pull_requests(self, pull_requests, repository_id):
        transformed_pull_requests = []

        for pull_request in pull_requests:
            transformed_pull_requests.append({
                "id": pull_request.get("id"),
                "repository_id": repository_id,
                "number": pull_request.get("number"),
                "title": pull_request.get("title"),
                "state": pull_request.get("state"),
                "created_at": pull_request.get("created_at"),
                "merged_at": pull_request.get("merged_at")
            })

        return transformed_pull_requests