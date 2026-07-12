-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "lsn_year",
    "staff_teaching_administrative_pick_one",
    "lwzyq",
    "gender",
    "lnw",
    "age",
    "ljnsy",
    "nationality",
    "municipality",
    "lbldy",
    "mjmw_l_mlyn_sub_total_staff"
FROM "qatar-planning-and-statistics-authority-d2-school-staff"
