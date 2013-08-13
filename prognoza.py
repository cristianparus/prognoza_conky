#/usr/bin/python

import xml.etree.ElementTree as ET
from datetime import datetime

def datum(dat):
	t = dat.rsplit("-")
	return (t[2] + "." + t[1])

class dan:
	def __init__(self):
		self.temp = list()
		self.termin = list()
		self.symbol = list()
		self.datum = ""

	def ispis(self):
		termin = ""
		temp = ""
		symbol = ""

		goto = 0

		for i in range(0,len(self.temp)):
			termin += "${goto %d}%s " %(goto,self.termin[i][11:-3])
			temp += "${goto %d}%s ${iconv_start UTF-8 ISO_8859-1}°${iconv_stop}C" %(goto,self.temp[i])
			symbol += "${goto %d}%s " %(goto,self.symbol[i])
			goto+=100

		print (termin + "\n" + temp + "\n" + symbol + "\n")


today = str(datetime.today())
today_date = today[:10]
today_time = today[11:16]

tree = ET.parse('/mnt/data/projekti/prognoza/forecast_hour_by_hour.xml')
root = tree.getroot()

sun = root.find("sun");
forecast = root.find("forecast")
tabular = forecast.find("tabular")

time = list(tabular.iter("time"))

counter = 0
t_danas = time[0].attrib["from"][:10]

danas = dan()
sutra = dan()
prekosutra = dan()

for i in time:
	t_from = i.attrib["from"]

	tem = i.find("temperature")
	t_temp = tem.attrib["value"]

	sym = i.find("symbol")
	t_sym = sym.attrib["name"]
	
	if t_from[:10] != t_danas:
		t_danas = t_from[:10]
		counter +=1

	if counter == 1:

		sutra.temp.append(t_temp)
		sutra.termin.append(t_from)
		sutra.symbol.append(t_sym)
		sutra.dan = datum(t_from[0:10])

	elif counter == 2:
		prekosutra.temp.append(t_temp)
		prekosutra.termin.append(t_from)
		prekosutra.symbol.append(t_sym)
		prekosutra.dan = datum(t_from[0:10])


	else:
		danas.temp.append(t_temp)
		danas.termin.append(t_from)
		danas.symbol.append(t_sym)
		danas.dan = datum(t_from[0:10])

print ("Izlazak sunca: " + sun.attrib["rise"][11:-3] + "\nZalazak sunca: " + sun.attrib["set"][11:-3] + "\n")
print ("\n${color green}Danas " + danas.dan + "${color}\n")
danas.ispis()
print ("\n${color green}Sutra " + sutra.dan + "${color}\n")

sutra.ispis()
print ("\n${color green}Prekosutra " + prekosutra.dan + "${color}\n")

prekosutra.ispis()