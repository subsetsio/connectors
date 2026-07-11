-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_resource",
    "source_file",
    CAST("County Code Residence" AS BIGINT) AS county_code_residence,
    "County Name Residence" AS county_name_residence,
    CAST("County Code Place of Work" AS BIGINT) AS county_code_place_of_work,
    "County Name" AS county_name,
    "Travel Mode" AS travel_mode,
    CAST("Workers in Commuting Flow" AS BIGINT) AS workers_in_commuting_flow
FROM "instituto-de-estad-sticas-de-puerto-rico-commuting-flow-2009-2015"
