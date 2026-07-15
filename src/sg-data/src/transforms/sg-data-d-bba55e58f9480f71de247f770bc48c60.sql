-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Temporal series table; confirm aggregation dimensions before summing across categories.
SELECT
    "year",
    "industry1",
    "industry2",
    "industry3",
    "compassionate_leave",
    "marriage_leave",
    "unpaid_leave_morethan1mth",
    "unpaid_leave_1mthorless",
    "study_examination_leave",
    "child_sick_leave",
    "family_care_leave",
    "parental_care_leave",
    "sick_leave_without_mc",
    "paternity_leave"
FROM "sg-data-d-bba55e58f9480f71de247f770bc48c60"
