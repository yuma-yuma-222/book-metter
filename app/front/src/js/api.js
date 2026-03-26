// app/front/src/js/api.js

const API_BASE = "/api"; // Nginx経由なのでドメイン不要

async function getBooks(userId) {
    const response = await fetch(`${API_BASE}/books/user/${userId}`);
    if (!response.ok) throw new Error("本の取得に失敗しました");
    return await response.json();
}

async function postProgress(bookId, data) {
    const response = await fetch(`${API_BASE}/books/${bookId}/progress`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    if (!response.ok) throw new Error("保存に失敗しました");
    return await response.json();
}

async function postBook(data) {
    const response = await fetch(`${API_BASE}/books/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    if (!response.ok) {
        const err = await response.json();
        throw new Error(err.detail || "本の登録に失敗しました");
    }
    return await response.json();
}


async function deleteBook(bookId) {
    const response = await fetch(`${API_BASE}/books/${bookId}`, {
        method: 'DELETE'
    });
    if (!response.ok) throw new Error("削除に失敗しました");
    return await response.json();
}