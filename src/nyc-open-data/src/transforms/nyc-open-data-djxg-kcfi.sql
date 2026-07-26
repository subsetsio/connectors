-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ccpversion",
    "maprojid",
    "magency",
    "projectid",
    "projectdescription",
    "sagencyacro",
    "sagencyname",
    "budgetline",
    "projecttype",
    "plancommdate",
    "commitmentdescription",
    "commitmentcode",
    "typc",
    "typcname",
    "plannedcommit_ccnonexempt",
    "plannedcommit_ccexempt",
    "plannedcommit_citycost",
    "plannedcommit_nccstate",
    "plannedcommit_nccfederal",
    "plannedcommit_nccother",
    "plannedcommit_noncitycost",
    "plannedcommit_total"
FROM "nyc-open-data-djxg-kcfi"
