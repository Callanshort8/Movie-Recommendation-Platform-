from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from dotenv import load_dotenv
from setupDB import setupDatabase

load_dotenv()

from auth import (
    hash_password, verify_password, create_access_token, get_current_user, require_admin
)

from database import get_db_connection
import TMDB

app = FastAPI(title = "Movie Recommendation Platform")

@app.on_event("startup")
def onStartup():
    setupDatabase()

#let it be called
app.add_middleware(
    CORSMiddleware,
    allow_origins =["http://localhost:5500", "http://127.0.0.1:5500", "https://ubiquitous-chainsaw-7v5gw5g5wpw6247q-5500.app.github.dev"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers = ["*"],

)

@app.post("/register")
def register(form: OAuth2PasswordRequestForm = Depends()):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    #check email exists 
    cursor.execute("SELECT email FROM Users WHERE email = %s", (form.username,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = hash_password(form.password)
    cursor.execute(
        "INSERT INTO Users (email, password) VALUES (%s, %s)",
        (form.username, hashed)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return {"message": "Account Created"}

@app.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends()):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("Select email, password, role FROM Users Where email = %s", (form.username,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if not user or not verify_password(form.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(data={"sub": user["email"], "role": user["role"]})
    return {"access_token": token, "token_type": "bearer"}
#Movie Search Route

@app.get("/api/health")
def health():
    result, status_code = tmdb.healthCheck()
    return result

@app.get("/api/movies/search")
def search_movies(query: str, page: int = 1):
    result, status_code = tmdb.MovieSearch(query, page)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result

@app.get("/api/movies/{tmdb_id}")
def movie_detail(tmdb_id: int):
    result, status_code = tmdb.getMovieDetails(tmdb_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result

@app.get("/api/movies/{tmdb_id}/cast")
def cast(tmdb_id: int):
    result, status_code = tmdb.getMovieCast(tmdb_id)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=result)
    return result

#User Routes

@app.post("/api/watchlist/{tmdb_id}")
def add_to_watchlist(tmdb_id: int, current_user: dict = Depends(get_current_user)):
    conn = get_db_connection()
    cursor = conn.cursor()

    movie_data, _ = tmdb.getMovieDetails(tmdb_id)
    cursor.execute(
        "INSERT IGNORE INTO Movies (canonical_id, tmdb_id, title, year, overview, poster_url) VALUES (UUID(), %s, %s, %s, %s, %s)",
        (tmdb_id, movie_data["title"], movie_data["releaseYear"], movie_data["plot"], movie_data["poster_url"])
    )

    cursor.execute(
        "SELECT canonical_id FROM Movies WHERE title = %s AND year = %s",
            (movie_data["title"], movie_data["releaseYear"])
    )
    row = cursor.fetchone()
    if row:
        cursor.execute(
            "INSERT IGNORE INTO watchlist (user_id,  canonical_id) "
            "SELECT u.user_id, %s FROM Users u WHERE u.email = %s",
            (row[0], current_user["email"])
        )

    

    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Added to watchlist"}

@app.post("/api/reviews/{tmdb_id}")
def add_review(tmdb_id: int, rating: int, body:str = "", current_user: dict = Depends(get_current_user)):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute (
        """INSERT INTO Reviews (user_id, canonical_id, rating, body)
        SELECT u.user_id, m.canonical_id, %s, %s
        FROM Users u, Movies m
        WHERE u.email = %s AND m.tmdb_id = %s""",
        (rating, body, current_user["email"], tmdb_id)
    )

    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "review submitted"}

@app.delete("/api/admin/reviews/{review_id}")
def delete_review(review_id: str, admin: dict = Depends(require_admin)):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Reviews WHERE review_id = %s", (review_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Review deleted"}

