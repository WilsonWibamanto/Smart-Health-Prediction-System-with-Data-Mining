from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User
from .models import Liver, Heart
from django.db.models import Q
import pandas as pd
import MySQLdb
import joblib

loaded_model=joblib.load(r'models\LiverDisease.pkl')
loaded_model2=joblib.load(r'models\HeartDisease.pkl')

db = MySQLdb.connect(host="localhost",
                     user="admin",
                     passwd="Admin123",
                     db="django")
cur = db.cursor()

def home(request):
    return render(request,'main.html')

def liver(request):
    return render(request,'liver.html')

def heart(request):
    return render(request,'heart.html')

@login_required(login_url="/login/")
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,f'Your account has been updated')
            print(messages)
            return redirect('/profile/')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {'u_form': u_form,'p_form': p_form}

    return render(request,'profile.html',context)

def predictLiver(request):
    print(request)
    if request.method == 'POST':
        liver = {}
        liver['age']=request.POST.get('age')
        liver['gender']=request.POST.get('gender')
        liver['totBilirubin']=request.POST.get('totBilirubin')
        liver['dirBilirubin']=request.POST.get('dirBilirubin')
        liver['alkPhos']=request.POST.get('alkPhos')
        liver['alanAmino']=request.POST.get('alanAmino')
        liver['asparAmino'] = request.POST.get('asparAmino')
        liver['totProt'] = request.POST.get('totProt')
        liver['albumin'] = request.POST.get('albumin')
        liver['agratio'] = request.POST.get('agratio')
        testData = pd.DataFrame({'x': liver}).transpose()
        scoreVal = loaded_model.predict(testData)[0]
        liver['result'] = scoreVal

        columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in liver.keys())
        values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in liver.values())
        sql = "INSERT INTO %s ( %s ) VALUES ( %s );" % ('liver', columns, values)
        cur.execute(sql)
        db.commit()

    if scoreVal == 1:
        result ="Very Likely"
    else:
        result ="Very Unlikely"
    context = {'result': result ,'liver': liver}
    return render(request, 'liver.html',context)

def predictHeart(request):
    print(request)
    if request.method == 'POST':
        heart = {}
        heart['age'] = request.POST.get('age')
        heart['gender'] = request.POST.get('gender')
        heart['cp'] = request.POST.get('cp')
        heart['trestbps'] = request.POST.get('trestbps')
        heart['chol'] = request.POST.get('chol')
        heart['fbs'] = request.POST.get('fbs')
        heart['restecg'] = request.POST.get('restecg')
        heart['thalach'] = request.POST.get('thalach')
        heart['exang'] = request.POST.get('exang')
        heart['oldpeak'] = request.POST.get('oldpeak')
        heart['slope'] = request.POST.get('slope')
        heart['ca'] = request.POST.get('ca')
        heart['thal'] = request.POST.get('thal')
        testData = pd.DataFrame({'x': heart}).transpose()
        scoreVal = loaded_model2.predict(testData)[0]
        heart['result'] = scoreVal

        columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in heart.keys())
        values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in heart.values())
        sql = "INSERT INTO %s ( %s ) VALUES ( %s );" % ('heart', columns, values)
        cur.execute(sql)
        db.commit()

    if scoreVal == 1:
        result ="Very Likely"
    else:
        result ="Very Unlikely"
    context = {'result': result ,'heart': heart}
    """context = {'scoreVal':scoreVal}"""
    return render(request, 'heart.html',context)

@login_required(login_url="/login/")
def viewDatabase(request):
    context={'Liver': Liver.objects.all(), 'Heart': Heart.objects.all()}
    return render(request,'viewDB.html',context)

def search(request):
    context={'User': User.objects.all()}
    return render(request,'search.html',context)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Succesfully Registered, You are now able to log in to your account')
            print(messages)
            return redirect('/login/')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html',{'form': form})


