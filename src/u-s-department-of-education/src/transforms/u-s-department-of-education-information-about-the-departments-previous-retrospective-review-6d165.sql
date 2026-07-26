-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Catalog-level dataset may contain mixed measures, geography levels, or reporting periods; inspect column definitions before aggregating.
SELECT
    "package_id",
    "package_title",
    "resource_id",
    "resource_name",
    "resource_format",
    "resource_position",
    "sheet_name",
    "row_number",
    "Agency" AS agency,
    "Sub-agency" AS sub_agency,
    "Title of initiative/rule or ICR" AS title_of_initiative_rule_or_icr,
    "RIN/OMB Control Number" AS rin_omb_control_number,
    "Summary of initiative" AS summary_of_initiative,
    "Status of initiative -- New to this update, ongoing, or completed" AS status_of_initiative_new_to_this_update_ongoing_or_completed,
    "Target completion date (if completed, please add the publication date and cite in Federal Register)" AS target_completion_date_if_completed_please_add_the_publication_date_and_cite_in_federal_register,
    "Does the initiative include pilot projects, safe harbor exemptions, sunset provisions, trigger provisions, streamlined requirements, State flexibilities, or other similar strategies?" AS does_the_initiative_include_pilot_projects_safe_harbor_exemptions_sunset_provisions_trigger_provisions_streamlined_requirements_state_flexibilities_or_other_similar_strategies,
    "Does the initiative employ any type of experimental design (y/n)?" AS does_the_initiative_employ_any_type_of_experimental_design_y_n,
    "If so, please briefly describe" AS if_so_please_briefly_describe,
    "What methods will you engage in to identify improvements (public comment, analyses, third party assessments, etc.)? Please identify all that apply" AS what_methods_will_you_engage_in_to_identify_improvements_public_comment_analyses_third_party_assessments_etc_please_identify_all_that_apply,
    "If available, anticipated or realized savings in costs or burdens and anticipated or realized changes in benefits" AS if_available_anticipated_or_realized_savings_in_costs_or_burdens_and_anticipated_or_realized_changes_in_benefits,
    "Unnamed: 12" AS unnamed_12,
    "Unnamed: 13" AS unnamed_13,
    "Unnamed: 14" AS unnamed_14,
    "Unnamed: 15" AS unnamed_15,
    "Unnamed: 16" AS unnamed_16,
    "Unnamed: 17" AS unnamed_17,
    "Unnamed: 18" AS unnamed_18,
    "Unnamed: 19" AS unnamed_19,
    "Unnamed: 20" AS unnamed_20,
    "Unnamed: 21" AS unnamed_21,
    "Unnamed: 22" AS unnamed_22
FROM "u-s-department-of-education-information-about-the-departments-previous-retrospective-review-6d165"
