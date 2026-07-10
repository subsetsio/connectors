-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("time_period" AS BIGINT) AS time_period,
    "time_identifier",
    "geographic_level",
    "country_code",
    "country_name",
    "region_code",
    "region_name",
    "lad_code",
    "lad_name",
    "idaci_decile",
    "sex",
    CAST("children_count" AS BIGINT) AS children_count,
    "elgs_expected_average",
    CAST("all_elgs_expected_children_count" AS BIGINT) AS all_elgs_expected_children_count,
    "all_elgs_expected_children_percent",
    CAST("comm_lang_lit_expected_children_count" AS BIGINT) AS comm_lang_lit_expected_children_count,
    "comm_lang_lit_expected_children_percent",
    CAST("gld_children_count" AS BIGINT) AS gld_children_count,
    "gld_children_percent"
FROM "dfe-019ac0fc-29f3-77d7-ae85-73e6d61a4648"
