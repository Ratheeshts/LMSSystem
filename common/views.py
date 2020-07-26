from django.shortcuts import render
import datetime
import itertools  
import os,pandas as pd
import numpy as np
import string
from sklearn.cluster import KMeans
from learner.models import Learner,LearningMaterial,Learning_Style,Session_Log,Learning_Session
from django.shortcuts import render
from django.apps import apps
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
from django.forms import Form
from django.core.paginator import Paginator
from LMSSystem import settings
from django.http import HttpResponse
import urllib.request
try:
    from io import BytesIO as IO # for modern python
except ImportError:
    from io import StringIO as IO # for legacy python

# Create your views here.

"""
This method input image files in user post request and upload files to directory
"""
def upload_file(request):
	myform = Form(request.POST, request.FILES)
	# create unique file name based on time
	uniq_filename = str(datetime.datetime.now().date()) + '_' \
					+ str(datetime.datetime.now().time()).replace(':', '.')
	file_name = 'img' + uniq_filename + '.png'
	file = myform.files['croppedImage']
	#  Saving POST'ed file to storage
	file_name = default_storage.save(file_name, file)
	data = {}
	data['file_name'] = file_name
	return JsonResponse(data)

# do recommandation


# find the simlar learners of current user
# find the all books under selected topic suggested by simler learners, sorted by avg of given rating
# recomand [5]


def file_to_dataframe(filename, **kwargs):

	"""Read file with **kwargs; files supported: xls, xlsx, csv, csv.gz, pkl"""

	read_map = {'xls': pd.read_excel, 'xlsx': pd.read_excel, 'csv': pd.read_csv,
				'gz': pd.read_csv, 'pkl': pd.read_pickle}
	ext = os.path.splitext(filename)[1].lower()[1:]
	assert ext in read_map, "Input file not in correct format, must be xls, xlsx, csv, csv.gz, pkl; current format '{0}'".format(ext)
	assert os.path.isfile(filename), "File Not Found Exception '{0}'.".format(filename)
	return read_map[ext](filename, **kwargs)


def excel_to_lmodel(file_path,app_name,model_name):
	excel_df=file_to_dataframe(file_path)
	df_records = excel_df.to_dict('records')
	#locate requested model class, apps.all_models is dictionary which hold all model classes 
	model_class=apps.all_models[app_name][model_name] 
	#itreate over the records (every row as dictionory) and create model instances
	model_instances = [model_publish(model_class(),**record) for record in df_records]
	model_class.objects.bulk_create(model_instances)
	return True
"""
This method is to import product_part model from excel file

"""
def excel_upload(request):
	data = {}
	if request.method == 'POST':
		file_data = request.FILES['excelFile']
		app_name=request.POST['app_name']
		model_name=request.POST['model_name']       
		file_name = default_storage.save(file_data.name, file_data)
		uploaded_file_url = default_storage.url(file_name)
		file_path=data['uploaded_file_url']= os.path.join(settings.MEDIA_ROOT, file_name)
		kwargs={'file_path':file_path,"app_name":app_name,"model_name":model_name}
		data['status']=excel_to_model(**kwargs)
	return JsonResponse(data)  

"""
This method will convert input excel file to specifide model object
filepath: input file path
app_name: app name
model_name: name of the model to be created
"""  
def model_publish(objmodel,**records):
	objmodel.save(**records)

def ls_publish(**records):
	Lobj=Learner.objects.get(Sid=records['Sid'])
	Lobj.update_learning_style(Active=records["Active"],Sensitive=records["Sensitive"],Global=records["Global"],Visual=records["Visual"])
	return True
	



def excel_to_model(file_path,app_name,model_name):
	excel_df=pd.concat(pd.read_excel(file_path, sheet_name=None), ignore_index=True)
	df_records = excel_df.to_dict('records')
	#locate requested model class, apps.all_models is dictionary which hold all model classes 
	model_class=apps.all_models[app_name][model_name] 
	#itreate over the records (every row as dictionory) and create model instances
	model_instances = [model_class(**record) for record in df_records]
	model_class.objects.bulk_create(model_instances)
	return True

"""
this method will convert requested model to excel file
Three arguments are there appname model name and required fields
"""
def model_to_excel(app_name,model_name,required_fields):    
	#locate requested model class, apps.all_models is dictionary which hold all model classes 
	model_class=apps.all_models[app_name][model_name] 
	df = pd.DataFrame(list(model_class.objects.values(*required_fields)))
	excel_file = IO()
	xlwriter = pd.ExcelWriter(excel_file, engine='xlsxwriter')
	df.to_excel(xlwriter, 'sheetname')
	xlwriter.save()
	xlwriter.close()
	# important step, rewind the buffer or when it is read() you'll get nothing
	# but an error message when you try to open your zero length file in Excel
	excel_file.seek(0)
	# set the mime type so that the browser knows what to do with the file
	response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
	# set the file name in the Content-Disposition header
	response['Content-Disposition'] = 'attachment; filename=myfile.xlsx'
	return response


"""
return cluster based comparison
"""

def findKM(id='1',topic='All'):
	ldf=get_learner_dataframe()
	Background=list(ldf['BackgroundKnowledge'].unique())
	def findBK(bk):
		return Background.index(bk)*100
	ldf['BackgroundKnowledge'] =ldf.apply(lambda x: findBK(x['BackgroundKnowledge']), axis=1)
	kmeans5 = KMeans(n_clusters=40, random_state=42)
	k_predictor= kmeans5.fit(ldf)
	ldf['s_class']=k_predictor.predict(ldf)
	SID_ARRAY = ldf.groupby('s_class')['SID'].unique()[ldf[ldf['SID']==id]['s_class']]
	if len(SID_ARRAY)>=1:
		id_list=SID_ARRAY[ldf[ldf['SID']==id].iloc[0,6]].tolist()
		Mached=Learner.objects.filter(Sid__in=id_list)
		L_S=[]
		I_D=[]
		Rate=[]
		Topic=[]
		urls=[]
		for Lobj in Mached:
			for L_Session in Lobj.Learning_Sessions.all():
				if L_Session is not None:
					for L_S_L in L_Session.Learning_Session_Logs.all():
						L_S.append(L_S_L.VisitedMaterial.Title)
						Rate.append(L_S_L.Rating)
						I_D.append(L_S_L.VisitedMaterial.id)
						Topic.append(L_S_L.VisitedMaterial.Topic)
						urls.append(L_S_L.VisitedMaterial.Link)
	#Mached_Sessions=[m_learner.Learning_Sessions for m_learner in Mached]
		#Mached_Sessions_list=[LS. for sessions in matc]
		Final_dc={'id':I_D,'Tittle':L_S,'Topic':Topic,'URL':urls,'Rating':Rate}
		final_df=pd.DataFrame(Final_dc)
		if topic!='All':
			final_df=final_df[final_df['Topic']==topic]
		#return final_df.head(5).values.tolist()
		final_df=final_df.groupby(['id'], as_index=False).agg({'Tittle': 'first', 'Rating': 'mean', 'URL': 'first'})
		#final_df=pd.DataFrame(final_df.groupby('Tittle')['Rating'].agg(lambda x: x.unique().sum()/x.nunique()))
		final_df.sort_values(by='Rating',ascending=False,inplace=True)
		
		return final_df.head(5).values.tolist()
	else:
		return None

"""

BackgroundKnowledge
LS.Active
LS.Sensitive
LS.Global
LS.Visual
"""
def get_learner_dataframe():
	Learner_all=Learner.objects.exclude(LS__isnull=True)
	learner_list=[[lobj.Sid,lobj.BackgroundKnowledge,lobj.LS.Active,lobj.LS.Sensitive,lobj.LS.Global,lobj.LS.Visual] for lobj in Learner_all]
	learner_df=pd.DataFrame(learner_list,columns=['SID','BackgroundKnowledge','Active','Sensitive','Global','Visual'])
	return learner_df

#upload learner data
def learner_excel_upload(request):
	data = {}
	if request.method == 'POST':
		file_data = request.FILES['excelFile']
		app_name=request.POST['app_name']
		model_name=request.POST['model_name']       
		file_name = default_storage.save(file_data.name, file_data)
		uploaded_file_url = default_storage.url(file_name)
		file_path=data['uploaded_file_url']= os.path.join(settings.MEDIA_ROOT, file_name)
		learner_df=file_to_dataframe(file_path)
		learning_style_df=file_to_dataframe(file_path,sheet_name="learning_style")
		learning_session_df=file_to_dataframe(file_path,sheet_name="learner_dynamic")
		#upload Learners
		learner_records = learner_df.to_dict('records')
		#locate requested model class, apps.all_models is dictionary which hold all model classes 
		model_class=apps.all_models[app_name][model_name] 
		#itreate over the records (every row as dictionory) and create model instances
		model_instances = [model_publish(model_class(),**record) for record in learner_records]
		#model_class.objects.bulk_create(model_instances)
		learning_style_records = learning_style_df.to_dict('records')
		results = [ls_publish(**ls_record) for ls_record in learning_style_records]
		ld_records = learning_session_df.to_dict('records')
		
		for re in ld_records:
			Lobj=Learner.objects.get(Sid=re['SID'])
			score=str(re['Material_Visited_Frequency']).split(",")
			VMS =str(re['VisitedMaterials']).split(",")
			time=str(re['Material_Visited_Time(Mins)']).split(",")
			for (a,b,c) in zip(VMS,score,time):
				kwargs={'LMID': a, 'time_spent': b,'score':c}
				if 'LS' in request.session:
					kwargs['LS']=request.session['LS']
				request.session['LS']=Lobj.add_session(**kwargs)
			re['LS']=request.session['LS']
			Lobj.add_ls(**re)	
			del request.session['LS'] 
			request.session.modified = True


	return JsonResponse(data) 


#upload learner data
def history_upload(request):
	data = {}
	if request.method == 'POST':
		file_data = request.FILES['excelFile']
		app_name=request.POST['app_name']
		model_name=request.POST['model_name']       
		file_name = default_storage.save(file_data.name, file_data)
		uploaded_file_url = default_storage.url(file_name)
		file_path=data['uploaded_file_url']= os.path.join(settings.MEDIA_ROOT, file_name)
		learning_session_df=pd.concat(pd.read_excel(file_path, sheet_name=None), ignore_index=True)
		ld_records = learning_session_df.to_dict('records')
		for re in ld_records:
			Lobj=Learner.objects.get(Sid=re['SID'])
			score=str(re['Material_Ratings']).split(",")
			VMS =str(re['Materials_Visited']).split(",")
			time=str(re['Material_Visited_Time(Mins)']).split(",")
			for (a,b,c) in zip(VMS,score,time):
				kwargs={'LMID': a, 'time_spent': b,'score':c}
				if 'LS' in request.session:
					kwargs['LS']=request.session['LS']
				request.session['LS']=Lobj.add_session(**kwargs)
			re['Login_Time']='0'
			re['Logout_Time']='0'
			re['LS']=request.session['LS']
			Lobj.add_ls(**re)	
			del request.session['LS'] 
			request.session.modified = True
	return JsonResponse(data) 