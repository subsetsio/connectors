SELECT DISTINCT
    ghsa_id,
    ecosystem,
    package_name,
    vulnerable_version_range,
    first_patched_version,
    source_directory
FROM "github-affected"
WHERE ghsa_id IS NOT NULL
  AND ecosystem IS NOT NULL
  AND package_name IS NOT NULL
