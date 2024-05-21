MySQL to PostgreSQL Converter
============================= 

Rakibul's additions to Lanyrd's MySQL to PostgreSQL conversion script:

Minor Bug fixes for Python 3.12.3+ versions 

4 new table creation format support is added
Major changes in Sequence format convertions

This script was designed for our specific database and column requirements -
notably, it doubles the lengths of VARCHARs due to a unicode size problem we
had, places indexes on all foreign keys, and presumes you're using Django
for column typing purposes.

NOTE: Triggers and Stored procedures are not compatible with this converter yet

How to use
----------

First, dump your MySQL database in PostgreSQL-compatible format

    mysqldump --compatible=postgresql --default-character-set=utf8 -u root -p --no-data --skip-triggers --skip-routines --skip-events --skip-add-locks --skip-lock-tables databasename > dumpfilename.mysql

Then, convert it using the dbconverter.py script

`python db_converter.py dumpfilename.mysql databasename.psql`

It'll print progress to the terminal.

Finally, load your new dump into a fresh PostgreSQL database using: 

`psql -f databasename.psql`

or, open cmd from your PostgreSQL bin directory and load file using:

`psql -h localhost -d databasename -U username -f "path\to\your\databasename.psql"`

More information
----------------

You can learn more about the move which this powered at http://lanyrd.com/blog/2012/lanyrds-big-move/ and some technical details of it at http://www.aeracode.org/2012/11/13/one-change-not-enough/.
