-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "naics_codes",
    "naics_industry_description",
    "size_standards_in_millions_of_dollars",
    "size_standards_in_number_of_employees",
    "footnotes"
FROM "nyc-open-data-y52e-hp89"
