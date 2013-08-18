#/usr/bin/python

import xml.etree.ElementTree as ET
from datetime import datetime
import os



def izbrisi_staro():
	os.chdir('/mnt/data/projekti/prognoza/')
	os.remove('forecast_hour_by_hour.xml')
	os.system('wget http://www.yr.no/place/Croatia/Grad_Zagreb/Zagreb/forecast_hour_by_hour.xml')
	os.system('cp conky_template conky.conf')



def datum(dat):
	t = dat.rsplit("-")
	return (t[2] + "." + t[1])

class dan:
	def __init__(self):
		self.temp = list()
		self.termin = list()
		self.symbol = list()
		self.dan = ""

	def ispis_hor(self,config):
		termin = ""
		temp = ""
		symbol = ""

		goto = 0

		for i in range(0,len(self.temp)):
			termin += "${goto %d}%s " %(goto,self.termin[i][11:-3])
			temp += "${goto %d}%s" %(goto,self.temp[i])
			symbol += "${goto %d}%s " %(goto,self.symbol[i])
			goto+=100

		config.write (termin + "\n" + temp + "\n" + symbol + "\n")


	def ispis_ver(self,sutra,prekosutra,config):
		termin = ""
		temp = ""
		symbol = ""

		t1 = [len(self.temp), len(sutra.temp),len(prekosutra.temp)]

		maks = max(t1)

		for i in range(0,maks):

			if len(self.termin) <= i:
				self.termin.append("")
				self.temp.append("")
				self.symbol.append("")

			if len(sutra.termin) <= i:
				sutra.termin.append("")
				sutra.temp.append("")
				sutra.symbol.append("")

			if len(prekosutra.termin) <= i:
				prekosutra.termin.append("")
				prekosutra.temp.append("")
				prekosutra.symbol.append("")



			config.write ("${goto 0}${color red}%s${color} ${goto 100}${color red}%s${color} ${goto 200}${color red}%s${color} " % (self.termin[i][11:-3],sutra.termin[i][11:-3],prekosutra.termin[i][11:-3]))
			config.write ("${goto 0}%s ${goto 100}%s ${goto 200}%s" % (self.temp[i],sutra.temp[i],prekosutra.temp[i]))
			config.write ("${goto 0}%s ${goto 100}%s ${goto 200}%s" % (self.symbol[i],sutra.symbol[i],prekosutra.symbol[i]))
		
			config.write ("\n")



izbrisi_staro()
config = open('conky.conf','a')

ispis = "hor"
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

		sutra.temp.append(t_temp + "${iconv_start UTF-8 ISO_8859-1}°${iconv_stop}C")
		sutra.termin.append(t_from)
		sutra.symbol.append(t_sym)
		sutra.dan = datum(t_from[0:10])

	elif counter == 2:
		prekosutra.temp.append(t_temp + "${iconv_start UTF-8 ISO_8859-1}°${iconv_stop}C")
		prekosutra.termin.append(t_from)
		prekosutra.symbol.append(t_sym)
		prekosutra.dan = datum(t_from[0:10])


	else:
		danas.temp.append(t_temp + "${iconv_start UTF-8 ISO_8859-1}°${iconv_stop}C")
		danas.termin.append(t_from)
		danas.symbol.append(t_sym)
		danas.dan = datum(t_from[0:10])


config.write ("Zadnji update: " + today_time + "\n")
config.write ("Izlazak sunca: " + sun.attrib["rise"][11:-3] + "\tZalazak sunca: " + sun.attrib["set"][11:-3] + "\n")
	
if ispis == "hor":

	config.write ("\n${color green}Danas " + danas.dan + "${color}\n")
	danas.ispis_hor(config)
	config.write ("\n${color green}Sutra " + sutra.dan + "${color}\n")

	sutra.ispis_hor(config)
	config.write ("\n${color green}Prekosutra " + prekosutra.dan + "${color}\n")

	prekosutra.ispis_hor(config)

else:
	prvi_red = "${color green}Danas " + danas.dan + "${color}${goto 100}"
	prvi_red += "${color green}Sutra " + sutra.dan + "${color}${goto 200}"
	prvi_red += "${color green}Prekosutra " + prekosutra.dan + "${color}${goto 300}"

	config.write (prvi_red + "\n")
	danas.ispis_ver(sutra,prekosutra,config)

config.close()
os.system('killall conky')
os.system('conky -c conky.conf &')
os.system('conky &')