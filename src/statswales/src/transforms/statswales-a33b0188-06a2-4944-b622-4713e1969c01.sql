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
    "Sex of Casualty" AS sex_of_casualty,
    "Type of Vehicle" AS type_of_vehicle,
    "Age of casualty" AS age_of_casualty,
    "By highways agency" AS by_highways_agency,
    "Notes" AS notes
FROM "statswales-a33b0188-06a2-4944-b622-4713e1969c01"
