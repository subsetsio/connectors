"""Opportunity Insights connector.

Two bulk-download surfaces, both per-entity stable-URL CSV fetches (no auth):
  * Economic Tracker GitHub repo — real-time indicator CSVs at
    raw.githubusercontent.com/OpportunityInsights/EconomicTracker/main/data/.
    A few are gzip-compressed (.csv.gz) and are decompressed before saving.
  * Data library — research-dataset CSVs hosted under
    opportunityinsights.org/wp-content/uploads/<YYYY>/<MM>/.

Both are immutable, full-table artefacts at persistent URLs, so the fetch is a
stateless full re-pull: download the whole CSV, save it verbatim as the raw
asset, and let the SQL transform (DuckDB read_csv_auto, SELECT *) type and
publish it. There is no incremental query surface on either host (no
since/cursor/fromDate); the maintain step gates whether a fetch runs.

The entity->URL map is baked in below from the collect catalog + rank-accepted
entity union (111 entities). Each spec id is f"opportunity-insights-{entity_id}".
"""

from __future__ import annotations

import gzip


from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

# entity_id -> {"url": str, "gzip": bool (optional)}
ENTITIES = {
    'lib-100-x-100-friendship-matrix': {"url": 'https://opportunityinsights.org/wp-content/uploads/2022/07/100_x_100_friendship_matrix.csv'},
    'lib-avg-auto-loan-balance-2020-cty': {"url": 'https://opportunityinsights.org/wp-content/uploads/2025/07/avg_auto_loan_balance_2020_cty.csv'},
    'lib-avg-auto-loan-balance-2020-cz': {"url": 'https://opportunityinsights.org/wp-content/uploads/2025/07/avg_auto_loan_balance_2020_cz.csv'},
    'lib-avg-credit-card-balance-2020-cty': {"url": 'https://opportunityinsights.org/wp-content/uploads/2025/07/avg_credit_card_balance_2020_cty.csv'},
    'lib-avg-credit-card-balance-2020-cz': {"url": 'https://opportunityinsights.org/wp-content/uploads/2025/07/avg_credit_card_balance_2020_cz.csv'},
    'lib-avg-credit-score-2020-cty': {"url": 'https://opportunityinsights.org/wp-content/uploads/2025/07/avg_credit_score_2020_cty.csv'},
    'lib-avg-credit-score-2020-cz': {"url": 'https://opportunityinsights.org/wp-content/uploads/2025/07/avg_credit_score_2020_cz.csv'},
    'lib-avg-delinq-rate-2020-cont-income-cty': {"url": 'https://opportunityinsights.org/wp-content/uploads/2025/07/avg_delinq_rate_2020_cont_income_cty.csv'},
    'lib-avg-delinq-rate-2020-cont-income-cz': {"url": 'https://opportunityinsights.org/wp-content/uploads/2025/07/avg_delinq_rate_2020_cont_income_cz.csv'},
    'lib-avg-delinq-rate-2020-cty': {"url": 'https://opportunityinsights.org/wp-content/uploads/2025/07/avg_delinq_rate_2020_cty.csv'},
    'lib-avg-delinq-rate-2020-cz': {"url": 'https://opportunityinsights.org/wp-content/uploads/2025/07/avg_delinq_rate_2020_cz.csv'},
    'lib-avg-mortgage-balance-2020-cty': {"url": 'https://opportunityinsights.org/wp-content/uploads/2025/07/avg_mortgage_balance_2020_cty.csv'},
    'lib-avg-mortgage-balance-2020-cz': {"url": 'https://opportunityinsights.org/wp-content/uploads/2025/07/avg_mortgage_balance_2020_cz.csv'},
    'lib-avg-student-loan-balance-2020-cty': {"url": 'https://opportunityinsights.org/wp-content/uploads/2025/07/avg_student_loan_balance_2020_cty.csv'},
    'lib-avg-student-loan-balance-2020-cz': {"url": 'https://opportunityinsights.org/wp-content/uploads/2025/07/avg_student_loan_balance_2020_cz.csv'},
    'lib-collegeadmissions-data': {"url": 'https://opportunityinsights.org/wp-content/uploads/2023/07/CollegeAdmissions_Data.csv'},
    'lib-county-outcomes-simple': {"url": 'https://opportunityinsights.org/wp-content/uploads/2018/10/county_outcomes_simple.csv'},
    'lib-cty-covariates': {"url": 'https://opportunityinsights.org/wp-content/uploads/2018/12/cty_covariates.csv'},
    'lib-cz-covariates': {"url": 'https://opportunityinsights.org/wp-content/uploads/2018/12/cz_covariates.csv'},
    'lib-cz-outcomes': {"url": 'https://opportunityinsights.org/wp-content/uploads/2018/10/cz_outcomes.csv'},
    'lib-cz-outcomes-simple': {"url": 'https://opportunityinsights.org/wp-content/uploads/2018/10/cz_outcomes_simple.csv'},
    'lib-health-ineq-online-table-1': {"url": 'https://opportunityinsights.org/wp-content/uploads/2018/04/health_ineq_online_table_1.csv'},
    'lib-health-ineq-online-table-10': {"url": 'https://opportunityinsights.org/wp-content/uploads/2018/04/health_ineq_online_table_10.csv'},
    'lib-health-ineq-online-table-11': {"url": 'https://opportunityinsights.org/wp-content/uploads/2018/04/health_ineq_online_table_11.csv'},
    'lib-health-ineq-online-table-12': {"url": 'https://opportunityinsights.org/wp-content/uploads/2018/04/health_ineq_online_table_12.csv'},
    'lib-health-ineq-online-table-13': {"url": 'https://opportunityinsights.org/wp-content/uploads/2018/04/health_ineq_online_table_13.csv'},
    'lib-health-ineq-online-table-14': {"url": 'https://opportunityinsights.org/wp-content/uploads/2018/04/health_ineq_online_table_14.csv'},
    'lib-health-ineq-online-table-15': {"url": 'https://opportunityinsights.org/wp-content/uploads/2018/04/health_ineq_online_table_15.csv'},
    'lib-health-ineq-online-table-16': {"url": 'https://opportunityinsights.org/wp-content/uploads/2018/08/health_ineq_online_table_16.csv'},
    'lib-health-ineq-online-table-16-4': {"url": 'https://opportunityinsights.org/wp-content/uploads/2018/09/health_ineq_online_table_16-4.csv'},
    'lib-health-ineq-online-table-2': {"url": 'https://opportunityinsights.org/wp-content/uploads/2018/04/health_ineq_online_table_2.csv'},
    'lib-health-ineq-online-table-3': {"url": 'https://opportunityinsights.org/wp-content/uploads/2018/04/health_ineq_online_table_3.csv'},
    'lib-health-ineq-online-table-4': {"url": 'https://opportunityinsights.org/wp-content/uploads/2018/04/health_ineq_online_table_4.csv'},
    'lib-health-ineq-online-table-5': {"url": 'https://opportunityinsights.org/wp-content/uploads/2018/04/health_ineq_online_table_5.csv'},
    'lib-health-ineq-online-table-6': {"url": 'https://opportunityinsights.org/wp-content/uploads/2018/04/health_ineq_online_table_6.csv'},
    'lib-health-ineq-online-table-7': {"url": 'https://opportunityinsights.org/wp-content/uploads/2018/04/health_ineq_online_table_7.csv'},
    'lib-health-ineq-online-table-8': {"url": 'https://opportunityinsights.org/wp-content/uploads/2018/04/health_ineq_online_table_8.csv'},
    'lib-health-ineq-online-table-9': {"url": 'https://opportunityinsights.org/wp-content/uploads/2018/04/health_ineq_online_table_9.csv'},
    'lib-hopevi-all-candidate-neighborhoods': {"url": 'https://opportunityinsights.org/wp-content/uploads/2026/01/HOPEVI_All_Candidate_Neighborhoods.csv'},
    'lib-hopevi-candidate-neighborhoods-for-connection-based-revitalization': {"url": 'https://opportunityinsights.org/wp-content/uploads/2026/01/HOPEVI_Candidate_Neighborhoods_For_Connection_Based_Revitalization.csv'},
    'lib-mrc-table1': {"url": 'https://opportunityinsights.org/wp-content/uploads/2018/03/mrc_table1.csv'},
    'lib-mrc-table10': {"url": 'https://opportunityinsights.org/wp-content/uploads/2018/04/mrc_table10.csv'},
    'lib-mrc-table11': {"url": 'https://opportunityinsights.org/wp-content/uploads/2018/04/mrc_table11.csv'},
    'lib-mrc-table12': {"url": 'https://opportunityinsights.org/wp-content/uploads/2019/01/mrc_table12.csv'},
    'lib-mrc-table13': {"url": 'https://opportunityinsights.org/wp-content/uploads/2019/01/mrc_table13.csv'},
    'lib-mrc-table14': {"url": 'https://opportunityinsights.org/wp-content/uploads/2019/01/mrc_table14.csv'},
    'lib-mrc-table15': {"url": 'https://opportunityinsights.org/wp-content/uploads/2020/06/mrc_table15.csv'},
    'lib-mrc-table2': {"url": 'https://opportunityinsights.org/wp-content/uploads/2018/04/mrc_table2.csv'},
    'lib-mrc-table3': {"url": 'https://opportunityinsights.org/wp-content/uploads/2018/04/mrc_table3.csv'},
    'lib-mrc-table4': {"url": 'https://opportunityinsights.org/wp-content/uploads/2018/04/mrc_table4.csv'},
    'lib-mrc-table5-1': {"url": 'https://opportunityinsights.org/wp-content/uploads/2018/04/mrc_table5-1.csv'},
    'lib-mrc-table6': {"url": 'https://opportunityinsights.org/wp-content/uploads/2018/04/mrc_table6.csv'},
    'lib-mrc-table7': {"url": 'https://opportunityinsights.org/wp-content/uploads/2018/04/mrc_table7.csv'},
    'lib-mrc-table8': {"url": 'https://opportunityinsights.org/wp-content/uploads/2018/04/mrc_table8.csv'},
    'lib-mrc-table9': {"url": 'https://opportunityinsights.org/wp-content/uploads/2018/04/mrc_table9.csv'},
    'lib-national-percentile-outcomes': {"url": 'https://opportunityinsights.org/wp-content/uploads/2018/10/national_percentile_outcomes.csv'},
    'lib-od': {"url": 'https://opportunityinsights.org/wp-content/uploads/2022/07/od.csv'},
    'lib-od-inc': {"url": 'https://opportunityinsights.org/wp-content/uploads/2022/07/od_inc.csv'},
    'lib-od-pooled': {"url": 'https://opportunityinsights.org/wp-content/uploads/2022/07/od_pooled.csv'},
    'lib-od-race': {"url": 'https://opportunityinsights.org/wp-content/uploads/2022/07/od_race.csv'},
    'lib-race-table6a-parametric': {"url": 'https://opportunityinsights.org/wp-content/uploads/2019/08/race_table6a_parametric.csv'},
    'lib-race-table6b-nonpar': {"url": 'https://opportunityinsights.org/wp-content/uploads/2019/08/race_table6b_nonpar.csv'},
    'lib-table-1-county-trends-estimates': {"url": 'https://opportunityinsights.org/wp-content/uploads/2024/07/Table_1_county_trends_estimates.csv'},
    'lib-table-2-cz-trends-estimates': {"url": 'https://opportunityinsights.org/wp-content/uploads/2024/07/Table_2_cz_trends_estimates.csv'},
    'lib-table-3-county-by-cohort-estimates': {"url": 'https://opportunityinsights.org/wp-content/uploads/2024/07/Table_3_County_by_Cohort_Estimates.csv'},
    'lib-table-4-cz-by-cohort-estimates': {"url": 'https://opportunityinsights.org/wp-content/uploads/2024/07/Table_4_cz_by_cohort_estimates.csv'},
    'lib-table-5-national-estimates-by-cohort-primary-outcomes': {"url": 'https://opportunityinsights.org/wp-content/uploads/2024/07/Table_5_national_estimates_by_cohort_primary_outcomes.csv'},
    'lib-table-6-national-estimates-by-cohort-secondary-outcomes': {"url": 'https://opportunityinsights.org/wp-content/uploads/2024/07/Table_6_national_estimates_by_cohort_secondary_outcomes.csv'},
    'lib-table-8-county-covariates': {"url": 'https://opportunityinsights.org/wp-content/uploads/2024/07/Table_8_county_covariates.csv'},
    'lib-table-9-cz-covariates': {"url": 'https://opportunityinsights.org/wp-content/uploads/2024/07/Table_9_cz_covariates.csv'},
    'lib-tract-covariates': {"url": 'https://opportunityinsights.org/wp-content/uploads/2018/10/tract_covariates.csv'},
    'lib-tract-outcomes-late-simple': {"url": 'https://opportunityinsights.org/wp-content/uploads/2024/08/tract_outcomes_late_simple.csv'},
    'lib-tract-outcomes-simple': {"url": 'https://opportunityinsights.org/wp-content/uploads/2018/10/tract_outcomes_simple.csv'},
    'tracker-affinity-city-daily': {"url": 'https://raw.githubusercontent.com/OpportunityInsights/EconomicTracker/main/data/Affinity%20-%20City%20-%20Daily.csv'},
    'tracker-affinity-city-monthly': {"url": 'https://raw.githubusercontent.com/OpportunityInsights/EconomicTracker/main/data/Affinity%20-%20City%20-%20Monthly.csv'},
    'tracker-affinity-county-daily': {"url": 'https://raw.githubusercontent.com/OpportunityInsights/EconomicTracker/main/data/Affinity%20-%20County%20-%20Daily.csv'},
    'tracker-affinity-county-monthly': {"url": 'https://raw.githubusercontent.com/OpportunityInsights/EconomicTracker/main/data/Affinity%20-%20County%20-%20Monthly.csv'},
    'tracker-affinity-daily-total-spending-national': {"url": 'https://raw.githubusercontent.com/OpportunityInsights/EconomicTracker/main/data/Affinity%20Daily%20Total%20Spending%20-%20National.csv'},
    'tracker-affinity-national-daily': {"url": 'https://raw.githubusercontent.com/OpportunityInsights/EconomicTracker/main/data/Affinity%20-%20National%20-%20Daily.csv'},
    'tracker-affinity-national-monthly': {"url": 'https://raw.githubusercontent.com/OpportunityInsights/EconomicTracker/main/data/Affinity%20-%20National%20-%20Monthly.csv'},
    'tracker-affinity-state-daily': {"url": 'https://raw.githubusercontent.com/OpportunityInsights/EconomicTracker/main/data/Affinity%20-%20State%20-%20Daily.csv'},
    'tracker-affinity-state-monthly': {"url": 'https://raw.githubusercontent.com/OpportunityInsights/EconomicTracker/main/data/Affinity%20-%20State%20-%20Monthly.csv'},
    'tracker-covid-city-daily': {"url": 'https://raw.githubusercontent.com/OpportunityInsights/EconomicTracker/main/data/COVID%20-%20City%20-%20Daily.csv'},
    'tracker-covid-county-daily-2020': {"url": 'https://raw.githubusercontent.com/OpportunityInsights/EconomicTracker/main/data/COVID%20-%20County%20-%20Daily%202020.csv'},
    'tracker-covid-county-daily-2021': {"url": 'https://raw.githubusercontent.com/OpportunityInsights/EconomicTracker/main/data/COVID%20-%20County%20-%20Daily%202021.csv.gz', "gzip": True},
    'tracker-covid-county-daily-2022': {"url": 'https://raw.githubusercontent.com/OpportunityInsights/EconomicTracker/main/data/COVID%20-%20County%20-%20Daily%202022.csv.gz', "gzip": True},
    'tracker-covid-county-daily-2023': {"url": 'https://raw.githubusercontent.com/OpportunityInsights/EconomicTracker/main/data/COVID%20-%20County%20-%20Daily%202023.csv'},
    'tracker-covid-national-daily': {"url": 'https://raw.githubusercontent.com/OpportunityInsights/EconomicTracker/main/data/COVID%20-%20National%20-%20Daily.csv'},
    'tracker-covid-state-daily': {"url": 'https://raw.githubusercontent.com/OpportunityInsights/EconomicTracker/main/data/COVID%20-%20State%20-%20Daily.csv'},
    'tracker-employment-city-weekly': {"url": 'https://raw.githubusercontent.com/OpportunityInsights/EconomicTracker/main/data/Employment%20-%20City%20-%20Weekly.csv'},
    'tracker-employment-county-weekly': {"url": 'https://raw.githubusercontent.com/OpportunityInsights/EconomicTracker/main/data/Employment%20-%20County%20-%20Weekly.csv'},
    'tracker-employment-national-weekly': {"url": 'https://raw.githubusercontent.com/OpportunityInsights/EconomicTracker/main/data/Employment%20-%20National%20-%20Weekly.csv'},
    'tracker-employment-state-weekly': {"url": 'https://raw.githubusercontent.com/OpportunityInsights/EconomicTracker/main/data/Employment%20-%20State%20-%20Weekly.csv'},
    'tracker-google-mobility-county-daily': {"url": 'https://raw.githubusercontent.com/OpportunityInsights/EconomicTracker/main/data/Google%20Mobility%20-%20County%20-%20Daily.csv.gz', "gzip": True},
    'tracker-google-mobility-national-daily': {"url": 'https://raw.githubusercontent.com/OpportunityInsights/EconomicTracker/main/data/Google%20Mobility%20-%20National%20-%20Daily.csv'},
    'tracker-google-mobility-state-daily': {"url": 'https://raw.githubusercontent.com/OpportunityInsights/EconomicTracker/main/data/Google%20Mobility%20-%20State%20-%20Daily.csv'},
    'tracker-job-postings-city-weekly': {"url": 'https://raw.githubusercontent.com/OpportunityInsights/EconomicTracker/main/data/Job%20Postings%20-%20City%20-%20Weekly.csv'},
    'tracker-job-postings-county-weekly': {"url": 'https://raw.githubusercontent.com/OpportunityInsights/EconomicTracker/main/data/Job%20Postings%20-%20County%20-%20Weekly.csv'},
    'tracker-job-postings-national-weekly': {"url": 'https://raw.githubusercontent.com/OpportunityInsights/EconomicTracker/main/data/Job%20Postings%20-%20National%20-%20Weekly.csv'},
    'tracker-job-postings-state-weekly': {"url": 'https://raw.githubusercontent.com/OpportunityInsights/EconomicTracker/main/data/Job%20Postings%20-%20State%20-%20Weekly.csv'},
    'tracker-ui-claims-city-weekly': {"url": 'https://raw.githubusercontent.com/OpportunityInsights/EconomicTracker/main/data/UI%20Claims%20-%20City%20-%20Weekly.csv'},
    'tracker-ui-claims-county-weekly': {"url": 'https://raw.githubusercontent.com/OpportunityInsights/EconomicTracker/main/data/UI%20Claims%20-%20County%20-%20Weekly.csv'},
    'tracker-ui-claims-national-weekly': {"url": 'https://raw.githubusercontent.com/OpportunityInsights/EconomicTracker/main/data/UI%20Claims%20-%20National%20-%20Weekly.csv'},
    'tracker-ui-claims-state-weekly': {"url": 'https://raw.githubusercontent.com/OpportunityInsights/EconomicTracker/main/data/UI%20Claims%20-%20State%20-%20Weekly.csv'},
    'tracker-womply-city-weekly': {"url": 'https://raw.githubusercontent.com/OpportunityInsights/EconomicTracker/main/data/Womply%20-%20City%20-%20Weekly.csv'},
    'tracker-womply-county-weekly': {"url": 'https://raw.githubusercontent.com/OpportunityInsights/EconomicTracker/main/data/Womply%20-%20County%20-%20Weekly.csv'},
    'tracker-womply-national-weekly': {"url": 'https://raw.githubusercontent.com/OpportunityInsights/EconomicTracker/main/data/Womply%20-%20National%20-%20Weekly.csv'},
    'tracker-womply-state-weekly': {"url": 'https://raw.githubusercontent.com/OpportunityInsights/EconomicTracker/main/data/Womply%20-%20State%20-%20Weekly.csv'},
    'tracker-zearn-county-weekly': {"url": 'https://raw.githubusercontent.com/OpportunityInsights/EconomicTracker/main/data/Zearn%20-%20County%20-%20Weekly.csv'},
    'tracker-zearn-national-weekly': {"url": 'https://raw.githubusercontent.com/OpportunityInsights/EconomicTracker/main/data/Zearn%20-%20National%20-%20Weekly.csv'},
    'tracker-zearn-state-weekly': {"url": 'https://raw.githubusercontent.com/OpportunityInsights/EconomicTracker/main/data/Zearn%20-%20State%20-%20Weekly.csv'},
}


@transient_retry()
def _download(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


def _to_utf8(raw: bytes) -> bytes:
    """Some legacy data-library CSVs are Stata exports encoded in
    Windows-1252/Latin-1, which DuckDB's strict reader rejects. Normalize to
    UTF-8 so parsing is uniform. Already-UTF-8 payloads pass through untouched."""
    try:
        raw.decode("utf-8")
        return raw
    except UnicodeDecodeError:
        # cp1252 is a superset of latin-1 and maps every byte, so this never raises.
        return raw.decode("cp1252").encode("utf-8")


def _csv_to_table(raw: bytes):
    """Parse CSV bytes into a typed Arrow table via DuckDB with FULL-file type
    detection (sample_size=-1). Parsing here — rather than letting the SQL
    transform's auto-view sample only the first ~20k rows — means a column whose
    distinguishing values appear late (e.g. a 'gnd' column that is 0/1 for 40k
    rows then 'M'/'F') is typed correctly as VARCHAR instead of mis-inferred as
    BOOLEAN and failing mid-scan. DuckDB widens to whatever type fits every row,
    so the conversion never raises on a stray value."""
    import os
    import tempfile

    import duckdb

    fd, path = tempfile.mkstemp(suffix=".csv")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(raw)
        con = duckdb.connect()
        try:
            return con.sql(
                f"SELECT * FROM read_csv_auto('{path}', sample_size=-1)"
            ).to_arrow_table()
        finally:
            con.close()
    finally:
        os.unlink(path)


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    entity_id = node_id[len("opportunity-insights-"):]
    meta = ENTITIES[entity_id]
    raw = _download(meta["url"])
    if meta.get("gzip"):
        raw = gzip.decompress(raw)
    raw = _to_utf8(raw)
    table = _csv_to_table(raw)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"opportunity-insights-{eid}", fn=fetch_one, kind="download")
    for eid in ENTITIES
]

# Thin pass-through publish: DuckDB auto-detects schema/nulls from each CSV.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}"',
    )
    for s in DOWNLOAD_SPECS
]
