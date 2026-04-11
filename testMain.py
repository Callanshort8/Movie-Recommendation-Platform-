#imports
import pytest
from fastapi import TestClient

from unittest.mock import MagicMock, patch
from main import app

client = TestClient(app)

def get_auth_token(email="test@test.com", password="testpassword"):
    with patch("main.get_db_connection") as mock_conn:
        mock_cursor = MagicMock()
        mock_conn.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None  

        from auth import hash_password
        client.post("/register", data={"username": email, "password": password})

    with patch("main.get_db_connection") as mock_conn:
        mock_cursor = MagicMock()
        mock_conn.return_value.cursor.return_value = mock_cursor
        from auth import hash_password
        mock_cursor.fetchone.return_value = {"email": email, "password": hash_password(password),"role": "user"}
        response = client.post("/login", data={"username": email, "password": password})
        return response.json().get("access_token")


def get_admin_token():
    with patch("main.get_db_connection") as mock_conn:
        mock_cursor = MagicMock()
        mock_conn.return_value.cursor.return_value = mock_cursor
        from auth import hash_password
        mock_cursor.fetchone.return_value = {"email": "admin@test.com","password": hash_password("adminpassword"),"role": "admin"}
        response = client.post("/login", data={"username": "admin@test.com","password": "adminpassword" })
        return response.json().get("access_token")

class TestRegister:

    def test_register_success(self):
        with patch("main.get_db_connection") as mock_conn:
            mock_cursor = MagicMock()
            mock_conn.return_value.cursor.return_value = mock_cursor
            mock_cursor.fetchone.return_value = None 
            response = client.post("/register", data={"username": "newuser@test.com","password": "password123"})
        assert response.status_code == 200
        assert response.json()["message"] == "Account Created"

    def test_register_duplicate_email(self):
        with patch("main.get_db_connection") as mock_conn:
            mock_cursor = MagicMock()
            mock_conn.return_value.cursor.return_value = mock_cursor
            mock_cursor.fetchone.return_value = {"email": "existing@test.com"}

            response = client.post("/register", data={"username": "existing@test.com", "password": "password123"})

        assert response.status_code == 400
        assert response.json()["detail"] == "Email in use"

    def test_register_missing_fields(self):
        response = client.post("/register", data={})
        assert response.status_code == 422

class TestLogin:
    def test_login_success(self):
        with patch("main.get_db_connection") as mock_conn:
            mock_cursor = MagicMock()
            mock_conn.return_value.cursor.return_value = mock_cursor
            from auth import hash_password
            mock_cursor.fetchone.return_value = {
                "email": "user@test.com",
                "password": hash_password("correctpassword"),
                "role": "user"
            }
            response = client.post("/login", data={
                "username": "user@test.com",
                "password": "correctpassword"
            })

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["role"] == "user"

    def test_login_wrong_password(self):
        with patch("main.get_db_connection") as mock_conn:
            mock_cursor = MagicMock()
            mock_conn.return_value.cursor.return_value = mock_cursor
            from auth import hash_password
            mock_cursor.fetchone.return_value = {
                "email": "user@test.com",
                "password": hash_password("correctpassword"),
                "role": "user"
            }

            response = client.post("/login", data={"username": "user@test.com","password": "wrongpassword"
            })

        assert response.status_code == 401

    def test_login_user_not_found(self):
        with patch("main.get_db_connection") as mock_conn:
            mock_cursor = MagicMock()
            mock_conn.return_value.cursor.return_value = mock_cursor
            mock_cursor.fetchone.return_value = None

            response = client.post("/login", data={
                "username": "ghost@test.com",
                "password": "password"
            })

        assert response.status_code == 401

    def test_login_admin_role(self):
        with patch("main.get_db_connection") as mock_conn:
            mock_cursor = MagicMock()
            mock_conn.return_value.cursor.return_value = mock_cursor
            from auth import hash_password
            mock_cursor.fetchone.return_value = {
                "email": "admin@test.com",
                "password": hash_password("adminpassword"),
                "role": "admin"
            }

            response = client.post("/login", data={
                "username": "admin@test.com",
                "password": "adminpassword"
            })

        assert response.status_code == 200
        assert response.json()["role"] == "admin"


