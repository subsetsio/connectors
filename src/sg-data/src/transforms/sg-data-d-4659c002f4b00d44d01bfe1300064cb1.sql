-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Reference_No" AS reference_no,
    "Year_Issue" AS year_issue,
    "Company" AS company,
    "Branch" AS branch,
    "Type_of_Entity" AS type_of_entity,
    "Supervising_Director" AS supervising_director,
    "Total_No_Of_Directors_Employees_Who_are_PE_with_PC" AS total_no_of_directors_employees_who_are_pe_with_pc,
    "Company_Address" AS company_address,
    "Contact_No" AS contact_no
FROM "sg-data-d-4659c002f4b00d44d01bfe1300064cb1"
