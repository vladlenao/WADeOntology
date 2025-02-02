const axios = require('axios');
const config = require('../config/config');

class AuthService {
    static async register(userData) {
        try {
            const response = await axios.post(
                `${config.authServiceUrl}/auth/register`,
                {
                    username: userData.username,
                    password: userData.password,
                    email: userData.email
                }
            );
            return response.data;
        } catch (error) {
            if (error.response) {
                // The request was made and the server responded with a status code
                // that falls out of the range of 2xx
                throw new Error(error.response.data.detail || 'Registration failed');
            } else if (error.request) {
                // The request was made but no response was received
                throw new Error('No response from authentication server');
            } else {
                // Something happened in setting up the request that triggered an Error
                throw new Error('Error setting up the request');
            }
        }
    }

    static async login(credentials) {
        try {
            const response = await axios.post(
                `${config.authServiceUrl}/auth/login`,
                {
                    username: credentials.username,
                    password: credentials.password,
                    email: ""
                }
            );
            return response.data;
        } catch (error) {
            if (error.response) {
                throw new Error(error.response.data.detail || 'Invalid credentials');
            } else if (error.request) {
                throw new Error('No response from authentication server');
            } else {
                throw new Error('Error setting up the request');
            }
        }
    }

    static async getUserProfile(token) {
        try {
            const response = await axios.get(
                `${config.authServiceUrl}/auth/users/me`,
                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            );
            return response.data;
        } catch (error) {
            if (error.response) {
                throw new Error(error.response.data.detail || 'Failed to get user profile');
            } else if (error.request) {
                throw new Error('No response from authentication server');
            } else {
                throw new Error('Error setting up the request');
            }
        }
    }
}

module.exports = AuthService;