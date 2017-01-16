import re
import math
import datetime
from pysolar.solar import datetime

def dayOfYear(year,month,day):
	format = '%Y.%m.%d'
	s = year + '.' + month + '.' + day
	dt = datetime.datetime.strptime(s,format)
	tt = dt.timetuple()
	return tt.tm_yday

def dayLight(latitude, year, month, day):
	L = float(latitude)
	J = float(dayOfYear(year, month, day))
	P = math.asin(0.39795 * math.cos(0.2163108 + 2 * math.atan(0.9671396 * math.tan(0.00860 * (J - 186)))))
	D = 24.0 - (24.0/math.pi) * math.acos((math.sin(0.8333 * math.pi/180) + math.sin(L * math.pi/180) * math.sin(P))/(math.cos(L * math.pi/180) * math.cos(P)))
	return round(D,2)

def CalculateET(latitude,longitude,elevation,year,month,day,Tmax,Tmin,RH,WindSpeed,SR,Precip):
	avgtemp = (Tmax + Tmin)/2

	# Calculate the daylight
	sunshine = dayLight(latitude, year, month, day)

	p = 101.3 * math.pow(((293 - 0.0065 * elevation)/293),5.26)
	Delta = 4098 * (0.6108 * math.exp(17.27 * avgtemp/(avgtemp + 237.3)))/math.pow((avgtemp + 237.3),2)
	r = 1.013 * 0.001 * p/(0.622 * 2.45)

	e_0_Tmax = 0.6108 * math.exp(17.27 * Tmax /(Tmax + 237.3))
	e_0_Tmin = 0.6108 * math.exp(17.27 * Tmin /(Tmin + 237.3))
	es = (e_0_Tmax + e_0_Tmin) / 2;
	ea = RH * 0.01 * ((e_0_Tmax + e_0_Tmin)/2)

	#Calculate the number of the days of a year
	numDayofYear = dayOfYear(year,month,day)

	# Constant numbers, no idea how James set this numbers -----------------------------
	Gsc = 0.082 #Gsc=0.082 MJm-2min-1
	G = 0 # The day or ten-days soi heat flux
	# ----------------------------------------------------------------------------------

	Rs = SR # Solar radiation mj/m2

	dr = 1 + 0.033 * math.cos(2 * math.pi * numDayofYear/365)
	phi = math.pi * (latitude)/180 # convert to radian
	sDelta = 0.409 * math.sin(2 * math.pi * numDayofYear/365 - 1.39)
	ws = math.acos(-math.tan(phi) * math.tan(sDelta))
	Ra = 24 * 60 * Gsc * dr * (ws * math.sin(phi) * math.sin(sDelta) + math.cos(phi) * math.cos(sDelta) * math.sin(ws))/math.pi
	N = 24 * ws/math.pi
	Rso = (0.75 + 2 * 0.00001 * elevation) * Ra
	Tmax_k = Tmax + 273.16 # Convert celsius to kelvin
	Tmin_k = Tmin + 273.16 # Convert celsius to kelvin
	Rns = (1-0.23) * Rs
	Rnl = 4.903 * math.pow(0.1,9) * ((math.pow(Tmax_k,4) + math.pow(Tmin_k,4))/2) * (0.34 - 0.14 * math.pow(ea,0.5)) * (1.35 * Rs/Rso - 0.35)
	Rn = Rns - Rnl

	a = 0.408 * (Rn - G) * Delta/(Delta + r * (1 + 0.34 * WindSpeed))

	b = (r/(Delta + r * (1 + 0.34 * WindSpeed))) * (900 * WindSpeed / (avgtemp + 273)) * (es - ea)
	# The grass reference evapotranspriration is 1.35 mm day-1
	ET=(a + b)*1.3
	 # ET = (a + b)
	return round(ET,3)

def main():
	print ("This program only runs text file with the defined format.\n")
	# Aks user to enter the input file
	inStream = input("Please enter the iput file: ")
	try:
		# Read the text file and store the variables
		inputFile = open(inStream , "r")
		a = inStream.split(".")
		outStream = a[0] + "_ET_result.txt"
		outputFile = open(outStream , "w")
		with inputFile as f:
			content = f.readlines()
			coordinate = re.findall(r"[-+]?\d*\.\d+|\d+", content[0])
			lat = float(coordinate[0])
			lon = float(coordinate[1])
			ele = float(coordinate[2])
			for i in range(3,len(content)):
				values = re.findall(r"[-+]?\d*\.\d+|\d+", content[i])
				month = values[0]
				day = values[1]
				year = values[2]
				Tmax = float(values[4])
				Tmin = float(values[5])
				RH = float(values[6]) # Relative Humidity
				WS = float(values[8]) # Wind Speed
				SR = float(values[9]) # Solar Radiation
				Precip = values[10] # Precipitation
				ET = float(values[11]) # Evapotranspriration from hprcc
				calcET = CalculateET(lat,lon,ele,year,month,day,Tmax,Tmin,RH,WS,SR,Precip)
				error = round((abs(ET-calcET)/(ET+calcET)/2)*100, 2)
				outputFile.write("Date: " + month + "/" + day + "/" + year + "\t ET from calculation: " + str(calcET) + "\tET from hprcc: " + str(ET) + "\tError: " + str(error) + '%\n')

		print ("The results is generated in "), outStream
		inputFile.close()
		outputFile.close()
	except:
		inputFileName = '"' + inStream + '"'
		print ("Sorry the file") , inputFileName , "is not in this directory or the file name is wrong.\nRun the program with the correct input file."


if __name__ == "__main__": main()
