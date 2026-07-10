-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "State" AS state,
    CAST("Reimbursement" AS DOUBLE) AS reimbursement,
    CAST("Patients" AS BIGINT) AS patients,
    CAST("Visits" AS BIGINT) AS visits,
    CAST("Average Reimbursement Per Patient" AS DOUBLE) AS average_reimbursement_per_patient,
    CAST("Average Visits Per Patient" AS DOUBLE) AS average_visits_per_patient
FROM "cms-dc1392f2-64ad-431b-9a2f-47217e1cf094"
