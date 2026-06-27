"""Entity union for the Migration Policy Institute connector.

`FILENAMES` maps each rank-active entity id (the entity union) to the current
basename of its Data Hub Excel file under
https://www.migrationpolicy.org/sites/default/files/datahub/ . These are data,
not logic: every filename was verified live (HTTP 200, real Excel) on 2026-06-27.

URL-stability caveat (from research): year-suffixed filenames are replaced on the
source's annual update, so a future refresh may need these basenames refreshed.
"""

FILENAMES = {
    "black-immigrants": "mpi-black-immigrants-data-appendix_final.xlsx",
    "children-in-immigrant-families": "MPI-Data-Hub-Children-in-Immigrant-Families_1990-2024.xlsx",
    "diaspora-top-origins": "_Estimates_diaspora_Top_origins_UPDATE.xlsx",
    "dual-language-learners-children": "us-dll-children-profiles-age0-8-2019-2023.xlsx",
    "educational-attainment-by-nativity": "MPI-Data-Hub_EduAttainment-Nativity & byCOB_2024.xlsx",
    "immigrant-population-by-region-of-birth": "MPI-Data-Hub-Region-Birth_1960-2024.xlsx",
    "immigrant-population-share-by-state": "MPI-Data-Hub_Immigrants_N-Percent-US-Population by State_2024.xlsx",
    "immigrant-population-share-us": "MPI-Data-Hub_Imm_N-Percent-US-Pop_2024.xlsx",
    "immigrants-in-labor-force-by-state": "since_1980_Imm_in_labor_force_by_state_UPDATE.xlsx",
    "lep-fb-adults-by-citizenship-status": "MPIDataHub_State-level-LEP-FB-Adults-by-USCitz-Status_UPDATE.xlsx",
    "lep-population-by-state": "MPI-Data-Hub_LEP-Population_US-States_1990-2024.xlsx",
    "lpr-inflow-by-country-of-birth": "MPIDataHub_USInflowLPRsbyCOB_0.xlsx",
    "lpr-trend-since-1820": "MPI-Data-Hub_LPRTrend_1820-2023.xlsx",
    "lprs-by-country-of-birth": "MPI-Data-Hub_LPRsbyCOB_2023.xlsx",
    "mexican-immigrants": "MPI-Data-Hub_Mexican-Immigrants-US_2024.xlsx",
    "naturalizations-by-country-of-birth": "MPI-Data-Hub_NaturalizationbyCOB_2023.xlsx",
    "new-us-citizens-since-1910": "MPI-Data-Hub_US-New-Citizens_1910-2023.xlsx",
    "postsecondary-credentials": "MPI_PostsecondaryCredentials_2023.xlsx",
    "refugee-admissions": "MPI-Data-Hub_Refugee-Admissions_1980-2026(Oct-Feb).xlsx",
    "unaccompanied-children-by-state-county": "MPI-Data-Hub_UACsbyState-County-FY2014-FY2025.xlsx",
    "unauthorized-state-county-estimates": "State-County-Unauthorized-Estimates.xlsx",
}

ENTITY_IDS = list(FILENAMES)
