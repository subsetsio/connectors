-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table combines special-adviser gifts, hospitality, and meetings disclosures; filter to the applicable populated columns before counting events.
-- caution: Rows are unioned from many CSV resources whose headers changed over time, so equivalent names, dates, and organisation fields can appear in multiple columns.
SELECT
    "resource_name",
    "resource_id",
    "resource_last_modified",
    "source_url",
    "row_index",
    "accompanied_by_guest",
    "accompanied_by_spouse_family_member_s_or_friend",
    "by_special_advisers",
    "col_1",
    "col_3",
    "col_4",
    "date",
    "date_gift_received",
    "date_of_hospitality",
    "from",
    "gift",
    "gifts_received",
    "given_or_received",
    "hospitality_received",
    "individual_or_organisation_that_offered_hospitality",
    "minister",
    "month_of_meeting",
    "name",
    "name_1",
    "name_of_adviser",
    "name_of_organisation",
    "name_of_organisation_or_individual",
    "name_of_senior_media_figure",
    "name_of_special_adviser",
    "name_permanent_secretary_only",
    "outcome",
    "outcome_received_gifts_only",
    "pdf_1_6",
    "person_or_organisation_that_meeting_was_with",
    "person_or_organisation_that_offered_hospitality",
    "purpose_of_meeting",
    "special_adviser",
    "type_of_hospitality_received",
    "value",
    "who_gift_was_given_to_or_received_from",
    "who_gift_was_received_from"
FROM "uk-dwp-special-advisers-dwp"
