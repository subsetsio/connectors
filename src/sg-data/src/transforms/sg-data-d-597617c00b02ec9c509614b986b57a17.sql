-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Temporal series table; confirm aggregation dimensions before summing across categories.
SELECT
    "RegNo" AS regno,
    "Fullname" AS fullname,
    "SpecialisedBranch" AS specialisedbranch,
    "DateofRegistration" AS dateofregistration,
    "Practice_EmployerName" AS practice_employername,
    "Practice_EmployerType" AS practice_employertype,
    "Practice_EmployerAddress" AS practice_employeraddress,
    "ContactNo" AS contactno
FROM "sg-data-d-597617c00b02ec9c509614b986b57a17"
