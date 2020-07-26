from django.db import models
from django.contrib.auth.models import User
from django.utils  import timezone
import urllib.request
import datetime

# Create your models here.
class Learning_Style(models.Model):
    
    Active=models.IntegerField(default=50)
    Is_Reflective=models.BooleanField(default=False)
    Is_Active=models.BooleanField(default=False)
    Sensitive=models.IntegerField(default=50)
    Is_Sensitive=models.BooleanField(default=False)
    Is_Intutive=models.BooleanField(default=False)
    Global=models.IntegerField(default=50)
    Is_Global=models.BooleanField(default=False)
    Is_Sequential=models.BooleanField(default=False)
    Visual=models.IntegerField(default=50)
    Is_Visual=models.BooleanField(default=False)
    Is_Verbal=models.BooleanField(default=False)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self,**kwargs):
        self.Active=kwargs['Active']
        self.Is_Active=self.isDominant(self.Active)
        self.Is_Reflective=not self.Is_Active
        self.Sensitive=kwargs['Sensitive']
        self.Is_Sensitive=self.isDominant(self.Sensitive)
        self.Is_Intutive=not self.Is_Sensitive
        self.Global=kwargs['Global']
        self.Is_Global=self.isDominant(self.Global)
        self.Is_Sequential=not self.Is_Global
        self.Visual=kwargs['Visual']
        self.Is_Visual=self.isDominant(self.Visual)
        self.Is_Verbal=not self.Is_Visual
        self.published_date = timezone.now()
        self.save()

    def isDominant(self,value):
        result=int(value)-50
        if(result>=0):
            return True
        else:
            return False
class LearningMaterial(models.Model):
    STRUCTURE_CHOICES=[('Linear','Linear'),('Hiearchy','Hiearchy'),('Collection','Collection'),('Atomic','Atomic'),('Text','Text')]
    INTRACTIVE_TYPE_CHOICES=[('Expositive','Expositive'),('Intractive','Intractive'),('Intractive','Intractive')]
    INTRACTIVE_LEVEL_CHOICES=[('Very Low','Very Low'),('Low','Low'),('Medium','Medium'),('Heigh','Heigh')]
    FORMAT_CHOICES=[('text','html/text'),('html/video','html/video'),('html/graphics','html/graphics')]
    DIFFICULTY_CHOICES=[('very easy','very easy'),('easy','easy'),('medium','medium'),('difficulty','difficulty')]
    Topic=models.CharField(max_length=300)
    LMID=models.CharField(max_length=100,unique=True)
    Title=models.CharField(max_length=300)
    Structure=models.CharField(max_length=300,choices=STRUCTURE_CHOICES,null=True)
    LR_Type=models.CharField(max_length=50,null=True)
    Intractive_Type=models.CharField(max_length=50,choices=INTRACTIVE_TYPE_CHOICES,null=True)
    Intractive_Level=models.CharField(max_length=50,choices=INTRACTIVE_LEVEL_CHOICES,null=True)
    Format=models.CharField(max_length=50,choices=FORMAT_CHOICES,null=True)
    Difficulty=models.CharField(max_length=50,choices=DIFFICULTY_CHOICES,null=True)
    Link=models.URLField(max_length = 200) 
    # To be replaced with Recommendation Algorithm



    def save(self,**kwargs):
        self.Topic=kwargs['Topic']
        self.Structure= kwargs.get('Structure')
        self.LR_Type = kwargs.get('LR_Type')
        self.LMID=kwargs['LMID']
        self.Format=kwargs['Format']
        self.Intractive_Type=kwargs.get('Intractive_Type')
        self.Title=kwargs['Title']
        self.Intractive_Level=kwargs['Intractive_Level']
        self.Difficulty=kwargs['Difficulty']
        self.Link=kwargs['Link']

class Session_Log(models.Model):
    VisitedMaterial=models.ForeignKey(LearningMaterial, on_delete=models.CASCADE ,related_name="slog")
    Visted_Time=models.IntegerField(default=0)
    Rating=models.FloatField(default=0)

    def publish(self,**kwargs):
        if 'lm' in kwargs:
            self.VisitedMaterial=LearningMaterial.objects.get(pk=kwargs['lm'])
        else:
            self.VisitedMaterial=LearningMaterial.objects.get(LMID=kwargs['LMID'])
        
        self.Visted_Time=kwargs['time_spent']
        self.Rating=kwargs['score']
        self.save()
    
    
class Learning_Session(models.Model):
    Sid=models.AutoField(primary_key=True)
    Visted_Materials=models.CharField(max_length=50,default='')
    Learning_Session_Logs=models.ManyToManyField(Session_Log,related_name="l_s") 
    Login_Time=models.CharField(max_length=50,null=True)
    Logout_Time=models.CharField(max_length=50,null=True)

    def add_session_log(self,visited):
        
        if self.Visted_Materials!='':
            self.Visted_Materials=str(self.Visted_Materials)+","+str(visited.VisitedMaterial.id)
        else:
            self.Visted_Materials=visited.VisitedMaterial.id
        
        self.Learning_Session_Logs.add(visited)
        self.save()
        return self.Sid


        
 


class Learner(models.Model):
    Male='M'
    Female='F'
    GENDER_CHOICES=[(Male,'Male'),(Female,'Female')]
    Sid=models.CharField(max_length=50,null=True)
    BRANCH_CHOICES=[('CS','Computer Science'),('MCS','Mathematics with Computer Science'),('BCS','BTech Computer Science'),('BIT','BTech Information Technology'),
    ('MCA','Master of Computer Applications'),('MC','Mathematics with Computer'),('Science','Science'),('MTech Computer Science','MTech Computer Science'),('BSc Computer Science','BSc Computer Science'),('MSc Computer Science','MSc Computer Science')]
    QUALIFICATION_CHOICES=[('HS','HS'),('Post-Graduate','Post-Graduate'),('Graduate','Graduate')]
    BK_CHOICES=[('Expert','Expert'),('Basic','Basic'),('Intermediate','Intermediate')]
    Name=models.CharField(max_length=50)
    Password=models.CharField(max_length=50,null=True)
    Age=models.IntegerField(default=18)
    Gender=models.CharField(max_length=3,choices=GENDER_CHOICES,null=True)
    Branch=models.CharField(max_length=50,choices=BRANCH_CHOICES,null=True)
    Qualification=models.CharField(max_length=50,choices=QUALIFICATION_CHOICES,null=True)
    BackgroundKnowledge=models.CharField(max_length=50,choices=BK_CHOICES,default='Basic')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # notice the absence of a "Password field", that is built in.
        #overide save method by adding a published date

    LS=models.OneToOneField(Learning_Style,  
          on_delete = models.CASCADE,null=True) 
    Learning_Sessions=models.ManyToManyField(Learning_Session,related_name="lnr")

    published_date = models.DateTimeField(blank=True, null=True)
     #publish object

    def add_session(self,**kwargs):
        SL=Session_Log()
        SL.publish(**kwargs)
        if 'LS' not in kwargs:
            LS=Learning_Session()
            LS.save()
        else:
            LS=Learning_Session.objects.get(pk=kwargs['LS'])
        sid=LS.add_session_log(SL)
        return sid

  

    def add_ls(self,**kwargs):
         LS=Learning_Session.objects.get(pk=kwargs['LS'])
         LS.Login_Time=str(kwargs['Login_Time'])
         LS.Logout_Time=str(kwargs['Logout_Time'])
         LS.save()
         self.Learning_Sessions.add(LS)
         super(Learner,self).save()

    def add_learning_session(self,request):
        LS=Learning_Session.objects.get(pk=request.session['LS'])
        now = datetime.datetime.now()
        LS.Logout_Time=str(now.strftime("%Y-%m-%d %H:%M:%S"))
        LS.Login_Time=str(request.session['Login_Time'])
        LS.save()
        self.Learning_Sessions.add(LS)
        super(Learner,self).save()
        request.session['LS'] = {}

    def update_learning_style(self,**kwargs):
        if all (k in kwargs for k in ("Active","Sensitive","Global","Visual")):
            lsObj=Learning_Style()
            lsObj.publish(Active=kwargs["Active"],Sensitive=kwargs["Sensitive"],Global=kwargs["Global"],Visual=kwargs["Visual"])
            self.LS=lsObj
            super(Learner,self).save()
        return True


    def save(self,**kwargs):
        self.Name=kwargs['Name']
        self.Password= kwargs.get('Password', "1234")
        self.user = User.objects.create_user(self.Name, 'lennon@thebeatles.com', self.Password)
       
        self.Age=int(kwargs['Age'])
        self.Gender=kwargs['Gender']
        self.Branch=kwargs['Branch']
        self.Qualification=kwargs['Qualification']
        self.BackgroundKnowledge=kwargs['BackgroundKnowledge']
        self.published_date = timezone.now()
        if all (k in kwargs for k in ("Active","Sensitive","Global","Visual")):
            lsObj=Learning_Style()
       # ls.publish(Name,Age,Gender,Branch,Qualification,BackgroundKnowledge,)
            lsObj.publish(Active=kwargs["Active"],Sensitive=kwargs["Sensitive"],Global=kwargs["Global"],Visual=kwargs["Visual"])
            self.LS=lsObj
        if kwargs['Sid']:
            self.Sid=kwargs['Sid']
        else:
            self.Sid=""+str(self.user.id)
        super(Learner,self).save()

    def __str__(self):
        return self.Name


