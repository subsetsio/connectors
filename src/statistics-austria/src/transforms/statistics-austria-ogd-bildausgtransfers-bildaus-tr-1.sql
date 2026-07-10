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
    "transfers_to_federal_government",
    "transfers_to_laender_provinces",
    "transfers_to_communes",
    "transfers_to_regional_boards",
    "transfers_to_other_bodies_under_public_law",
    "transfers_abroad",
    "transfers_to_private_households",
    "transfers_to_private_non_profit_services",
    "transfers_to_enterprises",
    "transfers_to_social_security_institutions"
FROM "statistics-austria-ogd-bildausgtransfers-bildaus-tr-1"
