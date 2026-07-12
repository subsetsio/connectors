-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows represent membership in GVA standing-report populations, not a deduplicated all-incidents universe; the same incident_id can appear under multiple report_population values.
-- caution: Some high-volume standing reports are capped by the source export API, so report populations can represent the most recent exported incidents rather than complete history.
SELECT
    "incident_id",
    strptime("incident_date", '%B %d, %Y')::DATE AS "incident_date",
    "state",
    "city_or_county",
    "address",
    "victims_killed",
    "victims_injured",
    "suspects_killed",
    "suspects_injured",
    "suspects_arrested",
    "report_population",
    "report_name"
FROM "gun-violence-archive-incidents"
