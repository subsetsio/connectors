-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are magnitude summaries over configured periods and frequencies, not raw observation events; filter by the period/frequency fields before comparing or summing magnitudes.
SELECT
    "species_id",
    "class_id",
    "order_id",
    "family_id",
    "genus_id",
    "genus",
    "species",
    "common_name",
    "kingdom",
    "phenophase_id",
    "phenophase_description",
    "year",
    "start_date",
    "end_date",
    "status_records_sample_size",
    "individuals_sample_size",
    "sites_sample_size",
    "num_yes_records",
    "numindividuals_with_yes_record",
    "numsites_with_yes_record",
    "proportion_yes_records",
    "proportion_individuals_with_yes_record",
    "proportion_sites_with_yes_record",
    "in-phase_sites_sample_size" AS in_phase_sites_sample_size,
    "in-phase_site_visits_sample_size" AS in_phase_site_visits_sample_size,
    "total_numanimals_in-phase" AS total_numanimals_in_phase,
    "mean_numanimals_in-phase" AS mean_numanimals_in_phase,
    "se_numanimals_in-phase" AS se_numanimals_in_phase,
    "in-phase_per_hr_sites_sample_size" AS in_phase_per_hr_sites_sample_size,
    "in-phase_per_hr_site_visits_sample_size" AS in_phase_per_hr_site_visits_sample_size,
    "mean_numanimals_in-phase_per_hr" AS mean_numanimals_in_phase_per_hr,
    "se_numanimals_in-phase_per_hr" AS se_numanimals_in_phase_per_hr,
    "in-phase_per_hr_per_acre_sites_sample_size" AS in_phase_per_hr_per_acre_sites_sample_size,
    "in-phase_per_hr_per_acre_site_visits_sample_size" AS in_phase_per_hr_per_acre_site_visits_sample_size,
    "mean_numanimals_in-phase_per_hr_per_acre" AS mean_numanimals_in_phase_per_hr_per_acre,
    "se_numanimals_in-phase_per_hr_per_acre" AS se_numanimals_in_phase_per_hr_per_acre
FROM "usa-npn-magnitude-phenometrics"
