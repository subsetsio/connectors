-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS "sheet",
    "District" AS "district",
    "HH no." AS "hh_no",
    "Surname" AS "surname",
    "First name" AS "first_name",
    "Female?" AS "female",
    "note",
    "c6",
    "acres",
    "£" AS "column",
    "£/acre" AS "acre",
    ".. And land" AS "and_land",
    "… no land" AS "no_land",
    "land, no slaves" AS "land_no_slaves",
    "number",
    "decimalized £" AS "decimalized",
    "£/slave" AS "slave",
    "number_2",
    "dec. £" AS "dec",
    "£/horse" AS "horse",
    "number_3",
    "dec. £_2" AS "dec_2",
    "£/head" AS "head",
    "& stock in trade""" AS "stock_in_trade",
    "Poll tax no." AS "poll_tax_no",
    "Poll tax £" AS "poll_tax",
    "assessment",
    "(repeated)" AS "repeated",
    "Other notes" AS "other_notes",
    "Jpeg no." AS "jpeg_no",
    "Got land?" AS "got_land",
    ".. & land" AS "land",
    ".. No land" AS "no_land_2",
    "money at interest" AS "money_at_interest",
    """Money on hand""" AS "money_on_hand",
    "Got land and slaves" AS "got_land_and_slaves",
    "c1",
    "106",
    "98",
    "128",
    "332"
FROM "gpih-nc-3-counties-1779-82"
