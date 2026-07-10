-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "citation_name",
    "date_signed",
    "state",
    "effective_date",
    "expiration_date",
    "prohibited_issuing_groups",
    "vaccination_prohibition_groups",
    "vaccination_requirement_details",
    "vaccination_person_exact_term",
    "vaccination_person_definition",
    "vaccination_issuer_exact_term",
    "vaccination_issuer_definition",
    "vaccination_prohibition_exemptions"
FROM "cdc-3m2r-fh4s"
