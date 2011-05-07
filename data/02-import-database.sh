#!/bin/sh
cd calima
YEARS=`ls ../datos/*.CSV.gz`
for y in $YEARS
do
    year=`echo $y | sed -e "s/..\/datos\/\(.*\).CSV.gz/\1/"`
    python manage.py generatedata ../datos $year
done
cd -
