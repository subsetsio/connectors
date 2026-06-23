import duckdb, re, importlib.util, sys
spec = importlib.util.spec_from_file_location("mod","src/nodes/eg_capmas.py")
# import without subsets_utils side effects: just read TRANSFORM_SPECS sql via regex is messy; build views manually
con = duckdb.connect()
con.execute("""CREATE TABLE "eg-capmas-subjects" AS SELECT * FROM (VALUES
  (1,'Economy','اقتصاد',13,'Prices','اسعار'),
  (1,'Economy','اقتصاد',13,'Prices','اسعار'),
  (2,'Social','اجتماعي',21,'Vital','حيوي')) t(main_subject_id,main_subject_en,main_subject_ar,sub_subject_id,sub_subject_en,sub_subject_ar);""")
con.execute("""CREATE TABLE "eg-capmas-indicators" AS SELECT * FROM (VALUES
  (3505,'Poultry prices','اسعار',1,'Economy',13,'Prices',60,'Index','مؤشر','Annually','EGP','جنيه',1998,2025),
  (3505,'Poultry prices','اسعار',1,'Economy',13,'Prices',61,'Index','مؤشر','Annually','EGP','جنيه',1998,2025),
  (49,'Food index','غذاء',1,'Economy',13,'Prices',3,'Index','مؤشر','Annually','idx','مؤشر',2000,2024))
  t(indicator_id,name_en,name_ar,main_subject_id,main_subject_en,sub_subject_id,sub_subject_en,publication_id,publication_en,publication_ar,periodicity_en,measure_unit_en,measure_unit_ar,start_year,end_year);""")
con.execute("""CREATE TABLE "eg-capmas-values" AS SELECT * FROM (VALUES
  (1,13,3505,'Poultry','1370','Rabbits','أرانب',2022,NULL,NULL,44.7),
  (1,13,3505,'Poultry','1370','Rabbits','أرانب',2022,NULL,NULL,44.7),
  (1,13,3505,'Poultry','1370','Rabbits','أرانب',2021,NULL,NULL,39.5),
  (1,13,49,'Food','188','Eggs','بيض',2016,2,3,6.3),
  (1,13,49,'Food','188','Eggs','بيض',2016,NULL,NULL,NULL))
  t(main_subject_id,sub_subject_id,indicator_id,indicator_name_en,category_id,category_en,category_ar,year,quarter,month,value);""")

# pull the SQL strings out of the module source
src=open("src/nodes/eg_capmas.py").read()
for m in re.finditer(r'id="(eg-capmas-[a-z]+-transform)",\s*deps=\[[^\]]*\],\s*sql=\'\'\'(.*?)\'\'\'', src, re.S):
    tid,sql=m.group(1),m.group(2)
    print("===",tid,"===")
    try:
        r=con.execute(sql).fetchall()
        cols=[d[0] for d in con.description]
        print("rows:",len(r),"cols:",cols)
        for row in r[:3]: print("  ",row)
    except Exception as e:
        print("SQL ERROR:",e); sys.exit(1)
print("\nALL TRANSFORMS OK")
