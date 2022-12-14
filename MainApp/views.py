from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import pandas as pd
from pathlib import Path
import os
from django.core.files.storage import FileSystemStorage
import json
import numpy as np

# Create your views here.
def upload_csv(request):
	data = {}
	if "GET" == request.method:
		return render(request, "upload_csv.html", data)
    # if not GET, then proceed
	if "POST" == request.method:
		#try:
			print('inside post')
			csv_file = request.FILES["csv_file"]
			time = request.POST.get('time')
			print(time)
			print(csv_file)
			#save csv file in system
			fs = FileSystemStorage()
			filename = fs.save(csv_file.name, csv_file)
			deletefilrurl=fs.path(filename)
			#read csv file
			df = pd.read_csv(deletefilrurl)
			print(df)
			#creating attribute on time frame
			id = df['BANKNIFTY'][0]
			open=df['OPEN'][0]
			date=df['DATE'][0]
			close=df['CLOSE'][int(time)-1]
			high = (df['HIGH'][0])
			low = (df['LOW'][0])
			for i in range(1,int(time)):
				if high < (df['HIGH'][i]):
					high = (df['HIGH'][i])
				if low > (df['LOW'][i]):
					low = (df['LOW'][i])
			
			candle = {'ID':str(id),'OPEN':str(open),'HIGH':str(high),'LOW':str(low),'CLOSE':str(close),'date':str(date)}
			print(candle)
			json_object = json.dumps(candle, indent=4, default=str)
			print(json_object)
			# with open("sample.txt", "w") as outfile:
			# 	outfile.write(json_object)
	return render(request, "upload_csv.html", data)
