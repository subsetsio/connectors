-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "obj_obtype",
    "obj_code",
    "obj_desc",
    "obj_class",
    "obj_category",
    "obj_position",
    "obj_parent",
    "obj_manufact",
    "obj_mrc",
    "obj_serialno",
    "obj_status",
    "obj_commiss",
    "obj_withdraw",
    "obj_record",
    "obj_notused",
    "obj_manufactmodel",
    "obj_value",
    "obj_updated",
    "obj_updatecount",
    "obj_gisobjid",
    "obj_sqlidentity",
    "obj_gislayer",
    "obj_xlocation",
    "obj_ylocation",
    "obj_udfchar01",
    "obj_udfchar02",
    "obj_udfchar05",
    "obj_udfchar06",
    "obj_created"
FROM "nyc-open-data-e25p-jzfy"
