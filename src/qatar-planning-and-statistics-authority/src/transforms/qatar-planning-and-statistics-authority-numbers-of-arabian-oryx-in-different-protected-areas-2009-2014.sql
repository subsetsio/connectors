-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "protected_area",
    "lmhmy",
    "dhkwr_2009_males",
    "nth_females_2009",
    "lmjmw_total_2009",
    "dhkwr_males_2010",
    "nth_females_2010",
    "lmjmw_total_2010",
    "dhkwr_males_2011",
    "nth_2011females",
    "lmjmw_total_2011",
    "dhkwr_males_2012",
    "nth_2012_females",
    "lmjmw_total_2012",
    "dhkwr_males_2013",
    "nth_females_2013",
    "lmjmw_total_2013",
    "dhkwr_males_2014",
    "nth_females_2014",
    "lmjmw_2014_total"
FROM "qatar-planning-and-statistics-authority-numbers-of-arabian-oryx-in-different-protected-areas-2009-2014"
