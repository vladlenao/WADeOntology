const OntologyService = require('../services/ontoService');

class OntoController {
    static async renderQueryPage(req, res) {
        try {
            // Get predicates from the service
            const predicates = await OntologyService.getPredicates();

            // Initial render without query parameters
            res.render('onto/query', {
                user: req.session.user,
                predicates: predicates || [], // Ensure predicates is always an array
                results: null,
                error: null,
                query: {} // Add empty query object for form
            });
        } catch (error) {
            console.error('Error loading query page:', error);
            res.render('onto/query', {
                user: req.session.user,
                predicates: [],
                results: null,
                error: 'Failed to load predicates. Please try again.',
                query: {} // Add empty query object for form
            });
        }
    }

    static async handleQuery(req, res) {
        try {
            const { entity, predicate, direction } = req.body;

            // Get predicates for the form
            const predicates = await OntologyService.getPredicates();

            // Input validation
            if (!entity || !predicate || !direction) {
                return res.render('onto/query', {
                    user: req.session.user,
                    predicates,
                    results: null,
                    error: 'All fields are required',
                    query: req.body // Send back the submitted data
                });
            }

            // Get the query results
            const results = await OntologyService.queryBidirectional(
                entity,
                predicate,
                direction
            );

            if (!results || results.length === 0) {
                throw new Error('No results found');
            }

            // Check if we got results
            if (!Array.isArray(results)) {
                throw new Error('Invalid response from query service');
            }

            res.render('onto/query', {
                user: req.session.user,
                predicates,
                results,
                error: null,
                query: req.body // Send back the submitted data
            });
        } catch (error) {
            console.error('Query error:', error);

            // Get predicates for the form
            const predicates = await OntologyService.getPredicates().catch(() => []);

            res.render('onto/query', {
                user: req.session.user,
                predicates,
                results: null,
                error: error.message || 'An error occurred while processing your query',
                query: req.body // Send back the submitted data
            });
        }
    }

    static async renderLanguagesPage(req, res) {
        try {
            const languages = await OntologyService.getAllLanguages();

            res.render('onto/languages', {
                user: req.session.user,
                languages,
                error: null
            });
        } catch (error) {
            console.error('Error loading languages:', error);
            res.render('onto/languages', {
                user: req.session.user,
                languages: [],
                error: error.message
            });
        }
    }

    static async renderLanguageDetails(req, res) {
        try {
            const language = req.params.language;
            const [languages, languageInfo] = await Promise.all([
                OntologyService.getAllLanguages(),
                OntologyService.getCompleteLanguageInfo(language)
            ]);

            // Create language-details.ejs view if you haven't already
            res.render('onto/language-details', {
                user: req.session.user,
                languages,
                selectedLanguage: language,
                details: languageInfo,
                error: null
            });
        } catch (error) {
            console.error('Error loading language details:', error);

            // Try to get languages list even if details fail
            const languages = await OntologyService.getAllLanguages().catch(() => []);

            res.render('onto/language-details', {
                user: req.session.user,
                languages,
                selectedLanguage: req.params.language,
                details: null,
                error: error.message
            });
        }
    }
}

module.exports = OntoController;