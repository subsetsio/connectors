-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide source table with many measured attributes or category columns; avoid summing across columns without checking the upstream definition.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_NoQualification" AS total_noqualification,
    "Total_Primary" AS total_primary,
    "Total_LowerSecondary" AS total_lowersecondary,
    "Total_Secondary" AS total_secondary,
    "Total_UpperSecondary" AS total_uppersecondary,
    "Total_Polytechnic" AS total_polytechnic,
    "Total_OtherDiploma" AS total_otherdiploma,
    "Total_University" AS total_university,
    "ChangedJobDuringLast2Years_Total" AS changedjobduringlast2years_total,
    "ChangedJobDuringLast2Years_NoQualification" AS changedjobduringlast2years_noqualification,
    "ChangedJobDuringLast2Years_Primary" AS changedjobduringlast2years_primary,
    "ChangedJobDuringLast2Years_LowerSecondary" AS changedjobduringlast2years_lowersecondary,
    "ChangedJobDuringLast2Years_Secondary" AS changedjobduringlast2years_secondary,
    "ChangedJobDuringLast2Years_UpperSecondary" AS changedjobduringlast2years_uppersecondary,
    "ChangedJobDuringLast2Years_Polytechnic" AS changedjobduringlast2years_polytechnic,
    "ChangedJobDuringLast2Years_OtherDiploma" AS changedjobduringlast2years_otherdiploma,
    "ChangedJobDuringLast2Years_University" AS changedjobduringlast2years_university,
    "DidNotChangeJobDuringLast2Years_Total" AS didnotchangejobduringlast2years_total,
    "DidNotChangeJobDuringLast2Years_NoQualification" AS didnotchangejobduringlast2years_noqualification,
    "DidNotChangeJobDuringLast2Years_Primary" AS didnotchangejobduringlast2years_primary,
    "DidNotChangeJobDuringLast2Years_LowerSecondary" AS didnotchangejobduringlast2years_lowersecondary,
    "DidNotChangeJobDuringLast2Years_Secondary" AS didnotchangejobduringlast2years_secondary,
    "DidNotChangeJobDuringLast2Years_UpperSecondary" AS didnotchangejobduringlast2years_uppersecondary,
    "DidNotChangeJobDuringLast2Years_Polytechnic" AS didnotchangejobduringlast2years_polytechnic,
    "DidNotChangeJobDuringLast2Years_OtherDiploma" AS didnotchangejobduringlast2years_otherdiploma,
    "DidNotChangeJobDuringLast2Years_University" AS didnotchangejobduringlast2years_university
FROM "sg-data-d-96af22b648b0c48e0d66efc0851477ba"
