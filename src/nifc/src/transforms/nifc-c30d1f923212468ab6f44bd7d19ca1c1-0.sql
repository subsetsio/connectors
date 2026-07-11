-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "OBJECTID" AS objectid,
    "DPA_AGENCY" AS dpa_agency,
    "DPA_GROUP" AS dpa_group,
    "RESPOND_ID" AS respond_id,
    "NWCG_UNITID" AS nwcg_unitid,
    "AGREEMENTS" AS agreements,
    "COST_APPOR" AS cost_appor,
    "COMMENTS" AS comments,
    "Shape__Area" AS shape_area,
    "Shape__Length" AS shape_length
FROM "nifc-c30d1f923212468ab6f44bd7d19ca1c1-0"
