-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Temporal series table; confirm aggregation dimensions before summing across categories.
SELECT
    "uen",
    "issuance_agency_desc",
    "uen_status_desc",
    "entity_name",
    "entity_type_desc",
    "uen_issue_date",
    "reg_street_name",
    "reg_postal_code"
FROM "sg-data-d-3f960c10fed6145404ca7b821f263b87"
