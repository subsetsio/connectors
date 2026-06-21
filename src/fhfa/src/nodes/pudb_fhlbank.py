"""PUDB FHLBank (Acquired Member Assets) — clean per-year CSV, latest only."""

from __future__ import annotations

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet

from utils import _csv_bytes_to_string_table, _current_year, _get_optional

PUDB_FHLB_URL = "https://www.fhfa.gov/document/d/pud/{year}-pudb.csv"
PUDB_FHLB_COLS = [
    "Year", "LoanCharacteristicsID", "Bank", "FIPSStateNumericCode",
    "FIPSCountyCode", "CoreBasedStatisticalAreaCode", "CensusTractIdentifier",
    "CensusTractMinorityRatioPercent", "CensusTractMedFamIncomeAmount",
    "LocalAreaMedianIncomeAmount", "TotalMonthlyIncomeAmount",
    "HUDMedianIncomeAmount", "LoanAcquisitionActualUPBAmt", "LTVRatioPercent",
    "NoteDate", "LoanAcquisitionDate", "LoanPurposeType", "ProductCategoryName",
    "MortgageType", "ScheduledTotalPaymentCount", "LoanAmortizationMaxTermMonths",
    "MortgageLoanSellerInstType", "BorrowerCount", "BorrowerFirstTimeHomebuyer",
    "Borrower1Race1Type", "Borrower2Race1Type", "Borrower1SexType",
    "Borrower2SexType", "Borrower1AgeAtApplicationYears",
    "Borrower2AgeAtApplicationYears", "PropertyUsageType", "PropertyUnitCount",
    "NoteRatePercent", "NoteAmount", "HousingExpenseRatioPercent",
    "TotalDebtExpenseRatioPercent", "Borrower1CreditScoreValue",
    "Borrower2CreditScoreValue", "PMICoveragePercent",
    "EmploymentBorrowerSelfEmployed", "PropertyType", "IndexSourceType",
    "MarginRatePercent", "PrepaymentPenaltyExpirationDate",
    "Borrower1EthnicityType", "Borrower1Race2Type", "Borrower1Race3Type",
    "Borrower1Race4Type", "Borrower1Race5Type", "Borrower2EthnicityType",
    "Borrower2Race2Type", "Borrower2Race3Type", "Borrower2Race4Type",
    "Borrower2Race5Type", "HOEPALoanStatusType", "LienPriorityType",
]


def fetch_pudb_fhlbank(node_id: str) -> None:
    for year in range(_current_year() + 2, 2007, -1):
        resp = _get_optional(PUDB_FHLB_URL.format(year=year))
        if resp is None:
            continue
        # strip a possible UTF-8 BOM on the first column name
        data = resp.content
        if data[:3] == b"\xef\xbb\xbf":
            data = data[3:]
        table = _csv_bytes_to_string_table(data, PUDB_FHLB_COLS)
        save_raw_parquet(table, node_id)
        return
    raise AssertionError("no FHLBank PUDB release found for any year")


_FHLB_NUMERIC = [
    "CensusTractMinorityRatioPercent", "CensusTractMedFamIncomeAmount",
    "LocalAreaMedianIncomeAmount", "TotalMonthlyIncomeAmount",
    "HUDMedianIncomeAmount", "LoanAcquisitionActualUPBAmt", "LTVRatioPercent",
    "ScheduledTotalPaymentCount", "LoanAmortizationMaxTermMonths",
    "BorrowerCount", "Borrower1AgeAtApplicationYears",
    "Borrower2AgeAtApplicationYears", "PropertyUnitCount", "NoteRatePercent",
    "NoteAmount", "HousingExpenseRatioPercent", "TotalDebtExpenseRatioPercent",
    "Borrower1CreditScoreValue", "Borrower2CreditScoreValue",
    "PMICoveragePercent", "MarginRatePercent",
]
_FHLB_REPLACE = ",\n                ".join(
    ["TRY_CAST(NULLIF(\"Year\", '') AS INTEGER) AS \"Year\""]
    + [f"TRY_CAST(NULLIF(\"{c}\", '') AS DOUBLE) AS \"{c}\"" for c in _FHLB_NUMERIC]
)


DOWNLOAD_SPECS = [
    NodeSpec(id="fhfa-pudb-fhlbank", fn=fetch_pudb_fhlbank, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="fhfa-pudb-fhlbank-transform",
        deps=["fhfa-pudb-fhlbank"],
        sql=f'''
            SELECT * REPLACE (
                {_FHLB_REPLACE}
            )
            FROM "fhfa-pudb-fhlbank"
        ''',
    ),
]
