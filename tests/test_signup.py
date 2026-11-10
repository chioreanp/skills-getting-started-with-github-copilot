from src.app import activities


def test_signup_adds_student_to_activity(client):
    # Arrange
    activity_name = "Basketball Team"
    email = "new.student@mergington.edu"
    url = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(url, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert email in activities[activity_name]["participants"]


def test_signup_rejects_duplicate_email(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    url = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(url, params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"
    assert activities[activity_name]["participants"].count(email) == 1


def test_signup_rejects_full_activity(client):
    # Arrange
    activity_name = "Basketball Team"
    activities[activity_name]["participants"] = ["first@mergington.edu"]
    activities[activity_name]["max_participants"] = 1
    url = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(url, params={"email": "second@mergington.edu"})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"
    assert "second@mergington.edu" not in activities[activity_name]["participants"]


def test_signup_unknown_activity_returns_404(client):
    # Arrange
    url = "/activities/Nonexistent Club/signup"

    # Act
    response = client.post(url, params={"email": "new.student@mergington.edu"})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
