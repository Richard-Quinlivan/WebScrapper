from bs4 import BeautifulSoup
import requests
import csv

fileName = "companies.csv"
with open(fileName, 'r') as csvFile:
	readCSV = csv.reader(csvFile, delimiter=',')
	for row in readCSV:
		with requests.Session() as session:
			manager = ""
			URL1 = "https://www.bbb.org/search?find_country=USA&find_loc=" + row[1] + "%2C%20"+ row[2] + "&find_text=" + (row[0]).lower() + "&page=1"
			header = {"user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"}
			searchGet1 = session.get(URL1, headers=header)
			soup = BeautifulSoup(searchGet1.content, "html.parser")

			URL2 = soup.find("a", class_="Name__Link-sc-1srnbh5-1 gNkQmF")["href"]
			searchGet2 = session.get(URL2, headers=header)
			soup = BeautifulSoup(searchGet2.content, "html.parser")
			name = soup.find("li", class_="styles__LI-fb5jhx-5 ePmlcI")
			if name is not None:
				manager = str(name).split("<span>")[1].split("</span>")[0]
			with open (fileName + "(managers)", 'a') as csvFile:
				writeCSV = csv.writer(csvFile, delimiter=',')
				writeCSV.writerow(row + [manager])
