class ApiError extends Error {
    constructor(code, message) {
        super(message);
        this.code = code;
    }
}


class APIClient {
    constructor(baseURL) {
        this.baseURL = baseURL;
    }

    get token() {
        return localStorage.getItem('token');
    }

    async request(endpoint, method = 'GET', body = null, requiresAuth = false) {
        const headers = {
            'Content-Type': 'application/json',
        };

        if (requiresAuth && this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }

        const config = {
            method,
            headers,
        };

        if (body) {
            config.body = JSON.stringify(body);
        }

        const response = await fetch(`${this.baseURL}${endpoint}`, config);

        if (response.status === 401) {
            this.clearSession();
            window.location.replace('/login');
        }

        if (!response.ok) {
            const json = await response.json();
            console.log(response.status, json);
            throw new ApiError(response.status, typeof(json.detail) === "string"? json.detail: response.statusText);
        }

        return response.status !== 204 ? await response.json() : null;
    }

    clearSession() {
        localStorage.removeItem('token');
        localStorage.removeItem('username');
        localStorage.removeItem('userId');
    }

    async createUser(username, password) {
        const data = {
            username,
            password,
        };
        return await this.request('/users/', 'POST', data);
    }

    async getUser(userId) {
        return await this.request(`/users/${userId}`, 'GET', null, true);
    }

    async getUserByUsername(username) {
        return await this.request(`/users/username/${username}`, 'GET', null, true);
    }

    async deleteUser() {
        return await this.request(`/users/${localStorage.userId}`, 'DELETE', null, true);
    }

    async login(username, password) {
        const data = {
            username,
            password,
        };
        const response = await this.request('/sessions/', 'POST', data);

        localStorage.setItem('token', response.token);
        localStorage.setItem('username', response.username);
        localStorage.setItem('userId', response.user_id);

        return response;
    }

    async sendMessage(to_id, text) {
        const data = {
            to_id,
            text,
        };
        return await this.request('/messages/', 'POST', data, true);
    }

    async getMessagesTo(to_id) {
        return await this.request(`/messages/to/${to_id}`, 'GET', null, true);
    }

    async getChats() {
        return await this.request('/chats/', 'GET', null, true);
    }

    async createTgKey() {
        return await this.request('/tg_key', 'POST', null, true);
    }
};
export default APIClient;
