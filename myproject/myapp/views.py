from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework import status
from .models import employees
from . serializers import employeesSerializer
import json

def doPrediction(Hometeam,Awayteam):
	a = loadFile(Hometeam,Awayteam)
	print("-------",a)
	result = loadModel(a)
	return result

def loadFile(Hometeam,Awayteam):
	import pandas as pd
	data= pd.read_csv('C:/Users/Bimesh/restFramework/myproject/final_dataset1.csv')
	ht= Hometeam
	at= Awayteam
	hm= data["HomeTeam"]
	hp= 0
	for i in hm:
		if i == ht:
			hp = hp + 1
	am= data["AwayTeam"]
	ap= 0
	for i in am:
		if i == at:
			ap = ap + 1
	
	a= (data[data["HomeTeam"] == ht].sum().HTP)/hp
	b= (data[data["AwayTeam"] == at].sum().ATP)/ap
	c= (data[data["HomeTeam"] == ht].sum().HomeTeamLP)/hp
	d= (data[data["AwayTeam"] == at].sum().AwayTeamLP)/ap
	e= (data[data["HomeTeam"] == ht].sum().HTFormPts)/hp
	f= (data[data["AwayTeam"] == at].sum().ATFormPts)/ap
	g= (data[data["HomeTeam"] == ht].sum().HTGD)/hp
	h= (data[data["AwayTeam"] == at].sum().ATGD)/ap
	feature =[a],[b],[c],[d],[e],[f],[g],[h]	
	return feature


def loadModel(p):
	import pandas as pd
	import pickle
	try:
		predictor = pickle.load(open('C:/Users/Bimesh/restFramework/myproject/xgbPredictionModel.sav','rb'))
	except:
		print("File is not loaded")
	print(p[0])
	d = {'HTP': p[0],'ATP': p[1],'HomeTeamLP': p[2],'AwayTeamLP': p[3],'HTFormPts': p[4],'ATFormPts': p[5], 'HTGD': p[6],'ATGD': p[7]}
	df = pd.DataFrame(data=d)
	print(df)
	result= predictor.predict(df)
	print(result)
	return result

class employeeList(APIView):

	def get(self,request):
		employees1= employees.objects.all()
		serializer= employeesSerializer(employees1, many=True)
		return Response(serializer.data)

	
	def post(self):
		pass

class helloWorld(APIView):
		
	def get(self,request):
		message= {'data': 'Hello World'} 
		return Response(message)

	
	def post(self, request):
		message= request.data
		yolo = json.dumps(message, indent=4)
		print(yolo)
		yolo = json.loads(yolo)
		ht= message.get('team1')
		at= message.get('team2')
		print(ht,at)
		b= doPrediction(ht,at)
		return Response(b)
	
	

