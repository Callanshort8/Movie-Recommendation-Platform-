//shared by all pages
const API = 'http://localhost:8000';

function getToken() {
    return localStorage.getItem('token');
}

function authHeaders(){
    return {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ${getToken()}'
    };
}

function requireAuth() {
    if (!getToken()) window.location.href = 'index.html';
}

async function apiGet(path) {
    const res = await fetch(API + path, { headers: authHeaders()});
    if (res.status === 401) {localStorage.removeItem('token'); window.location.href = 'index.html';}
    return res.json();
}

async function apiPost(path, body = {}) {
    const res = await fetch(API + path, {
        method: 'POST',
        headers: authHeaders(),
        body: JSON.stringify(body)
    });
    return res.json();
}