from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework import status
import json

def doPrediction(Hometeam,Awayteam):
	a = loadFile(Hometeam,Awayteam)
	result = loadModel(a)
	return result

def loadFile(Hometeam,Awayteam):
	import pandas as pd
	df2= pd.read_csv('C:/Users/Bimesh/restFramework/myproject/FootballDataset.csv')
	ht= Hometeam
	at= Awayteam
	homeData = df2["HomeTeam"]
	homePlayed = 0
	for i in homeData:
		if i == ht:
			homePlayed= homePlayed + 1

	awayData = df2["AwayTeam"]
	awayPlayed = 0
	for i in awayData:
		if i == at:
			awayPlayed= awayPlayed + 1
	
	HS= (df2[df2["HomeTeam"] == ht].sum().HS)/homePlayed
	AS= (df2[df2["AwayTeam"] == at].sum().AS)/awayPlayed
	HST= (df2[df2["HomeTeam"] == ht].sum().HST)/homePlayed
	AST= (df2[df2["AwayTeam"] == at].sum().AST)/awayPlayed
	HC= (df2[df2["HomeTeam"] == ht].sum().HC)/homePlayed
	AC= (df2[df2["AwayTeam"] == at].sum().AC)/awayPlayed
	HF= (df2[df2["HomeTeam"] == ht].sum().HF)/homePlayed
	AF= (df2[df2["AwayTeam"] == at].sum().AF)/awayPlayed
	feature =[HS],[AS],[HST],[AST],[HC],[AC],[HF],[AF]	
	return feature


def loadModel(p):
	import pandas as pd
	import pickle
	try:
		predictor = pickle.load(open('C:/Users/Bimesh/restFramework/myproject/decisionTreeModel.sav','rb'))
	except:
		print("File is not loaded")
	d = {'HS': p[0],'AS': p[1],'HST': p[2],'AST': p[3],'HC': p[4],'AC': p[5], 'HF': p[6],'AF': p[7]}
	df = pd.DataFrame(data=d)
	print(df)
	result= predictor.predict(df)
	print(result)
	return result


class makePrediction(APIView):
		
	def get(self,request):
		message= {'You can make prediction by posting two team values.'} 
		return Response(message)

	
	def post(self, request):
		message= request.data
		ht= message.get('team1')
		at= message.get('team2')
		print(ht,at)
		b= doPrediction(ht,at)
		return Response(b)
	
	

