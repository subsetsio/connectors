-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Model Name" AS model_name,
    "Stage" AS stage,
    "Number of Participants" AS number_of_participants,
    "Category" AS category,
    "Authority" AS authority,
    "Description" AS description,
    "Number of Beneficiaries Impacted" AS number_of_beneficiaries_impacted,
    "Number of Physicians Impacted" AS number_of_physicians_impacted,
    "Date Began" AS date_began,
    "Date Ended" AS date_ended,
    "States" AS states,
    "Keywords" AS keywords,
    "URL" AS url,
    CAST("Display Model Summary" AS BOOLEAN) AS display_model_summary,
    CAST("Unique ID" AS BIGINT) AS unique_id
FROM "cms-0d753f51-c3de-43cd-95d2-550a23b8606a"
