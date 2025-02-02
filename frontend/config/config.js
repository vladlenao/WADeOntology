module.exports = {
    port: process.env.PORT || 3000,
    sessionSecret: process.env.SESSION_SECRET || 'your-secret-key',
    authServiceUrl: process.env.AUTH_SERVICE_URL || 'http://localhost:8000',
    ontoServiceUrl: process.env.ONTO_SERVICE_URL || 'http://localhost:8001'
};