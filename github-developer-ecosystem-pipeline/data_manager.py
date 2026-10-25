import os
import requests
from dotenv import load_dotenv

load_dotenv()

HEADERS = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28"
}


class DataManager:

    def __init__(self, owner, repo):
        # Store repository information
        self.owner = owner
        self.repo = repo

        # Load GitHub token from environment
        self.token = os.getenv("GITHUB_TOKEN")

        # Store API rate limit information
        self.rate_limit = None

    def _get(self, endpoint, params=None):
        # Build the GitHub API URL
        url = (
            f"https://api.github.com/repos/"
            f"{self.owner}/{self.repo}{endpoint}"
        )

        # Prepare request headers
        request_headers = HEADERS.copy()

        # Add authentication token if available
        if self.token:
            request_headers["Authorization"] = (
                f"Bearer {self.token}"
            )

        # Execute GET request
        response = requests.get(
            url,
            headers=request_headers,
            params=params,
            timeout=15
        )

        # Capture API rate limit information
        self.rate_limit = {
            "limit": response.headers.get("X-RateLimit-Limit"),
            "remaining": response.headers.get("X-RateLimit-Remaining"),
            "used": response.headers.get("X-RateLimit-Used"),
            "reset": response.headers.get("X-RateLimit-Reset")
        }

        # Raise an exception for HTTP errors
        response.raise_for_status()

        return response.json()

    def _get_paginated(
        self,
        endpoint,
        max_pages=3,
        extra_params=None
    ):
        # Collect results from multiple API pages
        results = []

        # Request pages up to the configured limit
        for page in range(1, max_pages + 1):

            params = {
                "per_page": 100,
                "page": page
            }

            # Add endpoint-specific parameters
            if extra_params:
                params.update(extra_params)

            # Extract data from the current page
            data = self._get(endpoint, params=params)

            # Stop if the API returns no results
            if not data:
                break

            # Add current page results to the collection
            results.extend(data)

            # Stop if the current page is incomplete
            if len(data) < 100:
                break

        return results

    def get_github_data(self):
        # GET repository information
        return self._get("")

    def get_github_commits(self):
        # GET paginated repository commits
        return self._get_paginated("/commits")

    def get_github_issues(self):
        # GET paginated repository issues
        return self._get_paginated(
            "/issues",
            extra_params={
                "state": "all"
            }
        )

    def get_github_pulls(self):
        # GET paginated repository pull requests
        return self._get_paginated(
            "/pulls",
            extra_params={
                "state": "all"
            }
        )

    def get_rate_limit(self):
        # Return rate limit information from the last request
        return self.rate_limit