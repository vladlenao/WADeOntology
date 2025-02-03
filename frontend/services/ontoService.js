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
            print(response.data);
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

    static async getAllLanguages() {
        try {
            const response = await axios.get(
                `${config.ontoServiceUrl}/onto/languages/`
            );
            return response.data;
        } catch (error) {
            throw new Error(error.response?.data?.detail || 'Failed to get languages');
        }
    }

    static async getLanguageDetails(language) {
        try {
            const response = await axios.get(
                `${config.ontoServiceUrl}/onto/language/${encodeURIComponent(language)}/details/`
            );
            return response.data;
        } catch (error) {
            throw new Error(error.response?.data?.detail || 'Failed to get language details');
        }
    }

    static async getLanguageRepositories(language) {
        try {
            const response = await axios.get(
                `${config.ontoServiceUrl}/onto/language/${encodeURIComponent(language)}/repositories/`
            );
            return response.data;
        } catch (error) {
            throw new Error(error.response?.data?.detail || 'Failed to get language repositories');
        }
    }

    // Helper method to fetch all language related data at once
    static async getCompleteLanguageInfo(language) {
        try {
            const [details, repositories] = await Promise.all([
                this.getLanguageDetails(language),
                this.getLanguageRepositories(language)
            ]);

            return {
                ...details,
                repositories
            };
        } catch (error) {
            throw new Error(error.response?.data?.detail || 'Failed to get complete language information');
        }
    }
}


module.exports = OntologyService;