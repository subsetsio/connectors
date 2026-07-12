-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Commuting zones are generated geographies; use their ids rather than names for joins.
SELECT
    "region",
    "fbcz_id",
    "name",
    "fbcz_id_num",
    "cz_gen_ds",
    "win_population",
    "win_roads_km",
    "area",
    "country",
    "geography",
    "_source_file" AS source_file
FROM "meta-commuting-zones"
