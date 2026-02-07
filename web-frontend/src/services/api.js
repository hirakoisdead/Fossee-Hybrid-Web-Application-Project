import axios from 'axios';

const API_URL = '/api';

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Token ${token}`;
    }
    return config;
});

// Handle auth errors
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

export const authService = {
    register: async (username, email, password) => {
        const response = await api.post('/auth/register/', { username, email, password });
        return response.data;
    },

    login: async (username, password) => {
        const response = await api.post('/auth/login/', { username, password });
        return response.data;
    },

    logout: () => {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
    },

    isAuthenticated: () => {
        return !!localStorage.getItem('token');
    },

    getUser: () => {
        const user = localStorage.getItem('user');
        return user ? JSON.parse(user) : null;
    },

    setAuth: (token, user) => {
        localStorage.setItem('token', token);
        localStorage.setItem('user', JSON.stringify(user));
    }
};

export const datasetService = {
    upload: async (file) => {
        const formData = new FormData();
        formData.append('file', file);
        const response = await api.post('/upload/', formData, {
            headers: { 'Content-Type': 'multipart/form-data' },
        });
        return response.data;
    },

    list: async () => {
        const response = await api.get('/datasets/');
        return response.data;
    },

    get: async (id) => {
        const response = await api.get(`/datasets/${id}/`);
        return response.data;
    },

    getSummary: async (id) => {
        const response = await api.get(`/datasets/${id}/summary/`);
        return response.data;
    },

    delete: async (id) => {
        await api.delete(`/datasets/${id}/`);
    },

    getReportUrl: (id) => {
        const token = localStorage.getItem('token');
        return `${API_URL}/datasets/${id}/report/?auth=${token}`;
    }
};

export default api;
