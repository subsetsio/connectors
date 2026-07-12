-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The same NDC excerpt can map to multiple SDG targets, sectors, or response categories, and exact duplicate linkage rows can appear in the upstream extract.
SELECT
    "iso_code3",
    "country",
    "sdg",
    "sdg_target",
    "indc_text",
    "status",
    "sector",
    "climate_response",
    "type_of_information"
FROM "wri-ndc-sdg"
