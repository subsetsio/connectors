-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "borough",
    "feat_type",
    "feat_statu",
    "street_nm",
    "honorarynm",
    "old_st_nm",
    "streetwidt",
    "route_type",
    "roadwaytyp",
    "build_stat",
    "record_st",
    "paper_st",
    "stair_st",
    "cco_st",
    "marg_wharf",
    "edit_date"
FROM "nyc-open-data-g6zj-tzgn"
