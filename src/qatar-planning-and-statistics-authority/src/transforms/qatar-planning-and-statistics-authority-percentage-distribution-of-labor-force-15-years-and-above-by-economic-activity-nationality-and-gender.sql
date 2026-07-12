-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "economic_activity",
    "lnsht_lqtsdy",
    "qatari_males",
    "qatari_females",
    "non_qatari_males",
    "non_qatari_females"
FROM "qatar-planning-and-statistics-authority-percentage-distribution-of-labor-force-15-years-and-above-by-economic-activity-nationality-and-gender"
