const axios = require("axios");
const config = require("../config/config");

class OntologyService {
    static async queryBidirectional(entity, predicate, direction, limit = 20) {
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

    static async getResourceDetails(uri) {
        try {
            const prefixes_to_remove = [
                "http://example.org/lang/",
                "http://example.org/framework/",
                "http://example.org/paradigm/",
                "http://example.org/repo/",
                "http://example.org/os/"
            ]
            let entity = uri.replace(prefixes_to_remove.find(prefix => uri.startsWith(prefix)), "");
            if (entity.includes("/") && entity.includes("github.com")) {
                entity = entity.split("/").pop();
            }
            // Get all relations for this resource using entity_relations endpoint
            const response = await axios.get(
                `${config.ontoServiceUrl}/onto/entity_relations/${entity}`
            );

            // Extract type from URI
            const type = uri.includes('/lang/') ? 'language' :
                        uri.includes('/framework/') ? 'framework' :
                        uri.includes('/paradigm/') ? 'paradigm' :
                        uri.includes('/repo/') ? 'repository' :
                        uri.includes('/os/') ? 'operatingSystem' : 'unknown';

            // Get the name from the URI
            const name = uri.split('/').pop();

            // Process the relations data
            const processedData = {
                name,
                type,
                uri,
                forwardRelations: response.data.forward_relations.map(rel => ({
                    predicate: rel.predicate.includes('type') ? 'isA' :
                               rel.predicate.includes('label') ? 'hasName' :
                               rel.predicate.split('/').pop(),
                    object: rel.object,
                    objectName: rel.object.split('/').pop()
                })),
                backwardRelations: response.data.backward_relations.map(rel => ({
                    predicate: rel.predicate.includes('type') ? 'isA' :
                               rel.predicate.includes('label') ? 'hasName' :
                               rel.predicate.split('/').pop(),
                    subject: rel.subject,
                    subjectName: rel.subject.split('/').pop()
                }))
            };

            // Add special properties for repositories
            if (type === 'repository') {
                const urlRel = response.data.forward_relations.find(rel => rel.predicate.includes('url'));
                const watchersRel = response.data.forward_relations.find(rel => rel.predicate.includes('watchers'));
                const descRel = response.data.forward_relations.find(rel => rel.predicate.includes('description'));

                processedData.properties = {
                    url: urlRel ? urlRel.object : null,
                    watchers: watchersRel ? watchersRel.object : null,
                    description: descRel ? descRel.object : null
                };
            }

            return processedData;
        } catch (error) {
            throw new Error(error.response?.data?.detail || 'Failed to get resource details');
        }
    }
}


module.exports = OntologyService;