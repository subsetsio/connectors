-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: One row per GPSP initiative, not per observation period: Year is when the initiative ran, so summing budget or beneficiaries across rows totals a programme, not a time series.
-- caution: Column names are truncated to the shapefile DBF ten-character limit in the raw and carry no unit; monetary amounts are US dollars per the source's own column label.
SELECT
    "source_item_id",
    "source_title",
    "source_type",
    "source_kind",
    "source_name",
    "source_row_number",
    "Year" AS year,
    "Country" AS country,
    "City" AS city,
    "Name_of_pr" AS name_of_pr,
    "Type_of_in" AS type_of_in,
    "Number_of" AS number_of,
    "Beneficiar" AS beneficiar,
    "Theme" AS theme,
    "Sub_theme" AS sub_theme,
    "Engagement" AS engagement,
    "Number_o_1" AS number_o_1,
    "BBB_Worksh" AS bbb_worksh,
    "BBB_Work_1" AS bbb_work_1,
    "Total_Peop" AS total_peop,
    "Budget__US" AS budget_us,
    "Donor_Fund" AS donor_fund,
    "Co_funding" AS co_funding,
    "Donor" AS donor,
    "Co_fundi_1" AS co_fundi_1,
    "Partner" AS partner,
    "Year_of_pr" AS year_of_pr,
    "Trainings" AS trainings,
    "Number_o_2" AS number_o_2,
    "Training_P" AS training_p,
    "Local_Gove" AS local_gove,
    "Project_St" AS project_st,
    "LATITUDE" AS latitude,
    "LONGITUDE" AS longitude,
    "Impact_Sto" AS impact_sto,
    "BBB_Storie" AS bbb_storie,
    "Field31" AS field31,
    "wkb_geometry"
FROM "un-habitat-601d5a351d8a4c629227edab4cd32900"
