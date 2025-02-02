const AuthService = require('../services/authService');

class AuthController {
    static async renderLogin(req, res) {
        try {
            res.render('auth/login', {
                error: null,
                returnTo: req.session.returnTo || '/dashboard'
            });
        } catch (error) {
            console.error('Error rendering login page:', error);
            res.status(500).send('Error loading login page');
        }
    }

    static async renderRegister(req, res) {
        try {
            res.render('auth/register', { error: null });
        } catch (error) {
            console.error('Error rendering register page:', error);
            res.status(500).send('Error loading registration page');
        }
    }

    static async handleLogin(req, res) {
        try {
            const { username, password } = req.body;

            if (!username || !password) {
                return res.render('auth/login', {
                    error: 'Username and password are required',
                    returnTo: req.session.returnTo || '/dashboard'
                });
            }

            const loginData = await AuthService.login({
                username: username,
                password: password
            });

            // Store the token in session
            req.session.token = loginData.access_token;
            req.session.user = { username }; // Store basic user info

            // Redirect to the stored returnTo URL or dashboard
            const returnTo = req.session.returnTo || '/dashboard';
            delete req.session.returnTo; // Clear the stored URL
            res.redirect(returnTo);

        } catch (error) {
            console.error('Login error:', error);
            res.render('auth/login', {
                error: error.message || 'Invalid credentials',
                returnTo: req.session.returnTo || '/dashboard'
            });
        }
    }

    static async handleRegister(req, res) {
        try {
            const { username, email, password } = req.body;

            if (!username || !email || !password) {
                return res.render('auth/register', {
                    error: 'All fields are required'
                });
            }

            // Call the registration service
            await AuthService.register({
                username: username,
                email: email,
                password: password
            });

            // Redirect to login page after successful registration
            res.redirect('/auth/login');
        } catch (error) {
            console.error('Registration error:', error);
            res.render('auth/register', { 
                error: error.message || 'Registration failed' 
            });
        }
    }

    static async handleLogout(req, res) {
        try {
            // Clear the session
            req.session.destroy((err) => {
                if (err) {
                    console.error('Error destroying session:', err);
                }
                res.redirect('/auth/login');
            });
        } catch (error) {
            console.error('Logout error:', error);
            res.redirect('/auth/login');
        }
    }
}

module.exports = AuthController;