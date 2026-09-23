import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from fastapi.testclient import TestClient

from app import app, activities

client = TestClient(app)


def test_unregister_participant_removes_email():
    activity_name = "Chess Club"
    email = "student@test.com"

    activities[activity_name]["participants"].append(email)

    response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"


def test_unregister_missing_participant_returns_404():
    activity_name = "Chess Club"
    email = "missing@test.com"

    response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 404
