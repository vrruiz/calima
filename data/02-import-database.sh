#!/bin/sh
cd ../calima
YEARS=`ls ../data/datos/*.CSV.gz`
for y in $YEARS
do
    year=`echo $y | sed -e "s/..\/data\/datos\/\(.*\).CSV.gz/\1/"`
    print $year
    python manage.py importer ../data/datos $year
done
cd -
