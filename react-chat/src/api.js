const BASE_URL = "http://127.0.0.1:5000";

// GET 요청
export const get = async (endpoint) => {
    try {
        const response = await fetch(`${BASE_URL}${endpoint}`);
        return await response.json();
    } catch (error) {
        console.error("GET request failed:", error);
        throw error;
    }
};

// POST 요청
export const post = async (endpoint, body) => {
    try {
        const response = await fetch(`${BASE_URL}${endpoint}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body),
        });
        return await response.json();
    } catch (error) {
        console.error("POST request failed:", error);
        throw error;
    }
};
