-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Date" AS date,
    "Area" AS area,
    "Severity" AS severity,
    "Type of vehicle" AS type_of_vehicle,
    "Road classification" AS road_classification,
    "By highways agency" AS by_highways_agency,
    "Notes" AS notes
FROM "statswales-2159ac9b-9672-4f09-80fd-e461f0efd5e1"
