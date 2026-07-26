-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "borough",
    "feat_type",
    "officialnm",
    "honor_name",
    "old_name",
    "ulurpcpnum",
    "intro_num",
    "intro_year",
    "intromonth",
    "intro_day",
    "ll_num",
    "ll_sec",
    "ll_type",
    "lleffectdt",
    "ll_limits",
    "limits_er",
    "repealed",
    "repeal_dt",
    "amended",
    "amend_dt",
    "amendt_txt",
    "amdyrllsec"
FROM "nyc-open-data-qyv6-5ipu"
