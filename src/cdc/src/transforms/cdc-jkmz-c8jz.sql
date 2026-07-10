-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "State" AS state,
    "DistName" AS distname,
    "DistrictNCESID" AS districtncesid,
    "DistWeb" AS distweb,
    "DateClosure" AS dateclosure,
    "Distance Learning" AS distance_learning,
    "FrmDistanceLearning" AS frmdistancelearning,
    "FrmDistanceLearning_other" AS frmdistancelearning_other,
    "SubsidizedMeals" AS subsidizedmeals,
    "DistSubMeals" AS distsubmeals,
    "DistSubMeals_other" AS distsubmeals_other,
    "Sample_cat" AS sample_cat,
    CAST("Sample_cat_n" AS BIGINT) AS sample_cat_n
FROM "cdc-jkmz-c8jz"
