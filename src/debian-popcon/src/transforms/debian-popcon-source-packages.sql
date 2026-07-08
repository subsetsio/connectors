SELECT
    rank,
    name AS source_package,
    inst,
    vote,
    old,
    recent,
    no_files
FROM "debian-popcon-source-packages"
