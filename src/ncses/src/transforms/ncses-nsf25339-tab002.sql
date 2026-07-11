-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Type of activity and fiscal year - All activities" AS type_of_activity_and_fiscal_year_all_activities,
    "All agencies - All activities" AS all_agencies_all_activities,
    "AID - All activities" AS aid_all_activities,
    "ARC - All activities" AS arc_all_activities,
    "DHS - All activities" AS dhs_all_activities,
    "DOC - All activities" AS doc_all_activities,
    "DOD - All activities" AS dod_all_activities,
    "DOEa - All activities" AS doea_all_activities,
    "DOI - All activities" AS doi_all_activities,
    "DOJ - All activities" AS doj_all_activities,
    "DOL - All activities" AS dol_all_activities,
    "DOT - All activities" AS dot_all_activities,
    "ED - All activities" AS ed_all_activities,
    "EPA - All activities" AS epa_all_activities,
    "HHSb - All activities" AS hhsb_all_activities,
    "HUD - All activities" AS hud_all_activities,
    "NASA - All activities" AS nasa_all_activities,
    "NRC - All activities" AS nrc_all_activities,
    "NSF - All activities" AS nsf_all_activities,
    "SSA - All activities" AS ssa_all_activities,
    "USDA - All activities" AS usda_all_activities,
    "Otherc - All activities" AS otherc_all_activities
FROM "ncses-nsf25339-tab002"
