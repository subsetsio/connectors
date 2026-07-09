-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Long table of lead sponsor and collaborator associations; count distinct nct_id when counting studies by organization.
SELECT
    "nct_id",
    "name",
    "agency_class",
    "role"
FROM "clinicaltrials-gov-sponsors-collaborators"
