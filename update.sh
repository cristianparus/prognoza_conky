#/usr/bin/bash

path=/mnt/data/projekti/prognoza/
cd $path;


rm forecast_hour_by_hour.xml*
wget http://www.yr.no/place/Croatia/Grad_Zagreb/Zagreb/forecast_hour_by_hour.xml; 
cat conky_template > conky.conf; 
python prognoza.py >> conky.conf;


cd;
killall conky;
sh ~/.conky_start
