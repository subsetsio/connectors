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
    "Junction detail" AS junction_detail,
    "By highways agency" AS by_highways_agency,
    "Notes" AS notes
FROM "statswales-abcecddc-4843-4bda-aa9c-7289dd1410f5"
