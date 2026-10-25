from transform import DataTransformer


def test_transform_commits():
    # Dados fictícios semelhantes aos da API do GitHub
    commits = [
        {
            "sha": "abc123",
            "commit": {
                "message": "Fix bug",
                "author": {
                    "date": "2026-10-10T12:00:00Z"
                }
            }
        }
    ]

    transformer = DataTransformer({})

    result = transformer.transform_commits(
        commits,
        repository_id=123
    )

    assert len(result) == 1
    assert result[0]["sha"] == "abc123"
    assert result[0]["repository_id"] == 123
    assert result[0]["message"] == "Fix bug"
    assert result[0]["committed_at"] == "2026-10-10T12:00:00Z"

def test_transform_issues():
    issues = [
        {
            "id": 100,
            "number": 10,
            "title": "Fix login",
            "state": "open",
            "created_at": "2026-10-10T10:00:00Z",
            "closed_at": None
        },
        {
            "id": 101,
            "number": 11,
            "title": "Update documentation",
            "state": "closed",
            "created_at": "2026-10-09T10:00:00Z",
            "closed_at": "2026-10-10T10:00:00Z",
            "pull_request": {}
        }
    ]

    transformer = DataTransformer({})

    result = transformer.transform_issues(
        issues,
        repository_id=123
    )

    # O pull request não deve entrar na tabela issues
    assert len(result) == 1
    assert result[0]["id"] == 100
    assert result[0]["repository_id"] == 123
    assert result[0]["title"] == "Fix login"
    assert result[0]["state"] == "open"


def test_transform_pull_requests():
    pull_requests = [
        {
            "id": 200,
            "number": 20,
            "title": "Add new feature",
            "state": "closed",
            "created_at": "2026-10-09T10:00:00Z",
            "merged_at": "2026-10-10T10:00:00Z"
        }
    ]

    transformer = DataTransformer({})

    result = transformer.transform_pull_requests(
        pull_requests,
        repository_id=123
    )

    assert len(result) == 1
    assert result[0]["id"] == 200
    assert result[0]["repository_id"] == 123
    assert result[0]["title"] == "Add new feature"
    assert result[0]["merged_at"] == "2026-10-10T10:00:00Z"

def test_transform_empty_lists():
    transformer = DataTransformer({})

    assert transformer.transform_commits([], 123) == []
    assert transformer.transform_issues([], 123) == []
    assert transformer.transform_pull_requests([], 123) == []