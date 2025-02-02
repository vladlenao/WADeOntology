// routes/viewRoutes.js
const express = require('express');
const router = express.Router();
const AuthController = require('../controllers/authController');
const OntoController = require('../controllers/ontoController');

// Authentication middleware
const isAuthenticated = async (req, res, next) => {
    if (!req.session.token) {
        req.session.returnTo = req.originalUrl;
        return res.redirect('/auth/login');
    }
    try {
        next();
    } catch (error) {
        req.session.destroy();
        res.redirect('/auth/login');
    }
};

// Home route
router.get('/', (req, res) => {
    res.render('index', {
        user: req.session.user || null,
        error: req.query.error || null
    });
});

// Auth routes
router.get('/auth/login', (req, res) => {
    AuthController.renderLogin(req, res);
});

router.post('/auth/login', (req, res) => {
    AuthController.handleLogin(req, res);
});

router.get('/auth/register', (req, res) => {
    AuthController.renderRegister(req, res);
});

router.post('/auth/register', (req, res) => {
    AuthController.handleRegister(req, res);
});

router.get('/auth/logout', (req, res) => {
    AuthController.handleLogout(req, res);
});

// Protected Ontology routes
router.get('/onto/query', isAuthenticated, (req, res) => {
    OntoController.renderQueryPage(req, res);
});

router.post('/onto/query', isAuthenticated, (req, res) => {
    OntoController.handleQuery(req, res);
});

router.get('/onto/languages', isAuthenticated,(req, res) =>{
    OntoController.renderLanguagesPage(req, res);
});

router.get('/onto/language/:language', isAuthenticated,(req, res) =>{
    OntoController.renderLanguageDetails(req, res);
});

// Protected dashboard route
router.get('/dashboard', isAuthenticated, (req, res) => {
    res.render('dashboard', {
        user: req.session.user,
        error: null
    });
});



module.exports = router;