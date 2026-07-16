-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "SBI2008PartBedrijvenOverheid" AS sbi2008partbedrijvenoverheid,
    "Perioden" AS perioden,
    "VacaturesSeizoengecorrigeerd_1" AS vacaturesseizoengecorrigeerd_1,
    "SBI2008PartBedrijvenOverheid_label" AS sbi2008partbedrijvenoverheid_label,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-80474ned"
