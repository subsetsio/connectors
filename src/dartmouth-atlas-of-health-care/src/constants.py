"""Static data for the Dartmouth Atlas connector: the per-entity list of
longitudinal CSV.zip files to fetch. This is *data, not logic* (which files to
pull, harvested from each topic page during the collect stage) and lives outside
nodes/ so the loader never treats it as a node module.

The source is a frozen static archive (data.dartmouthatlas.org), so these URLs
are stable. All paths are relative to BASE.
"""

SLUG = "dartmouth-atlas-of-health-care"
BASE = "https://data.dartmouthatlas.org/"

# entity_id -> list of relative file paths (zipped CSVs) that union into that
# entity's one published table.
FILES = {
    "reimbursements": [
        "downloads/research_files/hrr_stdprices_ffs.csv.zip",
        "downloads/research_files/hsa_stdprices_ffs.csv.zip",
        "downloads/research_files/state_stdprices_ffs.csv.zip",
        "downloads/research_files/county_stdprices_ffs.csv.zip",
        "downloads/research_files/hrr_stdprices_2003_2010.csv.zip",
        "downloads/research_files/hsa_stdprices_2003_2010.csv.zip",
        "downloads/research_files/state_stdprices_2003_2010.csv.zip",
        "downloads/research_files/county_stdprices_2003_2010.csv.zip",
    ],
    "end-of-life-inpatient-care": [
        "downloads/research_files/hrr_eolmedpar_dead6699ffs.csv.zip",
        "downloads/research_files/hsa_eolmedpar_dead6699ffs.csv.zip",
        "downloads/research_files/state_eolmedpar_dead6699ffs.csv.zip",
        "downloads/research_files/county_eolmedpar_dead6699ffs.csv.zip",
        "downloads/research_files/hrr_eolmedpar_1994_2007.csv.zip",
        "downloads/research_files/hsa_eolmedpar_1994_2007.csv.zip",
        "downloads/research_files/state_eolmedpar_1994_2007.csv.zip",
    ],
    "care-chronically-ill-last-2yrs": [
        "downloads/research_files/hrr_eolchronic_dead6699ffs.csv.zip",
        "downloads/research_files/state_eolchronic_dead6699ffs.csv.zip",
        "downloads/research_files/hosp_eolchronic_dead6699ffs.csv.zip",
    ],
    "primary-care-access-quality": [
        "downloads/research_files/hrr_hedis_6575ffs.csv.zip",
        "downloads/research_files/hsa_hedis_6575ffs.csv.zip",
        "downloads/research_files/state_hedis_6575ffs.csv.zip",
        "downloads/research_files/county_hedis_6575ffs.csv.zip",
    ],
    "post-discharge-events": [
        "downloads/research_files/hrr_postdis_6599ffs.csv.zip",
        "downloads/research_files/hsa_postdis_6599ffs.csv.zip",
        "downloads/research_files/state_postdis_6599ffs.csv.zip",
        "downloads/research_files/county_postdis_6599ffs.csv.zip",
        "downloads/research_files/hosp_postdis_6599ffs.csv.zip",
    ],
    "discharge-rates": [
        "downloads/research_files/hrr_medutil_6599ffs.csv.zip",
        "downloads/research_files/hsa_medutil_6599ffs.csv.zip",
        "downloads/research_files/state_medutil_6599ffs.csv.zip",
        "downloads/research_files/county_medutil_6599ffs.csv.zip",
        "downloads/research_files/hrr_meddischarges_1992_2007.csv.zip",
        "downloads/research_files/hsa_meddischarges_1992_2007.csv.zip",
        "downloads/research_files/state_meddischarges_1992_2007.csv.zip",
        "downloads/research_files/hrr_surgicaldischarges_1992_2007.csv.zip",
        "downloads/research_files/hsa_surgicaldischarges_1992_2007.csv.zip",
        "downloads/research_files/state_surgicaldischarges_1992_2007.csv.zip",
    ],
    "geography-crosswalk": [
        "downloads/geography/ZipHsaHrr18.csv.zip",
        "downloads/geography/ZipHsaHrr19.csv.zip",
    ],
    "hospital-physician-capacity": [
        "downloads/tables/1996_hosp_phys_hrr.xls",
        "downloads/tables/1996_hosp_phys_hsa.xls",
        "downloads/tables/2006_hosp_phys_hrr.xls",
        "downloads/tables/2006_hosp_phys_hsa.xls",
        "downloads/tables/2011_phys_hrr.xls",
        "downloads/tables/2011_phys_hsa.xls",
        "downloads/tables/2012_hosp_resource_hrr.xls",
        "downloads/tables/2012_hosp_resource_hsa.xls",
    ],
    "hospital-research-data": [
        "downloads/research_files/hospital_research_data/hosp10_4983f.csv.zip",
        "downloads/research_files/hospital_research_data/hosp11_5231.csv.zip",
        "downloads/research_files/hospital_research_data/hosp12_5218.csv.zip",
        "downloads/research_files/hospital_research_data/hosp13_5186.csv.zip",
        "downloads/research_files/hospital_research_data/hosp14_5173_atlas.csv.zip",
        "downloads/research_files/hospital_research_data/hosp15_5130_atlas.csv.zip",
        "downloads/research_files/hospital_research_data/hosp16_atlas.csv.zip",
        "downloads/research_files/hospital_research_data/hosp17_atlas.csv.zip",
        "downloads/research_files/hospital_research_data/hospinfo08_14.csv.zip",
    ],
    "mortality": [
        "downloads/research_files/hrr_mortality_dead6599ffs.dta.zip",
        "downloads/research_files/state_mortality_dead6599ffs.dta.zip",
    ],
}

# Topic entities share the canonical long-format schema; the crosswalk does not.
TOPIC_ENTITIES = [
    "reimbursements",
    "end-of-life-inpatient-care",
    "care-chronically-ill-last-2yrs",
    "primary-care-access-quality",
    "post-discharge-events",
    "discharge-rates",
]

ENTITY_IDS = list(FILES.keys())
