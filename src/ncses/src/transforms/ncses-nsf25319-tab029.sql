-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Type of institution" AS type_of_institution,
    "All costs" AS all_costs,
    "Included in institutional plans - Construct" AS included_in_institutional_plans_construct,
    "Included in institutional plans - Repair or renovate" AS included_in_institutional_plans_repair_or_renovate,
    "Not included in institutional plans - Construct" AS not_included_in_institutional_plans_construct,
    "Not included in institutional plans - Repair or renovate" AS not_included_in_institutional_plans_repair_or_renovate
FROM "ncses-nsf25319-tab029"
