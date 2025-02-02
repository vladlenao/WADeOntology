document.addEventListener('DOMContentLoaded', function() {
    const entityInput = document.getElementById('entity');
    const predicateSelect = document.getElementById('predicate');

    // Add auto-complete functionality if needed
    if (entityInput) {
        entityInput.addEventListener('input', async function() {
            if (this.value.length >= 2) {
                try {
                    const response = await fetch(`/onto/entity_relations/${this.value}`);
                    const data = await response.json();
                    // Implementation for auto-complete suggestions
                }
                catch (error) {
                    console.error('Error fetching entity relations:', error);
                }
            }
        });
    }

    // Dynamic form updates based on predicate selection
    if (predicateSelect) {
        predicateSelect.addEventListener('change', function() {
            const selectedPredicate = this.value;
            // Update form or display additional options based on selected predicate
        });
    }
});