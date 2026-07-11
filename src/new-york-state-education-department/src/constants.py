# Entity union (rank-active subsets) + per-entity fetch config for NYSED.
#
# Each subset is one logical table inside the per-year Microsoft Access databases
# published on https://data.nysed.gov/downloads.php. A subset is identified by:
#   - category: the downloads.php path segment (/files/<category>/...), used to
#     discover that family's per-year ZIP URLs from the downloads index.
#   - table_re: a (case-insensitive) regex matching the table's name inside the
#     Access DB. Several categories embed the school year in the table name
#     (e.g. "GRAD_RATE_AND_OUTCOMES_2025", "2023-24 ELL Enrollment"), so we match
#     by pattern rather than an exact literal and union across years.
#
# This is data, not logic — imported by the node module. The list is copied from
# data/sources/new-york-state-education-department/work/entity_union.json (33 ids).

ENTITY_IDS = [
    "enrollment-beds-day",
    "enrollment-demographics",
    "studed-attendance",
    "studed-average-class-size",
    "studed-free-reduced-lunch",
    "studed-instructional-modalities",
    "studed-staff",
    "studed-suspensions",
    "graduation-rate-outcomes",
    "graduation-pathways",
    "ap-ib-assessment",
    "ell-enrollment",
    "ell-home-languages",
    "ell-graduation-rate",
    "assessment-3-8-ela-math",
    "appr-district-educator",
    "appr-state-educator",
    "student-digital-resources",
    "src-assessment-em-ela",
    "src-assessment-em-math",
    "src-assessment-em-science",
    "src-assessment-regents-annual",
    "src-assessment-regents-total-cohort",
    "src-assessment-nyseslat",
    "src-assessment-nysaa",
    "src-accountability-status",
    "src-accountability-status-by-subgroup",
    "src-acc-hs-graduation-rate",
    "src-acc-em-chronic-absenteeism",
    "src-acc-hs-chronic-absenteeism",
    "src-inexperienced-teachers-principals",
    "src-teachers-out-of-certification",
    "src-expenditures-per-pupil",
    "spg-district-hedi",
    "spg-state-hedi",
    "ref-boces-nrc",
    "ref-institution-grouping",
]

# entity_id -> (downloads.php category segment, table-name regex [case-insensitive])
ENTITY_CONFIG = {
    "enrollment-beds-day":              ("enrollment", r"^BEDS Day Enrollment$"),
    "enrollment-demographics":          ("enrollment", r"^Demographic Factors$"),
    "studed-attendance":                ("studed",     r"^Attendance$"),
    "studed-average-class-size":        ("studed",     r"^Average Class Size$"),
    "studed-free-reduced-lunch":        ("studed",     r"^Free Reduced Price Lunch$"),
    "studed-instructional-modalities":  ("studed",     r"^Instructional[_ ]Modalities$"),
    "studed-staff":                     ("studed",     r"^Staff$"),
    "studed-suspensions":               ("studed",     r"^Suspensions$"),
    "graduation-rate-outcomes":         ("gradrate",   r"^GRAD_RATE_AND_OUTCOMES"),
    "graduation-pathways":              ("pathways",   r"^GRADUATION_PATHWAYS"),
    "ap-ib-assessment":                 ("apib",       r"^AP_?IB_Assessment"),
    "ell-enrollment":                   ("ell",        r"ELL Enrollment$"),
    "ell-home-languages":               ("ell",        r"ELL Home Languages$"),
    "ell-graduation-rate":              ("ell",        r"ELL Graduation Rate$"),
    "assessment-3-8-ela-math":          ("assessment", r"ELA_AND_MATH"),
    "appr-district-educator":           ("eval",       r"^APPR_DISTRICT_RESEARCHER"),
    "appr-state-educator":              ("eval",       r"^APPR_STATE_RESEARCHER"),
    "student-digital-resources":        ("student-digital-resources", r"^DIGITAL_EQ_SUMMARY"),
    "src-assessment-em-ela":            ("essa",       r"^Annual EM ELA$"),
    "src-assessment-em-math":           ("essa",       r"^Annual EM MATH$"),
    "src-assessment-em-science":        ("essa",       r"^Annual EM SCIENCE$"),
    "src-assessment-regents-annual":    ("essa",       r"^Annual Regents Exams$"),
    "src-assessment-regents-total-cohort": ("essa",    r"^Total Cohort Regents Exams$"),
    "src-assessment-nyseslat":          ("essa",       r"^Annual NYSESLAT$"),
    "src-assessment-nysaa":             ("essa",       r"^Annual NYSAA$"),
    "src-accountability-status":        ("essa",       r"^Accountability Status$"),
    "src-accountability-status-by-subgroup": ("essa",  r"^Accountability Status by Subgroup$"),
    "src-acc-hs-graduation-rate":       ("essa",       r"^ACC HS Graduation Rate$"),
    "src-acc-em-chronic-absenteeism":   ("essa",       r"^ACC EM Chronic Absenteeism$"),
    "src-acc-hs-chronic-absenteeism":   ("essa",       r"^ACC HS Chronic Absenteeism$"),
    "src-inexperienced-teachers-principals": ("essa",  r"^Inexperienced Teachers and Principals$"),
    "src-teachers-out-of-certification": ("essa",      r"^Teachers Teaching Out of Certification$"),
    "src-expenditures-per-pupil":       ("essa",       r"^Expenditures per Pupil$"),
    # Student-growth (SPG) HEDI researcher files live in the same eval DBs as the
    # APPR researcher files (2012-13..2015-16 only — that APPR/SPG regime ended).
    # 12-13 names the statewide table SPG_STATE_RESEARCHER_..., 13-14/14-15 rename
    # it SPG_STATEWIDE_RESEARCHER_... (identical schema); 15-16 restructured it to
    # SPG_DATA_* and is left out (mirrors the APPR researcher-file entities).
    "spg-district-hedi":                ("eval",       r"^SPG_DISTRICT_RESEARCHER"),
    "spg-state-hedi":                   ("eval",       r"^SPG_STATE(WIDE)?_RESEARCHER"),
    # Shared institution-reference tables. downloads.php has no 'shared-reference'
    # path segment — these tables are bundled inside the per-year enrollment DBs
    # (alongside 'BEDS Day Enrollment' / 'Demographic Factors'), so discover them
    # via the 'enrollment' category. fetch_one tags each row with report_year.
    "ref-boces-nrc":                    ("enrollment", r"^BOCES and N/RC$"),
    "ref-institution-grouping":         ("enrollment", r"^Institution Grouping$"),
}
