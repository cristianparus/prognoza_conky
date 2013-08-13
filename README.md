prognoza_conky
==============

Small script which take and parse XML file from yr.no

This script is using weather data from yr.no website.

First, XML is downloaded with wget and it's saved in destinated folder. Provided XML is filled with weather data for 3 days and if you want to change town, go on yr.no site, find your city and click on forecast hour by hour link. After that, you have add "forecast_hour_by_hour.xml" to your URL.
Wanted URL must be placed in update.sh file.

After that, python script is retrieving data from XML and generating text which will be added in conky config file.

In conky_template, you can change view of your conky (not in conky.conf because that file is rewriting on every update).

On the end, if you want automatic update, use cron. Here is example which I'm using to update XML every 5 hours. 

00 */5 * * * sh /mnt/data/projekti/prognoza/update.sh


Notice:

yr.no policy says that if you are using yr.no XML feed, you have to write that on your gadget but only if you are implementing that on your webiste. I don't write that message for obvious reason, but if someone think that is neccesary, please inform me so I can change.
Also, policy says that nobody shouldn't download XML too much because they want to have a good bandwith. If you want any more information, read yr.no policy.



Contact:

if you find some bug, or want to suggest some design, wrote me an email on ante[at]ante003.com