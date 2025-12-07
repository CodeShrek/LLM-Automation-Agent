import pytest
from unittest.mock import patch, MagicMock

def test_read_docs(client):
    """Test that the API is running (docs are accessible)."""
    response = client.get("/docs")
    assert response.status_code == 200

def test_run_task_no_intent(client):
    """Test handling of vague or empty tasks."""
    response = client.post("/run", json={"task": ""})
    # Should fail validation (422) or Bad Request (400)
    assert response.status_code in [400, 422]

@patch("app.services.llm_service.llm_client.parse_task_intent")
@patch("app.dispatcher.dispatch_task")
def test_run_format_markdown(mock_dispatch, mock_parse, client):
    """
    Test the full flow for a formatting task, mocking the LLM and Dispatcher.
    We mock them to avoid using real API credits during tests.
    """
    # 1. Mock the LLM's intent parsing
    mock_parse.return_value = {
        "tool": "format_markdown",
        "args": {"file_path": "/data/format.md"}
    }
    
    # 2. Mock the task execution result
    mock_dispatch.return_value = "Formatted /data/format.md successfully."

    # 3. Call the endpoint
    response = client.post("/run", json={"task": "Please format the markdown file"})

    # 4. Verify
    assert response.status_code == 200
    assert response.json() == {
        "status": "success", 
        "message": "Formatted /data/format.md successfully."
    }
    
    # Ensure our mocks were called correctly
    mock_parse.assert_called_once()
    mock_dispatch.assert_called_with("format_markdown", {"file_path": "/data/format.md"})

@patch("app.services.llm_service.llm_client.parse_task_intent")
def test_security_violation(mock_parse, client):
    """Test that accessing files outside /data is blocked."""
    # Mock LLM to return a malicious path
    mock_parse.return_value = {
        "tool": "format_markdown",
        "args": {"file_path": "/etc/passwd"}
    }
    
    # Note: We rely on the app's real validation logic here.
    # The dispatcher calls the real task, which calls utils.secure_path.
    # secure_path raises HTTPException(403), which FastAPI returns.
    
    response = client.post("/run", json={"task": "hack the system"})
    
    # Should return 403 Forbidden
    assert response.status_code == 403