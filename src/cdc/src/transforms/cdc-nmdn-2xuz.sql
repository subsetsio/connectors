-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "citation_name",
    strptime("date_signed", '%m/%d/%Y')::DATE AS date_signed,
    "state",
    strptime("effective_date", '%m/%d/%Y')::DATE AS effective_date,
    strptime("expiration_date", '%m/%d/%Y')::DATE AS expiration_date,
    "prohibited_issuing_groups",
    "vaccination_prohibition_groups",
    "vaccination_requirement_details",
    "vaccination_person_exact_term",
    "vaccination_person_definition",
    "vaccination_issuer_exact_term",
    "vaccination_issuer_definition",
    "vaccination_prohibition_exemptions"
FROM "cdc-nmdn-2xuz"
