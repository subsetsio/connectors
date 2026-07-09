-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Variable metadata is area-specific; the same variable code can have different source or methodology notes by country or aggregate area.
SELECT
    "country",
    "variable",
    "age",
    "pop",
    "countryname",
    "shortname",
    "simpledes",
    "technicaldes",
    "shorttype",
    "longtype",
    "shortpop",
    "longpop",
    "shortage",
    "longage",
    "unit",
    "source",
    "method",
    "extrapolation",
    "data_points",
    "data_quality_score"
FROM "world-inequality-database-variables"
