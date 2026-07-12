-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "main_roads_ltrq_lry_ysy",
    "secondary_roads_ltrq_lthnwy",
    "third_class_roads_trq_ldrj_lthlth"
FROM "qatar-planning-and-statistics-authority-length-of-roads-annually-completed-by-road-type-and-year"
