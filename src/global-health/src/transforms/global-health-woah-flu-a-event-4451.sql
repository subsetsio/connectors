-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows describe epidemiological units within a single WOAH event; animal counts such as susceptible, cases, deaths, killed, slaughtered, and vaccinated are separate measures.
SELECT
    CAST("Event_ID" AS BIGINT) AS event_id,
    CAST("Report_ID" AS BIGINT) AS report_id,
    "Report_Date" AS report_date,
    "Wild_or_Domestic" AS wild_or_domestic,
    "Species" AS species,
    CAST("Susceptible" AS BIGINT) AS susceptible,
    CAST("Cases" AS BIGINT) AS cases,
    CAST("Deaths" AS BIGINT) AS deaths,
    CAST("Killed.and.Disposed.of" AS BIGINT) AS killed_and_disposed_of,
    CAST("Slaughtered..Killed.for.commercial.use" AS BIGINT) AS slaughtered_killed_for_commercial_use,
    CAST("Vaccinated" AS BIGINT) AS vaccinated
FROM "global-health-woah-flu-a-event-4451"
