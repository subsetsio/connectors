-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Characteristic" AS characteristic,
    "Total - Number" AS total_number,
    "Total - SE" AS total_se,
    "Annual time spent volunteering for religious educational health-related or other charitable organizations - None - Percent" AS annual_time_spent_volunteering_for_religious_educational_health_related_or_other_charitable_organizations_none_percent,
    "Annual time spent volunteering for religious educational health-related or other charitable organizations - None - SE" AS annual_time_spent_volunteering_for_religious_educational_health_related_or_other_charitable_organizations_none_se,
    "Annual time spent volunteering for religious educational health-related or other charitable organizations - Less than 50 hours - Percent" AS annual_time_spent_volunteering_for_religious_educational_health_related_or_other_charitable_organizations_less_than_50_hours_percent,
    "Annual time spent volunteering for religious educational health-related or other charitable organizations - Less than 50 hours - SE" AS annual_time_spent_volunteering_for_religious_educational_health_related_or_other_charitable_organizations_less_than_50_hours_se,
    "Annual time spent volunteering for religious educational health-related or other charitable organizations - 50 hours or more - Percent" AS annual_time_spent_volunteering_for_religious_educational_health_related_or_other_charitable_organizations_50_hours_or_more_percent,
    "Annual time spent volunteering for religious educational health-related or other charitable organizations - 50 hours or more - SE" AS annual_time_spent_volunteering_for_religious_educational_health_related_or_other_charitable_organizations_50_hours_or_more_se,
    "Annual time spent helping friends neighbors or relatives - None - Percent" AS annual_time_spent_helping_friends_neighbors_or_relatives_none_percent,
    "Annual time spent helping friends neighbors or relatives - None - SE" AS annual_time_spent_helping_friends_neighbors_or_relatives_none_se,
    "Annual time spent helping friends neighbors or relatives - Less than 50 hours - Percent" AS annual_time_spent_helping_friends_neighbors_or_relatives_less_than_50_hours_percent,
    "Annual time spent helping friends neighbors or relatives - Less than 50 hours - SE" AS annual_time_spent_helping_friends_neighbors_or_relatives_less_than_50_hours_se,
    "Annual time spent helping friends neighbors or relatives - 50 hours or more - Percent" AS annual_time_spent_helping_friends_neighbors_or_relatives_50_hours_or_more_percent,
    "Annual time spent helping friends neighbors or relatives - 50 hours or more - SE" AS annual_time_spent_helping_friends_neighbors_or_relatives_50_hours_or_more_se
FROM "ncses-nsf25321-tabr-004"
