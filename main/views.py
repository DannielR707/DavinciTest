from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
import csv
import os
from main.models import ClientsInfo, Campaign, Temp, TableColumns
from main.forms import DocumentForm

def home(request):
	
	campaigns = Campaign.objects.all()

	return render(request, 'main/home.html', { 'campaigns': campaigns })

def createCampaign(request):
	
	new_campaign = Campaign(name=request.POST['name'])
	new_campaign.save()

	campaigns = Campaign.objects.all()

	return render(request, 'main/home.html', { 'campaigns': campaigns })

def deleteCampaign(request, campaign_id):
	
	campaign = Campaign.objects.get(pk=campaign_id)	
	campaign.delete()

	campaigns = Campaign.objects.all()

	return render(request, 'main/home.html', { 'campaigns': campaigns })

def detailCampaign(request, campaign_id):

	campaign = Campaign.objects.get(pk=campaign_id)
	clientsInfo = ClientsInfo.objects.filter(campaign=campaign).order_by('id')
	tableColumns = TableColumns.objects.order_by('id')

	return render(request, "main/model_form_upload.html", {'campaign' : campaign, 'clientsInfo' : clientsInfo})


def checkFileColumns(request, campaign_id):

	campaign = Campaign.objects.get(pk=campaign_id)	
	clientsInfo = ClientsInfo.objects.filter(campaign=campaign).order_by('id')
	table_columns = TableColumns.objects.order_by('id')
	
	csv_file = request.FILES["csv_file"]	
	file_data = csv_file.read().decode("utf-8").strip()	
	lines = file_data.split("\n")

	i = 0
	rows = []
	while i < 5:
		rows.append(lines[i].split(";"))		
		i += 1

	file_length = len(lines)
	total_columns = len(rows[0])

	document = Temp(name=csv_file.name, URL=csv_file, campaign=campaign)
	document.save()
	
	return render(request, 'main/model_form_upload.html', { 'file_length': file_length, 'document_id' : document.id,
         'total_columns' : total_columns, 'campaign' : campaign, 'rows' : rows, 'clientsInfo' : clientsInfo, 'table_columns' : table_columns
    })

def model_form_upload(request, campaign_id):

	campaign = Campaign.objects.get(pk=campaign_id)	
	clientsInfo = ClientsInfo.objects.filter(campaign=campaign).order_by('id')
	
	document_id = request.POST.get('document_id')	
	total_columns = int(request.POST.get('total_columns'))
	document = Temp.objects.get(pk=document_id)	
	
	file_data = document.URL.read().decode("utf-8").strip()	
	lines = file_data.split("\n")
	
	#loop over the lines and save them in db. If error , store as string and then display
	for line in lines:
		data_dict = {}		
		fields = line.split(";")		
		i=0
		while i <= total_columns:
			
			value = request.POST.getlist('table_columns'+str(i))
			if value:
				
				if int(value[0]) == 1:					
					data_dict["name"] = fields[i]	
				if int(value[0]) == 2:
					data_dict["lastName"] = fields[i]	
				if int(value[0]) == 3:
					data_dict["phoneNumber"] = fields[i]	
				if int(value[0]) == 4:
					data_dict["address"] = fields[i]	
			
			i += 1
	
		if data_dict:	
			data_dict["campaign"] = campaign.id
		
		try:
			form = DocumentForm(data_dict)
			if form.is_valid():
				form.save()					
			else:
				logging.getLogger("error_logger").error(form.errors.as_json())												
		except Exception as e:
			logging.getLogger("error_logger").error(repr(e))					
			pass

	clientsInfo = ClientsInfo.objects.filter(campaign=campaign).order_by('id')
	
	document.delete()

	return render(request, 'main/model_form_upload.html', {'document_id' : document_id,
         'campaign' : campaign, 'clientsInfo' : clientsInfo
    })

def deleteInfo(request, info_id):
		
	client_info = ClientsInfo.objects.get(pk=info_id)	
	client_info.delete()

	campaign = Campaign.objects.get(pk=client_info.campaign.id)	
	clientsInfo = ClientsInfo.objects.filter(campaign=campaign).order_by('id')

	return render(request, 'main/model_form_upload.html', { 'campaign' : campaign, 'clientsInfo': clientsInfo })  

def deleteAllInfo(request, campaign_id):

	clients_info = ClientsInfo.objects.filter(campaign__id=campaign_id)
	clients_info.delete()

	campaign = Campaign.objects.get(pk=campaign_id)	

	return render(request, 'main/model_form_upload.html', { 'campaign' : campaign, })  
