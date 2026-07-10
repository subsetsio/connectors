-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Solar photovoltaics deployment includes capacity, accreditation, geography, and installation-count measures; filter to one measure before summing.
SELECT
    "resource",
    "sheet",
    "row_label",
    "series",
    "value_text",
    "value_num"
FROM "desnz-c647e722-b691-47e9-a765-a22e24f05a04"
