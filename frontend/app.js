const express = require('express');
const path = require('path');
const session = require('express-session');
const viewRoutes = require('./routes/viewRoutes');

const app = express();

// View engine setup
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public')));
app.use(session({
    secret: 'your-secret-key',
    resave: false,
    saveUninitialized: false,
    cookie: {
        secure: process.env.NODE_ENV === 'production',
        maxAge: 24 * 60 * 60 * 1000 // 24 hours
    }
}));

// Routes
app.use('/', viewRoutes);

// 404 handler
app.use((req, res) => {
    res.redirect('/?error=Page not found');
});

// Error handler
app.use((err, req, res, next) => {
    console.error(err);
    res.redirect(`/?error=${encodeURIComponent(err.message || 'Something went wrong')}`);
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});

module.exports = app;