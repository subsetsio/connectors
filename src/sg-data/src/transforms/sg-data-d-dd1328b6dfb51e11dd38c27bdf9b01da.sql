-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Year" AS year,
    "Takeup_Rate_of_Government_Paid_Maternity_Leave" AS takeup_rate_of_government_paid_maternity_leave,
    "Takeup_Rate_of_Government_Paid_Paternity_Leave" AS takeup_rate_of_government_paid_paternity_leave,
    "Takeup_Rate_of_Government_Paid_Childcare_Leave_by_Mother" AS takeup_rate_of_government_paid_childcare_leave_by_mother,
    "Takeup_Rate_of_Government_Paid_Childcare_Leave_by_Father" AS takeup_rate_of_government_paid_childcare_leave_by_father
FROM "sg-data-d-dd1328b6dfb51e11dd38c27bdf9b01da"
