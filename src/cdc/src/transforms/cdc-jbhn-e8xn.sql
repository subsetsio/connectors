-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Year" AS BIGINT) AS year,
    CAST("Month" AS BIGINT) AS month,
    "State" AS state,
    "Source Type" AS source_type,
    "Source Site" AS source_site,
    "Pathogen" AS pathogen,
    "Serotype/Species" AS serotype_species,
    CAST("Number of isolates" AS BIGINT) AS number_of_isolates,
    CAST("Outbreak associated isolates" AS BIGINT) AS outbreak_associated_isolates,
    CAST("New multistate outbreaks" AS BIGINT) AS new_multistate_outbreaks,
    CAST("New multistate outbreaks - US" AS BIGINT) AS new_multistate_outbreaks_us,
    CAST("% Isolates with clinically important antimicrobial resistance" AS BIGINT) AS isolates_with_clinically_important_antimicrobial_resistance,
    CAST("Number of sequenced isolates analyzed by NARMS" AS BIGINT) AS number_of_sequenced_isolates_analyzed_by_narms
FROM "cdc-jbhn-e8xn"
