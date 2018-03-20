import datetime
from datetime import timedelta
import zipfile
import sys
import pandas as pd
from pathlib import Path
import os
import numpy as np

class ProcessBhavCopy:
	def __init__(self, startDate):
		self.startDate = startDate
	
	def getNextDate(self, prevDate):
		if prevDate is None:
			startDate = datetime.datetime.strptime('010110', "%d%m%y").date()
			return startDate.strftime("%d%m%y")
		else:
			nextDate = prevDate + timedelta(days = 1)
			return nextDate.strftime("%d%m%y")

	def extractcsv(self, filePath, fileDate):
		try:
			archive = zipfile.ZipFile(filePath)
			if archive is None:
				print("File not found for date: "+ fileDate)
			else:	
				for file in archive.namelist():
					if file.startswith('Pd'+fileDate):
						archive.extract(file,'./Data/csvfiles')
		except FileNotFoundError:
			print("Could not find file for date: "+ fileDate)
	
	def extractstockframes(self, filePath, fileDate):
		print("Extracting stock frames from file: "+ filePath)
		columns = ['Date','Open','High','Low','Close','Volume','AdjustedClose','OC','return','returnLag1','returnLag2','returnLag3','returnLag4','returnLag5','direction']
		try:
			if self.fileExists(filePath):
				pdfile = pd.read_csv(filePath)
				for index,row in pdfile.iterrows():
					if row['SERIES'] == 'EQ':
						if self.fileExists('./Data/processed/'+row['SYMBOL']+'.csv'):
							stockframe = pd.read_csv('./Data/processed/'+row['SYMBOL']+'.csv',names=columns)
							data = [[datetime.datetime.strptime(fileDate,'%d%m%y').date(),row['OPEN_PRICE'],row['HIGH_PRICE'],row['LOW_PRICE'],row['CLOSE_PRICE'],row['NET_TRDQTY'],row['CLOSE_PRICE'],np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan]]
							tempframe = pd.DataFrame(data,columns=columns)
							stockframe = stockframe.append(tempframe)
							stockframe.to_csv('./Data/processed/'+row['SYMBOL']+'.csv',index=False,header=False)
						else:
							data = [[str(datetime.datetime.strptime(fileDate,'%d%m%y').date()),row['OPEN_PRICE'],row['HIGH_PRICE'],row['LOW_PRICE'],row['CLOSE_PRICE'],row['NET_TRDQTY'],row['CLOSE_PRICE'],np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan]]
							newStockFrame = pd.DataFrame(data, columns=columns)
							newStockFrame.to_csv('./Data/processed/'+row['SYMBOL']+'.csv',index=False, header=True)
		except FileNotFoundError:
			print("File not found at path: "+ basedir + filePath)	

	def extractAll(self):
		nextDate = self.getNextDate(None)
		nextDateDate = datetime.datetime.strptime(nextDate, '%d%m%y').date()
		while nextDateDate <= datetime.date.today():
			print("Processing for date: "+ nextDate)	
			self.extractcsv('./Data/zipfiles/'+nextDate+'.zip',nextDate)
			self.extractstockframes('./Data/csvfiles/Pd'+nextDate+'.csv',nextDate)
			nextDate = self.getNextDate(nextDateDate)
			nextDateDate = datetime.datetime.strptime(nextDate, '%d%m%y').date()

	def fromYear(self):
		if int(self.startDate) < 2010:
			print("Bhav copy for year before 2010 not available")
		else:
			startYear = self.startDate[2:]
			nextDate = '0101'+startYear
			nextDateDate = datetime.datetime.strptime(nextDate, '%d%m%y').date()
			while nextDateDate <= datetime.date.today():
				print("Processing for date: "+nextDate)
				self.extractcsv('./Data/zipfiles/'+nextDate+'.zip', nextDate)
				self.extractstockframes('./Data/csvfiles/Pd'+nextDate+'.csv',nextDate)
				nextDate = self.getNextDate(nextDateDate)
				nextDateDate = datetime.datetime.strptime(nextDate, '%d%m%y').date()

	def fromDate(self):
		inputDate = datetime.datetime.strptime(self.startDate, '%d%m%y').date()
		if inputDate > datetime.date.today():
			print('Input date cannot be greater than todays date.')
		else:
			nextDate = self.startDate
			nextDateDate = datetime.datetime.strptime(self.startDate, '%d%m%y').date()
			while nextDateDate <= datetime.date.today():
				print("Processing for date: "+nextDate)
				self.extractcsv('./Data/zipfiles/'+nextDate+'.zip',nextDate)
				self.extractstockframes('./Data/csvfiles/Pd'+nextDate+'.csv',nextDate)
				nextDate = self.getNextDate(nextDateDate)
				nextDateDate = datetime.datetime.strptime(nextDate, '%d%m%y').date()
	
	def fileExists(self,filePath):
		try:
			f = open(filePath)
			f.close()
		except:
			return False
		return True	
		

def main(args):
	if args[0] == "-extractAll":
		obj = ProcessBhavCopy(None)
		obj.extractAll()
	elif args[0] == "-fromYear":
		if len(args) < 2:
			print("Please input start year in yyyy format")
		else:
			obj = ProcessBhavCopy(args[1])
			obj.fromYear()
	elif args[0] == "-fromDate":
		if len(args) < 2:
			print("Please input start date in ddmmyy format.")
		else:
			obj = ProcessBhavCopy(args[1])
			obj.fromDate()

if __name__ == "__main__":
	main(sys.argv[1:])
