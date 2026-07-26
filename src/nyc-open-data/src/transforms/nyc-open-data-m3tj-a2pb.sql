-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "el_cycle",
    "from_stmt",
    "to_stmt",
    "office",
    "cand_name",
    "cand_id",
    "boro_dist",
    "termnd",
    "incumbent",
    "cntrs_no",
    "cntns_no",
    "net_cntns",
    "match_amt",
    "i_no",
    "i_cntns_no",
    "i_amt",
    "sml_no",
    "sml_amt",
    "pubfnd_pmt",
    "net_expnd",
    "cand_class_cd",
    "max_no",
    "max_amt",
    "_limit" AS limit,
    "outstanding_bills",
    "no_match"
FROM "nyc-open-data-m3tj-a2pb"
