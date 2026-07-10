-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("time" AS BIGINT) AS time,
    "regional_breakdown",
    "educational_institution",
    "educational_expenditure_in_total",
    "staff_expenditure",
    "material_expenditure",
    "investments",
    "taxes",
    "transfers_to_private_households",
    "transfers_to_private_non_profit_services",
    "transfers_to_enterprises",
    "transfers_to_social_security_institutions",
    "interests",
    "other_expenditure"
FROM "statistics-austria-ogd-bildungsausgaben-bildaus-2"
