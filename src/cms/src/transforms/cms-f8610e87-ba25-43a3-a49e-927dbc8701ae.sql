-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw profile; treat rows as source snapshot records, not entity-deduplicated facts.
SELECT
    "state",
    "CCN" AS ccn,
    "Provider_Name" AS provider_name,
    "city",
    "Ownership_Type" AS ownership_type,
    "ESRD_Network" AS esrd_network,
    "NPI" AS npi,
    "Chain" AS chain,
    "Modality" AS modality,
    "Alternate_CCNs" AS alternate_ccns,
    "Measure" AS measure,
    CAST("Measure_Score" AS BIGINT) AS measure_score,
    "year",
    "Measure_ID" AS measure_id
FROM "cms-f8610e87-ba25-43a3-a49e-927dbc8701ae"
