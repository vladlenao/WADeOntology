const axios = require("axios");
const config = require("../config/config");

class OntologyService {
    static async queryBidirectional(entity, predicate, direction, limit = 10) {
        try {
            const response = await axios.get(
                `${config.ontoServiceUrl}/onto/query/`,
                { params :{
                    entity,
                    predicate,
                    direction,
                    limit
                    }
                }
            );

            return response.data;
        } catch (error) {
            throw new Error(error.response?.data?.detail || 'Query failed');
        }
    }

    static async getPredicates() {
        try {
            const response = await axios.get(
                `${config.ontoServiceUrl}/onto/predicates/`
            );
            return response.data;
        } catch (error) {
            throw new Error(error.response?.data?.detail || 'Failed to get predicates');
        }
    }

    static async getEntityRelations(entity) {
        try {
            const response = await axios.get(
                `${config.ontoServiceUrl}/onto/entity_relations/${entity}/`
            );
            return response.data;
        } catch (error) {
            throw new Error(error.response?.data?.detail || 'Failed to get entity relations');
        }
    }
}

module.exports = OntologyService;