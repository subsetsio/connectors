"""Entity union for the nhs-digital connector.

The accepted CKAN package names (rank-active), copied verbatim from
data/sources/nhs-digital/work/entity_union.json. Data, not logic — kept out of
the node module so `nhs_digital.py` stays logic-only. The GP-practice
presentation-level prescribing package is deliberately absent (deferred at
accept: 411 resources, >1GB each — not publishable as one table via this mirror).
"""

ENTITY_IDS = [
    "adolescent-and-young-adult-type-1-diabetes-audit-2017-21",
    "general_pharmaceutical_services",
    "national-audit-of-pulmonary-hypertension-10th-annual-report-2019",
    "national-audit-of-pulmonary-hypertension-11th-annual-report-2020",
    "national-audit-of-pulmonary-hypertension-12th-annual-report-2020-21",
    "national-audit-of-pulmonary-hypertension-13th-annual-report-2021-22",
    "national-audit-of-pulmonary-hypertension-8th-annual-report-2017",
    "national-audit-of-pulmonary-hypertension-9th-annual-report-2018",
    "national-diabetes-audit-2020-21-type-1-diabetes",
    "national-diabetes-audit-diabetes-prevention-programme-2017-18-diagnoses-and-demographics",
    "national-diabetes-audit-insulin-pump-report-2016-17",
    "national-diabetes-audit-insulin-pump-report-2017-18",
    "national-diabetes-audit-report-1-care-processes-and-treatment-targets-2016-17",
    "national-diabetes-audit-report-1-care-processes-and-treatment-targets-2017-18-full-report",
    "national-diabetes-foot-care-audit-2014-2018",
    "national-diabetes-footcare-audit-hospital-admissions-report-2014-2016",
    "national-diabetes-inpatient-audit-harms-2018",
    "national-diabetes-inpatient-audit-harms-2019",
    "national-diabetes-inpatient-audit-nadia-2013",
    "national-diabetes-inpatient-audit-nadia-2018",
    "national-diabetes-inpatient-audit-nadia-2019",
    "national-diabetes-inpatient-safety-audit-ndisa-2018-2021",
    "national-diabetes-transition-audit-2011-2017",
    "national-pregnancy-in-diabetes-audit-report-2018",
    "ndfa-interval-review-july-2014-march-2021",
    "nhs-outcomes-framework-indicators",
    "pathology-laboratories",
]
