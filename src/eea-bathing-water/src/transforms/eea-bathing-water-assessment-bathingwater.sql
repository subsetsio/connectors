-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Annual assessment rows describe a bathing water in a reporting season; do not aggregate boolean assessment flags across seasons as independent sites.
SELECT
    "bathingWaterIdentifier" AS bathingwateridentifier,
    "countryCode" AS countrycode,
    "hasAbnormalSituationDuringInsufficientInterval" AS hasabnormalsituationduringinsufficientinterval,
    "hasAbnormalSituationDuringSeasonStart" AS hasabnormalsituationduringseasonstart,
    "hasBeenContinuouslyMonitoredInLastAssessmentPeriod" AS hasbeencontinuouslymonitoredinlastassessmentperiod,
    "hasBeenInaccessibleInLastAssessmentPeriod" AS hasbeeninaccessibleinlastassessmentperiod,
    "hasBeenNewlyIdentifiedInLastAssessmentPeriod" AS hasbeennewlyidentifiedinlastassessmentperiod,
    "hasInaccessibilityDuringInsufficientInterval" AS hasinaccessibilityduringinsufficientinterval,
    "hasInaccessibilityDuringSeasonStart" AS hasinaccessibilityduringseasonstart,
    "hasMetMaximumIntervalBetweenSamples" AS hasmetmaximumintervalbetweensamples,
    "hasMinimumNumberOfSamples" AS hasminimumnumberofsamples,
    "hasMinimumNumberOfSamplesInLastAssessmentPeriod" AS hasminimumnumberofsamplesinlastassessmentperiod,
    "hasPreSeasonSample" AS haspreseasonsample,
    "hasQualityChangesDuringInsufficientInterval" AS hasqualitychangesduringinsufficientinterval,
    "hasQualityChangesDuringSeasonStart" AS hasqualitychangesduringseasonstart,
    "hasQualityChangesInLastAssessmentPeriod" AS hasqualitychangesinlastassessmentperiod,
    "hasReportedData" AS hasreporteddata,
    "reasonForManualClassification" AS reasonformanualclassification,
    "season",
    "UID" AS uid
FROM "eea-bathing-water-assessment-bathingwater"
