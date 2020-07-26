from django.shortcuts import render
import datetime
from learner.forms import LearningMaterialForm
from learner.forms import LearnerForm,LSForm
from django.contrib.auth.models import User
from common import views as com
from common import paginate
import urllib.request
from django.http import JsonResponse
from django.shortcuts import render,get_object_or_404
from learner.models import LearningMaterial,Learning_Style,Session_Log,Learning_Session
from learner.models import Learner
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import redirect

# Create your views here.
# Create your views here.

# return dashboard view
def index(request):
    return(render(request,'learner/home.html',{'page_title':'LMS Dashboard'}))
def read_material(request):
    return(render(request,'learner/readmaterials.html',{'page_title':'Read Material'}))
def history(request):
    user = request.user
    page_request=1
    if (request.method=='GET'):
        page_request = request.GET.get('page', 1)
        if request.user.id==1:
            Ls_all= Learning_Session.objects.all()  
        else:
            lobj=Learner.objects.get(user_id=request.user.id)
            Ls_all= lobj.Learning_Sessions.all()
    #paginate result query set using get_page function
    page_details=paginate.get_page(object_set=Ls_all,page_count=0,page=page_request) 
    page_details['page_title']='history'
    page_details['app_name']='learner'
    page_details['model_name']='learning_session'
    return render(request,'learner/history.html',page_details)

def add_learn_material(request):
     # if requets is post we need to store data to DB
    if request.method == 'POST':
        data ={}

        form = LearningMaterialForm(data=request.POST)
        if form.is_valid():
            LearningMaterial = form.save(commit=True)
        else:
            context['form'] = form
            return render(request, 'learner/add_learn_material.html', context)
    form = LearningMaterialForm()
    context = {'form': form,
               'page_title': 'LMS-add_learn_material'}

    return render(request, 'learner/add_learn_material.html', context)

def add_session(request,pk):
    data ={}
    if request.method == 'GET':
        time_spent=request.GET.get('timespent')
        score=request.GET.get('score')
        lm=request.GET.get('lm')
        current_user = request.user
        SL=Session_Log()
        SL.publish(lm=lm,time_spent=time_spent,score=score)
        if 'LS' not in request.session:
            newLsObj=Learning_Session()
            newLsObj.save()
            current_user.LS=newLsObj
            sid=current_user.LS.add_session_log(SL)
            request.session['LS']=sid
            data['status'] = True
        else:
            LS=Learning_Session.objects.get(pk=request.session['LS'])
            sid=LS.add_session_log(SL)
            data['status'] = True
    return JsonResponse(data)


def view_learners(request):
    user = request.user
    page_details={}
    page_details['page_index']=0  
    page_request=1
    if (request.method=='GET'):
        page_request = request.GET.get('page', 1)
        Learner_all= Learner.objects.all() 
    #paginate result query set using get_page function
    page_details=paginate.get_page(object_set=Learner_all,page_count=0,page=page_request) 
    page_details['page_title']='Learners'
    page_details['app_name']='learner'
    page_details['model_name']='learner'

    return render(request, 'learner/learners.html',
                  page_details)
                  
def view_learning_materials(request,topic="All"):
    user = request.user
    page_details={}
    Topic_All= LearningMaterial.objects.all().values('Topic').distinct()
    topic=topic.replace('-',' ')
    L_list=com.findKM(id=str(request.session['Sid']),topic=topic)
    page_details['page_index']=0  
    page_request=1
    if (request.method=='GET'):
        page_request = request.GET.get('page', 1)
        if(topic!='All'):
             LM_all= LearningMaterial.objects.filter(Topic=topic)
        else:
            LM_all= LearningMaterial.objects.all() 
       
    #paginate result query set using get_page function
    page_details=paginate.get_page(object_set=LM_all,page_count=0,page=page_request) 
    page_details['page_title']='LMS-view all Materials'
    page_details['app_name']='learner'
    page_details['model_name']='LearningMaterial'
    page_details['topic_list']=Topic_All#L_list.to_html()
    page_details['id']=request.user.id
    page_details['L_list']=L_list if L_list is not None  else 'No data to display' 
    return render(request, 'learner/view_learning_materials.html',
                  page_details)
def view_materials(request):
    user = request.user
    page_details={}
    page_details['page_index']=0  
    page_request=1
    if (request.method=='GET'):
        page_request = request.GET.get('page', 1)
        LM_all= LearningMaterial.objects.all() 
    #paginate result query set using get_page function
    page_details=paginate.get_page(object_set=LM_all,page_count=0,page=page_request) 
    page_details['page_title']='LMS-view all Materials'
    page_details['app_name']='learner'
    page_details['model_name']='learningmaterial'
    return render(request, 'learner/materials.html',
                  page_details)


#To be replaced with KNN

def recommend(MyModel):
    rec_set=set()        
    c=0
    while c<5:
        obj=MyModel.objects.order_by('?').first()
        rec_set.add(obj)
        c=c+1
    return rec_set
def logout_request(request):
    if request.user.id!=1:
       if 'LS' in request.session:
           lobj=Learner.objects.get(user_id=request.user.id)
           lobj.add_learning_session(request)
        
    request.session.flush()
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("login")

def read_material(request,pk):
    data={}
    data['pk']=pk
    requested_lm=get_object_or_404(LearningMaterial, pk=pk
            )
    fp = urllib.request.urlopen("http://www.python.org")
    mybytes = fp.read()
    mystr = mybytes.decode("utf8")
    fp.close()
    data['html']= mystr
    data['LM']=requested_lm
    return render(request, 'learner/read_material.html',
                  data)

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                now = datetime.datetime.now()
                request.session['Login_Time']=now.strftime("%Y-%m-%d %H:%M:%S")
                request.session['Sid']=1
                if user.id!=1:
                    request.session['Sid']=Learner.objects.get(user_id=user.id).Sid
                messages.info(request, f"You are now logged in as {username}")
                return redirect('view_learning_materials')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request = request,
                    template_name = "learner/login.html",
                    context={"form":form})

def add_learner(request):
     # if requets is post we need to store data to DB
    if request.method == 'POST':
        data ={}
        Sid=request.POST.get("Sid", "")
        Name=request.POST.get("Name", "")
        Password=request.POST.get("Password", "1234")
        Age=request.POST.get("Age", "18")
        Gender=request.POST.get("Gender", "")
        Branch=request.POST.get("Branch", "")
        Qualification=request.POST.get("Qualification", "")
        BackgroundKnowledge=request.POST.get("BackgroundKnowledge", "")
        Active=request.POST.get("Active")
        Sensitive=request.POST.get("Sensitive")
        Global=request.POST.get("Global")
        Visual=request.POST.get("Visual")
       # ls.publish(Name,Age,Gender,Branch,Qualification,BackgroundKnowledge,)
        LearnerObj = Learner()
        LearnerObj.save(  Sid=Sid,Name=Name,Password=Password,Age=Age,Gender=Gender,Branch=Branch,Qualification=Qualification,
        BackgroundKnowledge=BackgroundKnowledge,Active=Active,Sensitive=Sensitive,Global=Global,Visual=Visual)
    form = LearnerForm()
    lsf=LSForm()
    context = {'form': form,'lsf':lsf,
               'page_title': 'LMS-add_learner'}

    return render(request, 'learner/add_learner.html', context)