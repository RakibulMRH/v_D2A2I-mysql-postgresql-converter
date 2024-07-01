MySQL to PostgreSQL Converter
============================= 

Updated Lanyrd's MySQL to PostgreSQL conversion script:

Minor Bug fixes for Python 3.12.3+ versions 

Added 4 new table creation format support for the converter

Major changes in Sequence format convertions

This script was designed for our specific database and column requirements -
notably, it doubles the lengths of VARCHARs due to a unicode size problem we
had, places indexes on all foreign keys, and presumes you're using Django
for column typing purposes.

NOTE: Triggers and Stored procedures are not compatible with this converter yet

How to use
----------
Here is a GitHub README file with the necessary commands and one-click copy buttons for ease of use:

```markdown
# MySQL to PostgreSQL Dump and Import

This guide provides step-by-step instructions for creating dumps of MySQL tables and importing them into PostgreSQL.

## Steps

### 1. Create Dump of the Skeleton

```sh
mysqldump --compatible=postgresql --default-character-set=utf8 -u root -p --no-data --skip-triggers --skip-routines --skip-events --skip-add-locks --skip-lock-tables testd2 > "E:\AIUB\DA2I2 Internship\Resources\alltables.mysql"
```

#### Convert using `db_converterSkeleton.py`

```sh
python db_converterSkeleton.py alltables.mysql skeleton.psql
```

#### Import using `import_psql.py` or use this command from the PostgreSQL bin directory

```sh
psql -h localhost -d test -U postgres -f "E:\AIUB\DA2I2 Internship\Resources\skeleton.psql"
```

### 2. Create Dump of All Data

```sh
mysqldump --compatible=postgresql --default-character-set=utf8 -u root -p --no-create-info --skip-triggers --skip-routines --skip-events --skip-add-locks --skip-lock-tables testd2 > "E:\AIUB\DA2I2 Internship\Resources\alldata.mysql"
```

#### Convert using `db_converter2.py`

```sh
python db_converter2.py alldata.mysql convertedtables.psql
```

#### Import using `import_psql.py` (change the PostgreSQL and other directories inside the code)

### 3. Create Dump of the Exceptional Tables

```sh
mysqldump --compatible=postgresql --default-character-set=utf8 -u root -p --no-create-info --skip-triggers --skip-routines --skip-events --skip-add-locks --skip-lock-tables testd2 view_logs dayparts dayparts_process view_logs_archive device_history_log device_boxes deployer_info deselect_logs deselect_periods devices data_reliability > "E:\AIUB\DA2I2 Internship\Resources\selected_tables.mysql"
```

#### Convert using `db_converter.py`

```sh
python db_converter.py selected_tables.mysql convertedtables.psql
```

#### Import using `import_psql.py` (change the PostgreSQL and other directories inside the code)
```

For each section, I included the one-click copy buttons to simplify copying commands. You can paste this README into your GitHub repository. The commands are in code blocks, so users can copy them with a single click.
