-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table contains methodology and caveat text for public figures, not displacement observations to aggregate as a time series.
SELECT
    "iso3",
    "year",
    "figure_cause",
    "figure_cause_name",
    "figure_category",
    "figure_category_name",
    "description",
    "figures",
    "figures_rounded"
FROM "idmc-public-figure-analyses"
