from src.app import activities


def test_unregister_removes_student_from_activity(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    url = f"/activities/{activity_name}/unregister"

    # Act
    response = client.post(url, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}
    assert email not in activities[activity_name]["participants"]


def test_unregister_rejects_student_not_registered(client):
    # Arrange
    activity_name = "Chess Club"
    email = "nobody@mergington.edu"
    url = f"/activities/{activity_name}/unregister"

    # Act
    response = client.post(url, params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student not registered for this activity"


def test_unregister_unknown_activity_returns_404(client):
    # Arrange
    url = "/activities/Nonexistent Club/unregister"

    # Act
    response = client.post(url, params={"email": "michael@mergington.edu"})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
