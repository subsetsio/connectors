-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "exam_no",
    "list_no",
    "first_name",
    "mi",
    "last_name",
    "adj_fa",
    "list_title_code",
    "list_title_desc",
    "group_no",
    "list_agency_code",
    "list_agency_desc",
    "list_div_code",
    "published_date",
    "established_date",
    "anniversary_date",
    "extension_date",
    "termination_date",
    "veteran_credit",
    "parent_lgy_credit",
    "sibling_lgy_credit",
    "residency_credit"
FROM "nyc-open-data-qu8g-sxqf"
