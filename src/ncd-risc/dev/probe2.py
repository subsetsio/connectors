import io, zipfile, csv
from subsets_utils import get

samples = {
 "bp_country_ageStd": "https://www.ncdrisc.org/downloads/bp/NCD_RisC_Lancet_2017_BP_age_standardised_countries.csv",
 "bp_men_agespec": "https://www.ncdrisc.org/downloads/bp/NCD_RisC_Lancet_2017_Men_Agespecific_Mean_SBP_by_Country.csv",
 "height_global": "https://www.ncdrisc.org/downloads/bmi-height-2020/height/global/NCD_RisC_Lancet_2020_height_child_adolescent_global.csv",
 "hyp_country": "https://www.ncdrisc.org/downloads/hypertension/NCD-RisC_Lancet_2021_Hypertension_age_standardised_countries.csv",
 "hyp_agespec": "https://www.ncdrisc.org/downloads/hypertension/NCD-RisC_Lancet_2021_Hypertension_age_specific_estimates_by_country.csv",
 "chol_country": "https://www.ncdrisc.org/downloads/chol/NCD_RisC_Nature_2020_Cholesterol_age_standardised_countries.csv",
 "chol_agespec": "https://www.ncdrisc.org/downloads/chol/NCD_RisC_Nature_2020_Cholesterol_age_specific_countries.csv",
 "bmi_country": "https://www.ncdrisc.org/downloads/bmi-2026/adult/NCD_RisC_Nature_2026_BMI_age_standardised_country.csv",
}
for label, u in samples.items():
    try:
        r = get(u, timeout=(10.0,60.0)); r.raise_for_status()
        rows = list(csv.reader(io.StringIO(r.content.decode("utf-8","replace"))))
        print(f"== {label} == nrows={len(rows)}")
        print("  H:", rows[0])
        print("  1:", rows[1])
    except Exception as e:
        print(label, "ERR", type(e).__name__, repr(e)[:150])

# ZIP families
zips = {
 "height_country_zip": "https://www.ncdrisc.org/downloads/bmi-height-2020/height/all_countries/NCD_RisC_Lancet_2020_height_child_adolescent_country.zip",
 "diabetes_agespec_zip": "https://www.ncdrisc.org/downloads/dm-2024/NCD_RisC_Lancet_2024_Diabetes_age_specific_countries.zip",
 "bmi_male_agespec_zip": "https://www.ncdrisc.org/downloads/bmi-2026/adult/NCD_RisC_Nature_2026_BMI_male_age_specific_country.zip",
}
for label, u in zips.items():
    try:
        r = get(u, timeout=(10.0,120.0)); r.raise_for_status()
        zf = zipfile.ZipFile(io.BytesIO(r.content))
        names = zf.namelist()
        print(f"== {label} == members={len(names)} sample_names={names[:3]}")
        # find first csv member
        csvm = [n for n in names if n.lower().endswith('.csv')]
        if csvm:
            with zf.open(csvm[0]) as f:
                rows = list(csv.reader(io.TextIOWrapper(f, encoding='utf-8', errors='replace')))
            print("  member:", csvm[0], "nrows=", len(rows))
            print("  H:", rows[0])
            print("  1:", rows[1])
    except Exception as e:
        print(label, "ERR", type(e).__name__, repr(e)[:150])
