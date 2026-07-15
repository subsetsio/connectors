-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Temporal series table; confirm aggregation dimensions before summing across categories.
SELECT
    "year",
    "gender",
    "mean_score",
    "social_intelligence",
    "cognitive_efficacy",
    "self_esteem",
    "emotional_intelligence",
    "resilience"
FROM "sg-data-d-586ef8eb3f0f49a6c871665c2aa5784f"
