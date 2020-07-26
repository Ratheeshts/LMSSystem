from django.forms import ModelForm
from learner.models import LearningMaterial
from learner.models import Learner,Learning_Style
from django import forms
"""
This form is for product Category

"""
class LearningMaterialForm(ModelForm):
    class Meta:
        model=LearningMaterial
        exclude = ['published_date']

    def __init__(self, *args, **kwargs):
        super(LearningMaterialForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'col-xs-10 col-sm-5',
                'id':str(field)
            })
        OPTIONS = [("text", "text"),
        ("figure", "figure"),
        ("Diagram", "Diagram"),("slide", "slide"),("Simulation", "Simulation"),("lecture", "lecture")]
        
        
        self.fields['LR_Type'] = forms.MultipleChoiceField(
                       widget=forms.CheckboxSelectMultiple(),choices=OPTIONS,)
        # this function will be used for the validation 
    def clean(self): 
        # data from the form is fetched using super function 
        super(LearningMaterialForm, self).clean()         
        # return any errors if found 
        return self.cleaned_data 

class LearnerForm(ModelForm):
    class Meta:
        model=Learner
        exclude = ['published_date','user','Learning_Sessions','LS']

    def __init__(self, *args, **kwargs):
        super(LearnerForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'col-xs-10 col-sm-5',
                'id':str(field)
            })
        
        # this function will be used for the validation 
    def clean(self): 
        # data from the form is fetched using super function 
        super(LearnerForm, self).clean()         
        # return any errors if found 
        return self.cleaned_data 
class LSForm(ModelForm):
    class Meta:
        model=Learning_Style
        exclude = ['Is_Reflective','Is_Active','Is_Sensitive','Is_Intutive','Is_Global','Is_Sequential','Is_Visual','Is_Verbal','published_date' ]


   
        
        # this function will be used for the validation 
    def clean(self): 
        # data from the form is fetched using super function 
        super(LSForm, self).clean()         
        # return any errors if found 
        return self.cleaned_data 