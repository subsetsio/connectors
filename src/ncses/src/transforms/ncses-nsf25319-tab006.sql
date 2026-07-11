-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Field" AS field,
    "Institutions with research space number a" AS institutions_with_research_space_number_a,
    "Institutions with research space shared with other fields - Number" AS institutions_with_research_space_shared_with_other_fields_number,
    "Institutions with research space shared with other fields - Percent" AS institutions_with_research_space_shared_with_other_fields_percent,
    "Institutions with research space also used for nonresearch purposes - Number" AS institutions_with_research_space_also_used_for_nonresearch_purposes_number,
    "Institutions with research space also used for nonresearch purposes - Percent" AS institutions_with_research_space_also_used_for_nonresearch_purposes_percent
FROM "ncses-nsf25319-tab006"
