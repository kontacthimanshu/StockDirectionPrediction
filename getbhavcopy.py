import urllib.request
import ssl
import datetime
from datetime import timedelta
import sys

class GetBhavCopy:
	def __init__(self, startYear):
		self.startYear = startYear
	
	def getNextDate(self, prevDate):
		if prevDate is None:
			startDate = datetime.datetime.strptime('010110',"%d%m%y").date()
			return startDate.strftime("%d%m%y")
		else:
			nextDate = prevDate + timedelta(days = 1)
			return nextDate.strftime("%d%m%y")

	def getAll(self):
		nextDate = self.getNextDate(None)
		nextDateDate = datetime.datetime.strptime(nextDate,'%d%m%y').date()
		while nextDateDate <= datetime.date.today():
			fileurl = self.getFileUrl(nextDate)
			filePath = self.getFilePath(nextDate)
			if self.fileExists(filePath) == False:
				print('Downloading file: '+ filePath)	
				self.downloadFile(fileurl,nextDate)
			else:
				print('File already downloaded:'+filePath)
			nextDate = self.getNextDate(nextDateDate)
			nextDateDate = datetime.datetime.strptime(nextDate,'%d%m%y').date()
	
	def fromYear(self):
		if int(self.startYear) < 2010:
			print("Bhav copy for year before 2010 not available.")
		else:
			startYear = self.startYear[2:]
			nextDate = '0101'+startYear
			nextDateDate = datetime.datetime.strptime(nextDate, '%d%m%y').date()
			while nextDateDate <= datetime.date.today():
				fileUrl = self.getFileUrl(nextDate)
				filePath = self.getFilePath(nextDate)
				if self.fileExists(filePath) == False:
					print('Downloading file: '+ filePath)	
					self.downloadFile(fileUrl, nextDate)
				else:
					print('File already downloaded: '+filePath)
				nextDate = self.getNextDate(nextDateDate)
				nextDateDate = datetime.datetime.strptime(nextDate,'%d%m%y').date()
	
	def fromDate(self):
		inputDate = datetime.datetime.strptime(self.startYear,'%d%m%y').date()
		if inputDate > datetime.date.today():
			print('Input date cannot be greater than todays date.')
		else:
			nextDate = self.startYear
			nextDateDate = datetime.datetime.strptime(self.startYear,'%d%m%y').date()
			while nextDateDate <= datetime.date.today():
				fileUrl = self.getFileUrl(nextDate)
				filePath = self.getFilePath(nextDate)
				if self.fileExists(filePath) == False:
					print('Downloading file: '+ filePath)
					self.downloadFile(fileUrl, nextDate)
				else:
					print('File already downloaded'+filePath)
				nextDate = self.getNextDate(nextDateDate)
				nextDateDate = datetime.datetime.strptime(nextDate, '%d%m%y').date()		
			
	def getFileUrl(self, fileDate):
		fileUrl = "https://www.nseindia.com/archives/equities/bhavcopy/pr/PR"+fileDate+".zip"
		return fileUrl
	
	def getFilePath(self, fileDate):
		filePath = "./Data/zipfiles/"+fileDate+".zip"
		return filePath

	def downloadFile(self, fileUrl, fileDate):
		try:	
			user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
			headers = {'User-Agent': user_agent}
			context = ssl._create_unverified_context()
			req = urllib.request.Request(fileUrl,None,headers)
			response = urllib.request.urlopen(req,context=context)
			if response.status == 200:
				data = response.read()
				if data:	
					file = open("./Data/zipfiles/"+fileDate+".zip","wb")
					file.write(data)
					file.close()
			else:
				print("Could not get file for date " +fileDate)
		except BaseException:
			print("Could not download file with url" + fileUrl)
		finally:
			print("Going to try next file")
	
	def fileExists(self,filePath):
		try:
			f = open(filePath)
			f.close()
		except:
			return False
		return True

def main(args):
	if args[0] == "-getAll":
		obj = GetBhavCopy(None)
		obj.getAll()
	elif args[0] == "-fromYear":
		if len(args) < 2:
			print("Please input start year in yyyy format.")
		else:
			obj = GetBhavCopy(args[1])
			obj.fromYear()
	elif args[0] == "-fromDate":
		if len(args) < 2:
			print("Please input start date in ddmmyy format.")
		else:
			obj = GetBhavCopy(args[1])
			obj.fromDate()	
	
if __name__ == "__main__":
	main(sys.argv[1:])			 
