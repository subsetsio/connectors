SELECT
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "mortgage_backed_securities",
    "federal_agency_debt_securities",
    "federal_agency_debt_and_mortgage_backed_securities_purchases"
FROM "cleveland-fed-crediteasing-fedagencydebtmbs"
