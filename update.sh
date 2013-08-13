#/usr/bin/bash

path= YOUR PATH
cd $path;

rm forecast_hour_by_hour.xml*
wget http://www.yr.no/place/Croatia/Grad_Zagreb/Zagreb/forecast_hour_by_hour.xml; 
cat conky_template > conky2.conf; 
python prognoza.py >> conky2.conf;


cd;
killall conky;
sh ~/.conky_start