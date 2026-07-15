-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Temporal series table; confirm aggregation dimensions before summing across categories.
SELECT
    "RegNo" AS regno,
    "Fullname" AS fullname,
    "Branch" AS branch,
    "DateofRegistration" AS dateofregistration,
    "Practice_EmployerName" AS practice_employername,
    "Practice_EmployerType" AS practice_employertype,
    "Practice_EmployerAddress" AS practice_employeraddress,
    "ContactNo" AS contactno
FROM "sg-data-d-f92927723e0894a14ee3acca6411e73d"
