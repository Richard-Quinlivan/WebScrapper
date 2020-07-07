from bs4 import BeautifulSoup
import requests
import csv
import time

userAgents = [
{"user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15"},
{"user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.14 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15"},
{"user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.14 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15"},
{"user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.13 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.14"},
{"user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.14 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.14"},
{"user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.14 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.13"},
{"user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"},
{"user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.35 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"},
{"user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.34 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"},
{"user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.35"},
{"user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.35 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.35"},
{"user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.34 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.35"}
]
# ip = [{"https" : "45.229.193.109"}, {"https" : "122.54.27.147"}, {"https" : "75.109.249.111"}]
fileName = "companies.csv"

def write_to_csv(manager, row):
	if manager is not None:
		manager = str(manager).split("<span>")[1].split("</span>")[0]
	with open (fileName.split('.')[0] + "(managers)" + ".csv", 'a') as csvFile:
		writeCSV = csv.writer(csvFile, delimiter=',')
		writeCSV.writerow(row + [manager])

def main():
	i = 0
	with open(fileName, 'r') as csvFile:
		readCSV = csv.reader(csvFile, delimiter=',')
		for row in readCSV:
			i+=1
			with requests.Session() as session:
				URL1 = "https://www.bbb.org/search?find_country=USA&find_loc=" + row[1] + "%2C%20"+ row[2] + "&find_text=" + (row[0]).lower() + "&page=1"
				header = userAgents[i % len(userAgents)]
				# proxy = ip[i % len(ip)]
				connection = True # if the connection failes, this boolean tell the code to retry with the next ip address
				checkBool = True	#if the company is not present this boolean will tell the code to skip this entry
				while connection:
					try:
						searchGet1 = session.get(URL1, headers=header)
						soup = BeautifulSoup(searchGet1.content, "html.parser")
						check = soup.find("a", class_="Name__Link-sc-1srnbh5-1 gNkQmF")#makes sure the company exists on BBB.org
						if check == None:
							write_to_csv(None, row)
							time.sleep(5)
							checkBool = False
							break
						URL2 = check["href"]
						searchGet2 = session.get(URL2, headers=header)
						soup = BeautifulSoup(searchGet2.content, "html.parser")
						manager = soup.find("li", class_="styles__LI-fb5jhx-5 ePmlcI")
						write_to_csv(manager, row)
						connection = False
					except:
						i+=1
				if not checkBool:
					continue
			time.sleep(5)
main()

