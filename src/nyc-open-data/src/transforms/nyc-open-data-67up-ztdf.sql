-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "health_opinion_poll_questions",
    "prevalence_hop1_april_16_to_may_13_2019",
    "prevalence_hop2_april_16_to_may_10_2019"
FROM "nyc-open-data-67up-ztdf"
