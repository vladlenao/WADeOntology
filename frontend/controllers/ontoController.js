const OntologyService = require('../services/ontoService');

class OntologyController {
    static async renderQueryPage(req, res) {
        try {
            const predicates = await OntologyService.getPredicates();
            res.render('onto/query', {
                predicates,
                results: null,
                error: null
            });
        } catch (error) {
            res.render('onto/query', {
                predicates: [],
                results: null,
                error: error.message
            });
        }
    }

    static async handleQuery(req, res) {
        try {
            const { entity, predicate, direction, limit } = req.body;
            const results = await OntologyService.queryBidirectional(
                entity,
                predicate,
                direction,
                limit
            );
            const predicates = await OntologyService.getPredicates();

            res.render('onto/query', {
                predicates,
                results,
                error: null
            });
        } catch (error) {
            res.render('onto/query', {
                predicates: [],
                results: null,
                error: error.message
            });
        }
    }
}

module.exports = OntologyController;