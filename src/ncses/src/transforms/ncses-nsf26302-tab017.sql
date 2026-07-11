-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "State and department or agency" AS state_and_department_or_agency,
    "R and D performersa - All" AS r_and_d_performersa_all,
    "R and D performersa - Intramural" AS r_and_d_performersa_intramural,
    "R and D performersa - Extramural" AS r_and_d_performersa_extramural,
    "R and D plantb - All" AS r_and_d_plantb_all,
    "R and D plantb - Intramural" AS r_and_d_plantb_intramural,
    "R and D plantb - Extramural" AS r_and_d_plantb_extramural
FROM "ncses-nsf26302-tab017"
