from django.shortcuts import render, redirect
from django import http
from django.urls import path
from django.shortcuts import redirect, render, HttpResponse
from django.http import HttpResponse, request
from django.core.paginator import Paginator
from fireo.queries import filter_query
# from .decoration import adminuser
from django.core.paginator import Paginator
from .models import *
import os
from .settings import BASE_DIR
import fireo
#anish Emailer
from email.mime.multipart import MIMEMultipart
from email.utils import make_msgid
import smtplib
from django.contrib.auth.forms import UserCreationForm
from django.core.mail.message import MIMEMixin
from django.http import HttpResponse
from django.shortcuts import render

import urllib
import imaplib
import email
import json
# from .sendemail_form import EmailForm
from django.core.mail import send_mail, send_mass_mail,EmailMessage
import re
import datetime
import os

from django.http import HttpResponse, HttpResponseRedirect
# from background_task import background
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from email.mime.message import MIMEMessage
from textwrap import dedent
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import make_msgid
import time
from html import escape, unescape
# database stuff
import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
cred = credentials.Certificate(
    os.path.join(BASE_DIR, "serviceAccountKey.json"))
firebase_admin.initialize_app(cred)
db = firestore.client()
databunny = {}

firebaseConfig = {
    "apiKey": "AIzaSyDlZMu8lypZDEhRpMVKlD3JcTuvItFaG2A",
    "authDomain": "bimaxpress-cashless.firebaseapp.com",
    "projectId": "bimaxpress-cashless",
    "storageBucket": "bimaxpress-cashless.appspot.com",
    "messagingSenderId": "577257002368",
    "databaseURL": "https://accounts.google.com/o/oauth2/auth",
    "appId": "1:577257002368:web:489252768c47b398465d65",
    "measurementId": "G-Y8B68GW5YX"
}
mth = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec" ]

firebase = pyrebase.initialize_app(firebaseConfig)
authe = firebase.auth()

def hospital(request):
    return render(request,'hospital.html')

def plandetails(request):
    return render(request,'plandetails.html')

def hospitalEdit(request):
    return render(request,'hospitalEdit.html')

def doctor(request):
    return render(request,'doctor.html')

def doctorEdit(request):
    return render(request,'doctorEdit.html')

def analist(request):
    return render(request,'analist.html')

def analistEdit(request):
    return render(request,'analistEdit.html')

def analistAdd(request):
    return render(request,'analistAdd.html')

def rateList(request):
    return render(request,'rateList.html')

def rateListDetails(request):
    return render(request,'ratelistDetails.html')

def EmpanelledCompanies(request):
    return render(request,'empanelledCompanies.html')

def empanelledCompaniesAdd(request):
    return render(request,'empanelledCompaniesAdd.html')

def randomCompany(request):
    return render(request,'randomCompany.html')

def doctorAdd(request):
    return render(request,'doctorAdd.html')

def caseDetails(request):
    return render(request,'caseDetails.html')

def newAction(request):
    return render(request,'newAction.html')

def loginPage(request):
    return render(request,'loginPage.html')





def postsignIn(request):
    context = {}
    cases_data = []
    counter=0
    list_status = ['draft',  'Unprocessed','query', 'Approved', 'Reject',
                       'Enhance Discharge', 'Discharge Approved', 'All Processed']
    values = {
    "draft":0,
    "Unprocessed":0,
    "query":0,
    "Approved":0,
    "Reject":0,
    "Enhance_Discharge":0,
    "Discharge_Approved":0,
    "All_Processed":0
    }
    if request.method == "POST":

        email = request.POST.get('email')
        pasw = request.POST.get('pass')
        try:
            user = authe.sign_in_with_email_and_password(email, pasw)
            request.session['email'] = user['email']

        except:
            message = "Invalid Credentials!!Please ChecK your Data"
            return render(request, "login.html", {"message": message})

        docs = db.collection(u'backend_users').where(
            u'Email', u'==', user['email']).stream()
        for doc in docs:
            Role = doc.to_dict()
            request.session['role'] = Role['Role']

        if Role['Role'] != 'admin':
            request.session['hospital_email'] = Role['hospital']
            data = Hospitals.collection.fetch()
            for obj in data:
               
                print("Hospital Name : ", obj.name)
                if(obj.id == request.session['hospital_email']):
                    val = Cases.collection.parent(obj.key).fetch()
                    
                    for i in val:
                        counter=counter+1
                        if(i.status == "done"):
                            print("--------")
                            print("case Number", i.id)
                            print("Status:", i.status)
                        
                            if(i.formstatus == ""):
                                values['draft'] += 1
                            if(i.formstatus == "draft"):
                                values['draft'] += 1
                            if(i.formstatus == "Unprocessed"):
                                values['Unprocessed'] += 1
                                values['draft'] += 1
                            if(i.formstatus == "query"):
                                values['query'] += 1
                                values['draft'] += 1
                            if(i.formstatus == "Approved"):
                                values['Approved'] += 1
                                values['draft'] += 1
                            if(i.formstatus == "Reject"):
                                values['Reject'] += 1
                                values['draft'] += 1
                            if(i.formstatus == "Enhance Discharge"):
                                values['Enhance_Discharge'] += 1
                                values['draft'] += 1
                            if(i.formstatus == "Discharge Approved"):
                                values['Discharge_Approved'] += 1
                                values['draft'] += 1
                            if(i.formstatus == "All Processed"):
                                values['All_Processed'] += 1
                                values['draft'] += 1
    
                            print("formStatus", i.formstatus)
                            print("Test : ", i.test)
                            # print("doctor_name",i.doctor_name)

                            val2 = hospital_details.collection.parent(
                                i.key).fetch()
                            for j in val2:
                                print("Hospital Name : ", j.name)
                                print("Date of Admision:",j.Date_of_Admission)

                            val3 = patient_details.collection.parent(
                                i.key).fetch()
                            for m in val3:
                                print("Patient Name : ", m.Name)
                                print("Insurance Company",m.Insurance_Company)
                                if(m.Name) != None:
                                    cases_data.append(
                                        {'email': request.session['hospital_email'], 'casenumber': i.id, 'formstatus': i.formstatus, 'patient_name': m.Name,"company":m.Insurance_Company,"Date":j.Date_of_Admission})
                else:
                    continue
                
            print(values)
            
            
            context["backcase"] = "case"+str(counter+1)   
            context["cases_data"] = cases_data
            context['list_status'] = list_status
            context['values'] = values
            context['hospital_email'] = request.session['hospital_email']
            context['role'] = request.session.get('role')
            return render(request, "index.html", context)

        else:
            return HttpResponse("Successsss")


def listData(request, p):
    context = {}
    if request.session.get('role') != None:
        list_status = ['draft',  'Unprocessed','query', 'Approved', 'Reject',
                       'Enhance Discharge', 'Discharge Approved', 'All Processed']
        values = {
    "draft":0,
    "Unprocessed":0,
    "query":0,
    "Approved":0,
    "Reject":0,
    "Enhance_Discharge":0,
    "Discharge_Approved":0,
    "All_Processed":0
    }


        user_data = []
        print("this is value of p", p)
        data = Hospitals.collection.fetch()

        for obj in data:
            if(obj.id == request.session['hospital_email']):
                print("Hospital Name : ", obj.name)
                print("Hospital ID : ", obj.id)
                print("--------------")
                val = Cases.collection.parent(obj.key).fetch()
                for i in val:
                    if(i.status == "done"):
                            print("--------")
                            print("case Number", i.id)
                            print("Status:", i.status)
                            
                            if(i.formstatus == ""):
                                values['draft'] += 1
                            if(i.formstatus == "draft"):
                                values['draft'] += 1
                            if(i.formstatus == "Unprocessed"):
                                values['Unprocessed'] += 1
                                values['draft'] += 1
                            if(i.formstatus == "query"):
                                values['query'] += 1
                                values['draft'] += 1
                            if(i.formstatus == "Approved"):
                                values['Approved'] += 1
                                values['draft'] += 1
                            if(i.formstatus == "Reject"):
                                values['Reject'] += 1
                                values['draft'] += 1
                            if(i.formstatus == "Enhance Discharge"):
                                values['Enhance_Discharge'] += 1
                                values['draft'] += 1
                            if(i.formstatus == "Discharge Approved"):
                                values['Discharge_Approved'] += 1
                                values['draft'] += 1
                            if(i.formstatus == "All Processed"):
                                values['All_Processed'] += 1
                                values['draft'] += 1

                                
                            print("formStatus", i.formstatus)
                            print("Test : ", i.test)
                            # print("doctor_name",i.doctor_name)

                            val2 = hospital_details.collection.parent(
                                i.key).fetch()
                            for j in val2:
                                print("Hospital Name : ", j.name)
                                print("Date of Admision:",j.Date_of_Admission)

                            val3 = patient_details.collection.parent(
                                i.key).fetch()
                            for m in val3:
                                print("Patient Name : ", m.Name)
                                print("Insurance Company",m.Insurance_Company)
                                if(m.Name) != None:
                                    user_data.append(
                                        {'email': request.session['hospital_email'], 'casenumber': i.id, 'formstatus': i.formstatus, 'patient_name': m.Name,"company":m.Insurance_Company,"Date":j.Date_of_Admission})
                else:
                    continue

        print(user_data)
        print(p)

        context['content_data'] = user_data
        context['list_status'] = list_status
        context['values'] = values
        context['hospital_email'] = request.session['hospital_email']
        context['p'] = p

        print(p.upper())
        if p.upper() == "DRAFT":
            context['isdraft'] = True
        else:
            context['isdraft'] = False

        if p.upper() == "ISSUBMITTED_QUERY":
            context['issubmitted_query'] = True
        else:
            context['issubmitted_query'] = False

        if p.upper() == "QUERY":
            context['isquery'] = True
        else:
            context['isquery'] = False

        if p.upper() == "APPROVED":
            context['isapproved'] = True
        else:
            print("runnnniiiiiiiiiing")
            context['isapproved'] = False

        if p.upper() == "REJECT":
            context['isreject'] = True
        else:
            context['isreject'] = False

        if p.upper() == "ENHANCE DISCHARGE":
            context['isenhance'] = True
        else:
            context['isenhance'] = False

        if p.upper() == "DISCHARGE APPROVE":
            context['isdischargeapprove'] = True
        else:
            context['isdischargeapprove'] = False

        if p.upper() == "ALL PROCESSED":
            context['isallprocessed'] = True
        else:
            context['isallprocessed'] = False

        return render(request, 'renderCards.html', context)
    else:
        return redirect('login')


def updateFormstatus(request, new):
    new_status = ''
    email = ''
    old_status = ''
    case = ''
    flag = 1
    print("update form status", new)
    for char in new:
        if char == '+':
            flag = 0
        if flag == 1:
            new_status = new_status+char
        if char == '*':
            flag = 2
        if char == '&':
            flag = 3
        if flag == 0 and char != '+':
            email = email+char
        if flag == 2 and char != '*':
            old_status = old_status+char
        if flag == 3 and char != '&':
            case = case+char

    # doc_ref = db.collection(u'users').document(
    #     f'{email}').collection(u'case').document(f'{case}')
    # doc_ref.update({
    #     'formstatus': f'{new_status}',
    # })

    return HttpResponse("success")


def claimpage1(request):
    if request.session.get('role') != None:
        context = {}
        system = request.GET.get('system', None)
        flag = 0
        email = ''
        case = ''
        for char in system:
            if char == "+":
                flag = 1
            if flag == 0 and char != '+':
                email = email+char
            if flag == 1 and char != '+':
                case = case+char
        print(email)
        print(case)
        bunny = []
        docus = db.collection(u'hospitals').document(email).collection(
            u'cases').where(u'status', u'==', 'done').get()

        for i in docus:
            collections = db.collection('hospitals').document(
                email).collection(u'cases').document(case).collections()
            for collection in collections:
                for doc in collection.stream():
                    databunny[doc.id] = doc.to_dict()
                    bunny.append(doc.to_dict())
        print(databunny)
        context['akey'] = case
        context['email'] = email
        context['bunny'] = bunny
        context['data'] = databunny
        context['system'] = system

        print("cool dude", system)

        # return HttpResponse('Success')
        return render(request, 'pageAccordian.html', context)
    else:
        return redirect('login')


def claims(request):
    context = {}
    cases_data = []
    values = {
    "draft":0,
    "Unprocessed":0,
    "query":0,
    "Approved":0,
    "Reject":0,
    "Enhance_Discharge":0,
    "Discharge_Approved":0,
    "All_Processed":0
    }
    print(request.session['hospital_email'])
    print(request.session['email'])
    data = Hospitals.collection.fetch()
    for obj in data:
        print("Hospital Name : ", obj.name)
        if(obj.id == request.session['hospital_email']):
            val = Cases.collection.parent(obj.key).fetch()
            for i in val:
                if(i.status == "done"):
                            print("--------")
                            print("case Number", i.id)
                            # print("Status:", i.status)
                            if(i.formstatus == ""):
                                values['draft'] += 1
                            if(i.formstatus == "draft"):
                                values['draft'] += 1
                            if(i.formstatus == "Unprocessed"):
                                values['Unprocessed'] += 1
                                values['draft'] += 1
                            if(i.formstatus == "query"):
                                values['query'] += 1
                                values['draft'] += 1
                            if(i.formstatus == "Approved"):
                                values['Approved'] += 1
                                values['draft'] += 1
                            if(i.formstatus == "Reject"):
                                values['Reject'] += 1
                                values['draft'] += 1
                            if(i.formstatus == "Enhance Discharge"):
                                values['Enhance_Discharge'] += 1
                                values['draft'] += 1
                            if(i.formstatus == "Discharge Approved"):
                                values['Discharge_Approved'] += 1
                                values['draft'] += 1
                            if(i.formstatus == "All Processed"):
                                values['All_Processed'] += 1
                                values['draft'] += 1

                                
                            # print("formStatus", i.formstatus)
                            # print("Test : ", i.test)
                            # print("doctor_name",i.doctor_name)

                            val2 = hospital_details.collection.parent(
                                i.key).fetch()
                            for j in val2:
                                print("Hospital Name : ", j.name)
                                print("Date of Admision:",j.Date_of_Admission)

                            val3 = patient_details.collection.parent(
                                i.key).fetch()
                            for m in val3:
                                print("Patient Name : ", m.Name)
                                print("Insurance Company",m.Insurance_Company)
                                if(m.Name) != None:
                                    cases_data.append(
                                        {'email': request.session['hospital_email'], 'casenumber': i.id, 'formstatus': i.formstatus, 'patient_name': m.Name,"company":m.Insurance_Company,"Date":j.Date_of_Admission})
                else:
                    continue

    print(cases_data)
    context["cases_data"] = cases_data
    return render(request, "cases.html", context)


def logout(request):
    request.session.flush()
    return render(request, 'login.html')


def adduser(request):
    context = {}
    context['role'] = request.session.get('role')
    return render(request, 'addaccount.html', context)


def index(request):

    return render(request, 'index.html')


def about(request):
    return HttpResponse("About page bolte")


def login(request):
    message = "Provide Email password to singnIn"
    return render(request, 'login.html', {"message": message})


def dashboard(request):
    context = {}
    cases_data = []
    list_status = ['draft',  'Unprocessed','query', 'Approved', 'Reject',
                       'Enhance Discharge', 'Discharge Approved', 'All Processed']
    values = {
    "draft":0,
    "Unprocessed":0,
    "query":0,
    "Approved":0,
    "Reject":0,
    "Enhance_Discharge":0,
    "Discharge_Approved":0,
    "All_Processed":0
    }

    if request.session['role'] != "admin":
        data = Hospitals.collection.fetch()
        for obj in data:
            print("Hospital Name : ", obj.name)
            if(obj.id == request.session['hospital_email']):
                val = Cases.collection.parent(obj.key).fetch()
                for i in val:
                    if(i.status == "done"):
                        print("--------")
                        print("case Number", i.id)
                        print("Status:", i.status)
                        if(i.formstatus == ""):
                            values['draft'] += 1
                        if(i.formstatus == "draft"):
                            values['draft'] += 1
                        if(i.formstatus == "Unprocessed"):
                            values['Unprocessed'] += 1
                            values['draft'] += 1
                        if(i.formstatus == "query"):
                            values['query'] += 1
                            values['draft'] += 1
                        if(i.formstatus == "Approved"):
                            values['Approved'] += 1
                            values['draft'] += 1
                        if(i.formstatus == "Reject"):
                            values['Reject'] += 1
                            values['draft'] += 1
                        if(i.formstatus == "Enhance Discharge"):
                            values['Enhance_Discharge'] += 1
                            values['draft'] += 1
                        if(i.formstatus == "Discharge Approved"):
                            values['Discharge_Approved'] += 1
                            values['draft'] += 1
                        if(i.formstatus == "All Processed"):
                            values['All_Processed'] += 1
                            values['draft'] += 1
            
                        print("formStatus", i.formstatus)
                        print("Test : ", i.test)
                            # print("doctor_name",i.doctor_name)

                        val2 = hospital_details.collection.parent(
                                i.key).fetch()
                        for j in val2:
                            print("Hospital Name : ", j.name)
                            print("Date of Admision:",j.Date_of_Admission)

                        val3 = patient_details.collection.parent(
                                i.key).fetch()
                        for m in val3:
                            print("Patient Name : ", m.Name)
                            print("Insurance Company",m.Insurance_Company)
                            if(m.Name) != None:
                                cases_data.append(
                                    {'email': request.session['hospital_email'], 'casenumber': i.id, 'formstatus': i.formstatus, 'patient_name': m.Name,"company":m.Insurance_Company,"Date":j.Date_of_Admission})
    else:
        return render("admin login")
    
    print(values)
    context["cases_data"] = cases_data
    context['list_status'] = list_status
    context['values'] = values
    context['hospital_email'] = request.session['hospital_email']
    context['role'] = request.session.get('role')
    
    return render(request, "index.html", context)

  

    

def get_name(email):
    try:
        name = ''
        for char in email:
            if char == '@':
                return name
            name = name+char
    except:
        return None


def saveData(request):
    context = {}
    form = ""
    form_data = ""
    if request.method == "POST":
        data = request.POST.dict()
        system = request.POST.get('save', None)
        form = request.POST.get('last', None)
        if(form != None):
            form_data = form[-4:]

        print("system = ", system)

        flag = 0
        email = ''
        case = ''
        print(" System value when in last"+f"{system}")
        print(system)
        if system == None:
            context['data'] = data
            print("None called")
            return render(request, "hdfc.html", context)
        if system == "":
            context['data'] = data
            print("Emptycalled")
            return render(request, "hdfc.html", context)

        if system != None:
            print("running inside")
            for char in system:
                if char == "+":
                    flag = 1
                if flag == 0 and char != '+':
                    email = email+char
                if flag == 1 and char != '+':
                    case = case+char
            print("email = ", email)
            print("case = ", case)
            context["data"] = data
            # return render(request,"test.html",context)
            try:
                patient_details = {
                    "Type": data.get("admissiontype", ""),
                    "Insurance_Company": data["insurance_company"],
                    "Name": data["patient_details_name"],
                    "Gender": data["patient_details_gender"],
                    "AgeYear": data["patient_details_ageYear"],
                    "AgeMonth": data["patient_details_ageMonth"],
                    "AgeDate": data["patient_details_date"],
                    "Contact_Number": data["patient_details_contact_number"],
                    "NumberOfAttendingRelative": data["patient_details_numberOfAttendingRelative"],
                    "Id_card_number": data["patient_details_insuredMemberIdCardNo"],
                    "PolicyNumberorCorporateName": data["patient_details_policyNumberorCorporateName"],
                    "EmployeeId": data["patient_details_EmployeeId"],
                    "Currentaddress": data["patient_details_currentAddress"],
                    "patient_details_occupation": data["patient_details_occupation"],
                    "NameOfTreatingDoctor": data["doctor_nameOfTreatingDoctor"],
                    "Doctor_ContactNumber": data["doctor_contactNumber"],
                }

                addition_details = {
                    "Nature_Of_Illness": data["doctor_natureOfLiness"],
                    "Duration_Of_Present_Ailments": data["doctor_durationOfPresentAliment"],
                    "NatureOfLiness": data["doctor_dateOfFirstConsultation"],
                    "Past_History_Of_Present_Ailments": data["doctor_PastHistoryOfPresentAlignment"],
                    "Provision_Diagnosis": data["doctor_provisionalDiagnosis"],
                    "ICD_Code": data["doctor_icdCode"],
                    "If_Other_Treatment_Provide_Details": data["doctor_ifOtherTratmentProvideDetails"],
                    "How_Did_Injury_Occur": data["doctor_howDidInjuryOccure"],
                    # "Date_Of_Injury_(dd-mm-yyyy)":data["doctor_dateOfInjury"],
                    "MandatoryPastHistoryMonth": data["admission_mandatoryPastHistoryMonth"],
                    "MandatoryPastHistoryYear": data["admission_mandatoryPastHistoryYear"],
                    "HeartDiseaseMonth": data["admission_heartDiseaseMonth"],
                    "HeartDiseaseYear": data["admission_heartDiseaseYear"],
                    "HypertensionMonth": data["admission_hypertensionMonth"],
                    "HypertensionYear": data["admission_hypertensionYear"],
                    "HyperlipidemiasMonth": data["admission_HyperlipidemiasMonth"],
                    "HyperlipidemiasYear": data["admission_HyperlipidemiasYear"],
                    "OsteoarthritisMonth": data["admission_osteoarthritisMonth"],
                    "OsteoarthritisYear": data["admission_osteoarthritisYear"],
                    "AsthmaOrCOPDOrBronchitisMonth": data["admission_asthmaOrCOPDOrBronchitisMonth"],
                    "AsthmaOrCOPDOrBronchitisYear": data["admission_asthmaOrCOPDOrBronchitisYear"],
                    "CancerMonth": data["admission_cancerMonth"],
                    "CancerYear": data["admission_cancerYear"],
                    "AlcoholOrDrugAbuseMonth": data["admission_alcoholOrDrugAbuseMonth"],
                    "AlcoholOrDrugAbuseYear": data["admission_alcoholOrDrugAbuseYear"],
                    "RelatedAlimentsMonth": data["admission_anyHIVOrSTDOrRelatedAlimentsMonth"],
                    "RelatedAlimentsYear": data["admission_anyHIVOrSTDOrRelatedAlimentsYear"],
                    "OtherAliments": data["admission_anyOtherAliments"],
                    "Reported_To_Police": data.get("doctor_reportedToPolice", ""),
                    "patient_details_HealthInsurance": data.get("patient_details_HealthInsurance", ""),
                    "familyPhysician": data.get("patient_details_familyPhysician", ""),
                    "doctor_proposedLineOfTreatment": data.get("doctor_proposedLineOfTreatment", ""),
                    "In_Case_Of_Accident": data.get("doctor_inCaseOfAccident", ""),
                    "Injury_Disease_Caused_Due_To_Substance_Abuse_Alcohol_Consumption_": data.get("doctor_injuryorDiseaseCausedDueToSubstance", ""),
                    "doctor_testAlcohol": data.get("doctor_testAlcohol", ""),
                    "isThisAEmergencyPlannedHospitalization": data.get("admission_isThisAEmergencyPlannedHospitalization", ""),
                }

                hospital_details = {
                    "Date_of_Admission": data["admission_date"],
                    "ExpectedDateOfDelivery": data["doctor_expectedDateOfDelivery"],
                    "Days_In_ICU": data["admission_daysInICU"],
                    "Room_Type": data["admission_roomType"],
                    "DateofInjury": data["doctor_dateOfInjury"],
                }

                hospital_charges = {
                    "Per_Day_Room_Rent": data["admission_perDayRoomRent"],
                    "Cost_Of_Investigation": data["admission_expectedCostForInvestigation"],
                    "ICU_Charges": data["admission_icuCharge"],
                    "OT_Charges": data["admission_otCharge"],
                    "ProfessionalFeesSurgeon": data["admission_professionalFeesSurgeon"],
                    "ConsumablesCostOfImplats": data["admission_madicineConsumablesCostOfImplats"],
                    "OtherHospitalIfAny": data["admission_otherHospitalIfAny"],
                    "All_Including_Package": data["admission_allIncludePackageCharge"],
                    "total": data["admission_sumTotalExpected"],
                }
                try:
                    db.collection(u'hospitals').document(f'{email}').collection(u'cases').document(
                        case).collection(u'patient_details').document(u'patient_details').update(patient_details)

                    db.collection(u'hospitals').document(f'{email}').collection(u'cases').document(
                        case).collection(u'patient_details').document(u'addition_details').update(addition_details)

                    db.collection(u'hospitals').document(f'{email}').collection(u'cases').document(
                        case).collection(u'hospital_details').document(u'hospital_details').update(hospital_details)

                    db.collection(u'hospitals').document(f'{email}').collection(u'cases').document(
                        case).collection(u'hospital_details').document(u'hospital_charges').update(hospital_charges)
                except:
                    
                    db.collection(u'hospitals').document(f'{email}').collection(u'cases').document(
                    case).collection(u'patient_details').document(u'patient_details').set(patient_details)

                    db.collection(u'hospitals').document(f'{email}').collection(u'cases').document(
                        case).collection(u'patient_details').document(u'addition_details').set(addition_details)

                    db.collection(u'hospitals').document(f'{email}').collection(u'cases').document(
                        case).collection(u'hospital_details').document(u'hospital_details').set(hospital_details)

                    db.collection(u'hospitals').document(f'{email}').collection(u'cases').document(
                        case).collection(u'hospital_details').document(u'hospital_charges').set(hospital_charges)
                    
                    db.collection(u'hospitals').document(f'{email}').collection(u'cases').document(case).set({
                    'formstatus': u'draft',
                    'status':"done",
                    'Type':data.get("admissiontype", ""),
                    })
                    
            except IndexError as e:
                print(e)
                return redirect(f"/claimpage1?system={email}%2B{case}")

            db.collection(u'hospitals').document(f'{email}').collection(u'cases').document(case).update({
                'formstatus': u'draft',
            })

            return redirect(f"/claimpage1?system={email}%2B{case}")

    return redirect(f"/claimpage1?system={email}%2B{case}")


def formData(request, text):
    flag = 0
    email = ''
    case = ''

    print("thiissssssssssssssssssss")

    for char in text:
        if char == "+":
            flag = 1
        if flag == 0 and char != '+':
            email = email + char
        if flag == 1 and char != '+':
            case = case+char

    context = {}
    doc_ref = db.collection(u'users').document(f'{email}').collection(
        u'case').document(f'{case}').collection(u'forms').document(u'form_data')
    doc = doc_ref.get()
    if doc.exists:
        a = doc.to_dict()
    else:
        print("no data found")
    print(a)
    context['formContents'] = a

    return render(request, 'formData.html', context)


def addQuery(request, que):
    email = ""
    case = ''
    query = ''
    flag = 0
    for char in que:
        if char == '+':
            flag = 1
        if char == '&':
            flag = 2
        if flag == 0:
            query = query+char
        if flag == 1 and char != '+':
            email = email+char
        if flag == 2 and char != '&':
            case = case+char

    print("email = ", email)
    print("case = ", case)
    print("query = ", query)

    db.collection(u'hospitals').document(f'{email}').collection(u'cases').document(
        case).update({
            'formstatus': 'query',
            'Query': query,
            "status": "filled"
        })

    return HttpResponse("success")


# Emailer Anish
def optimiser(s):
    if(s[0]=='"' and s[len(s)-1]=='"'):
        return s[1:-1]
    else :
        return s

def helper(s):
    s = str(s)
    if(s[0]=='0'):
        return s[1:]
    else:
        return s

def spliteremail(s):
    if(s==None):
        return "",""
    idx = s.find('<')
    if(idx == -1):
        return s,s
    lgth = len(s)
    # print(s)
    x_name = s[:idx-1]
    if s[:-1].isalpha():
        y_email = s[idx+1:]
        
    else:
        y_email = s[idx+1:-1]
    # print (y_email)
    # print("-"*50)
    return x_name,y_email

def func(s):
    if(s[:2].isdigit()):
        x = s[:2]
        y = s[2:]
    else:
        x=s[:1]
        y=s[1:]

    # print(x)
    # print(y)
    return x,y

def spliterdate(s):
    if s == None:
        return "0"
    day = s[5:11]
    final = day
    monthdate = day.replace(" ","")
    curr = datetime.datetime.now()

    date,day = func(monthdate)

    date = helper(date)
    day = mth.index(day) + 1
    tdate = helper(curr.day)
    tmonth = helper(curr.month)

    if(date == tdate and day==tmonth):
        return "today"
    else:
        s = date +" "+ mth[day-1]
        return s
    
def bunny(request):
    context ={}
    if request.method == "POST":
        # file = request.FILES['filenameupload'] 
        sender_msg = request.POST.get('smsg')
        reciever = request.POST.get('recv')
        Bcc = request.POST.get('recvBcc')
        Cc = request.POST.get('recvCc')
        sub = request.POST.get('ssub')
        # att = request.POST.get('filenameupload')
        sender = "anish@bimaxpress.com"
        # print(len(file))
        
        sendemail(sender, reciever, sub, sender_msg,Bcc, Cc,)
    # print(data)    

    imap_server = imaplib.IMAP4_SSL(host='mail.bimaxpress.com')
    imap_server.login("anish@bimaxpress.com","abcd1234")
    imap_server.select()  # Default is `INBOX`
    count = 0
    # Find all emails in inbox
    _, message_numbers_raw = imap_server.search(None, 'ALL')

    message = []
    count = 0
    for message_number in message_numbers_raw[0].split():
        _, msg = imap_server.fetch(message_number, '(RFC822)')

        # Parse the raw email message in to a convenient object
        x = email.message_from_bytes(msg[0][1])
        nameid, emailid = spliteremail(x['from'])
        time = spliterdate(x['date'])
        # print("========email start===========")
        # print(x)
        # print("========email end===========")
        newtext=""
        for part in x.walk():
            if (part.get('Content-Disposition') and part.get('Content-Disposition').startswith("attachment")):

                part.set_type("text/plain")
                part.set_payload('Attachment removed: %s (%s, %d bytes)'
                        %(part.get_filename(), 
                        part.get_content_type(), 
                        len(part.get_payload(decode=True))))
                del part["Content-Disposition"]
                del part["Content-Transfer-Encoding"]
            print("part print")
            print(part)
            if part.get_content_type().startswith("text/plain"):
                newtext += "\n"
                newtext += part.get_payload(decode=False)

        # newtext.replace('"',"\'" )
        # newtext.replace("'","\'")
        # newtext = escape(newtext)
        # print(newtext)
        msg_json = {
            # "from" : x['from'],
            "from": escape( emailid),
            "name": escape(optimiser(nameid)),
            "to": escape(x['to']),
            "subject": escape(x['subject']),
            # "name": x['name'],
            # "name": spliter1(x['from']),
            # "emailaddr": spliter2(x['from']),
            "message":escape(newtext),
            "date": escape(time),
            "id":count,
        }
        # print(newtext)
        count +=1
        message.append(msg_json)


    email_message = json.dumps(message)
    # print(email_message)s
    a=eval(email_message)
    # print(a)
    from_list=[]
    to_list=[]
    sub_list=[]
    date_list=[]
    l=[]
    time_list=[]
    

    for i in reversed(range(len(a))):
        
        print("+++++++++++")
        l.append(a[i])
        from_list.append(a[i]['from'])
        to_list.append(a[i]['to'])
        sub_list.append(a[i]['subject'])
        date_list.append(a[i]['date'])
    
    # print(l)
    context['data_from'] = from_list
    context['data_to'] = to_list
    context['data_sub'] = sub_list
    context['data_date'] = date_list
    context['data'] = l
    
    return render(request,"baseemail.html",context)

def replymail(request):
    context ={}
    # print(request.method)
    if request.method == "POST":
        # file = request.FILES['filenameupload'] 
        
        sender_msg = request.POST.get('rep_smsg')
        reciever = request.POST.get('rep_recv')
        
        Bcc = request.POST.get('rep_recvBcc')
        Cc = request.POST.get('rep_recvCc')
        sub = request.POST.get('rep_ssub')
        m_id = request.POST.get('rep_id')
        # att = request.POST.get('filenameupload')
        sender = "anish@bimaxpress.com"

        imap_server = imaplib.IMAP4_SSL(host='mail.bimaxpress.com')
        imap_server.login("anish@bimaxpress.com","abcd1234")
        imap_server.select()
        
        _, msg = imap_server.fetch(m_id, '(RFC822)')
        email_msg = email.message_from_bytes(msg[0][1])
        
        newtext=""

    
    
        new = EmailMultiAlternatives("Re: "+email_msg["Subject"],
                             sender_msg, 
                             sender, # from
                             [email_msg["Reply-To"] or email_msg["From"]], # to
                             headers = {'Reply-To': sender,
                                        "In-Reply-To":email_msg["Message-ID"],
                                        "References":email_msg["Message-ID"]})
        # new.attach_alternative(sender_msg, "text/plain")
        new.attach( MIMEMessage(email_msg) )
        # print(new.body) # attach original message
        new.send()
        next = request.POST.get('next', '/')
    return HttpResponseRedirect(next)
    # return render(request,"baseemail.html",context)



def create(request):
    if request.method == 'POST':
        to = request.POST['to']
        subject = request.POST['subject']
        message = request.POST['message']
        new_email = Email(to=to, subject=subject,message=message)
        new_email.save()
        # print(new_email)
        success = 'Mail sent' + to + 'successfully'
        return HttpResponse(success)
    
   

def sendemail(sender, reciever, sub, sender_msg, Bcc, Cc):
    email = EmailMultiAlternatives(sub, sender_msg, sender, [reciever,], bcc = [Bcc,], cc = [Cc,], reply_to=["cse180001006@iiti.ac.in",]) 
    print(email.message())
    text = str(email.message())
    imap_server = imaplib.IMAP4_SSL(host='mail.bimaxpress.com',port=993)
    imap_server.login("anish@bimaxpress.com","abcd1234")
    imap_server.append('INBOX.Sent', '\\Seen', imaplib.Time2Internaldate(time.time()), text.encode('utf8'))

    email.send()
    # print("EMAIL SENT")


def sentmail(request):
    context ={}
    if request.method == "POST":
        # file = request.FILES['filenameupload'] 
        sender_msg = request.POST.get('smsg')
        reciever = request.POST.get('recv')
        Bcc = request.POST.get('recvBcc')
        Cc = request.POST.get('recvCc')
        sub = request.POST.get('ssub')
        # att = request.POST.get('filenameupload')
        sender = "anish@bimaxpress.com"
        # print(len(file))
        sendemail(sender, reciever, sub, sender_msg,Bcc, Cc,)
    # print(data)    

    imap_server = imaplib.IMAP4_SSL(host='mail.bimaxpress.com')
    imap_server.login("anish@bimaxpress.com","abcd1234")
    imap_server.select('INBOX.Sent')  #sent folder selected
    count = 0
    # Find all emails in inbox
    _, message_numbers_raw = imap_server.search(None, 'ALL')

    message = []
    count = 0
    for message_number in message_numbers_raw[0].split():
        _, msg = imap_server.fetch(message_number, '(RFC822)')

        # Parse the raw email message in to a convenient object
        x = email.message_from_bytes(msg[0][1])
        # print(x['from'])
        nameid, emailid = spliteremail(x['from'])
        time = spliterdate(x['date'])
        to=""
        ssub=""
        mssg=""
        if(x['to']!=None):
            to=x['to']

        if(x['subject']!=None):
            ssub = x['subject']

        if(x['message']!=None):
            mssg = x['message']

        newtext=""
        for part in x.walk():
            if (part.get('Content-Disposition') and part.get('Content-Disposition').startswith("attachment")):

                part.set_type("text/plain")
                part.set_payload('Attachment removed: %s (%s, %d bytes)'
                        %(part.get_filename(), 
                        part.get_content_type(), 
                        len(part.get_payload(decode=True))))
                del part["Content-Disposition"]
                del part["Content-Transfer-Encoding"]

            if part.get_content_type().startswith("text/plain"):
                newtext += "\n"
                newtext += part.get_payload(decode=False)

        
        msg_json = {
            "from": emailid,
            "name": nameid,
            "to": to,
            "subject": ssub,
            "date": time,
            "id":count,
            "message":newtext,
        }
        
        if(emailid):
            count +=1
            message.append(msg_json)
            

    imap_server.close() 
    imap_server.logout()
    


    email_message = json.dumps(message)
    print(email_message)
    
    a=eval(email_message)
    from_list=[]
    to_list=[]
    sub_list=[]
    date_list=[]
    l=[]
    time_list=[]
    

    for i in reversed(range(len(a))):
        # print(a[i]['from'])
        # print(a[i]['message'])
        l.append(a[i])
        from_list.append(a[i]['from'])
        to_list.append(a[i]['to'])
        sub_list.append(a[i]['subject'])
        date_list.append(a[i]['date'])
    
    # print(l)
    context['data_from'] = from_list
    context['data_to'] = to_list
    context['data_sub'] = sub_list
    context['data_date'] = date_list
    context['data'] = l
    
    return render(request,"sentemail.html",context)

#TRASH Folder
def trashmail(request):
    context ={}
    if request.method == "POST":
        # file = request.FILES['filenameupload'] 
        sender_msg = request.POST.get('smsg')
        reciever = request.POST.get('recv')
        Bcc = request.POST.get('recvBcc')
        Cc = request.POST.get('recvCc')
        sub = request.POST.get('ssub')
        # att = request.POST.get('filenameupload')
        sender = "anish@bimaxpress.com"
        # print(len(file))
        sendemail(sender, reciever, sub, sender_msg,Bcc, Cc,)
    # print(data)    

    imap_server = imaplib.IMAP4_SSL(host='mail.bimaxpress.com')
    imap_server.login("anish@bimaxpress.com","abcd1234")
    imap_server.select('INBOX.Trash')  # Default is `INBOX`
    count = 0
    # Find all emails in inbox
    _, message_numbers_raw = imap_server.search(None, 'ALL')

    message = []
    count = 0
    for message_number in message_numbers_raw[0].split():
        _, msg = imap_server.fetch(message_number, '(RFC822)')

        # Parse the raw email message in to a convenient object
        x = email.message_from_bytes(msg[0][1])
        nameid, emailid = spliteremail(x['from'])
        time = spliterdate(x['date'])

        newtext=""
        for part in x.walk():
            if (part.get('Content-Disposition') and part.get('Content-Disposition').startswith("attachment")):

                part.set_type("text/plain")
                part.set_payload('Attachment removed: %s (%s, %d bytes)'
                        %(part.get_filename(), 
                        part.get_content_type(), 
                        len(part.get_payload(decode=True))))
                del part["Content-Disposition"]
                del part["Content-Transfer-Encoding"]

            if part.get_content_type().startswith("text/plain"):
                newtext += "\n"
                newtext += part.get_payload(decode=False)


        msg_json = {
            "from": emailid,
            "name": nameid,
            "to": x['to'],
            "subject": x['subject'],
            "date": time,
            "id":count,
            "message":newtext,
        }
        count +=1
        message.append(msg_json)

    email_message = json.dumps(message)
    # print(email_message)s
    a=eval(email_message)
    from_list=[]
    to_list=[]
    sub_list=[]
    date_list=[]
    l=[]
    time_list=[]
    

    for i in reversed(range(len(a))):
        # print(a[i]['from'])
        l.append(a[i])
        from_list.append(a[i]['from'])
        to_list.append(a[i]['to'])
        sub_list.append(a[i]['subject'])
        date_list.append(a[i]['date'])
    
    # print(l)
    context['data_from'] = from_list
    context['data_to'] = to_list
    context['data_sub'] = sub_list
    context['data_date'] = date_list
    context['data'] = l
    
    return render(request,"trash.html",context)

#DRAFTS Folder
def draftmail(request):
    context ={}
    if request.method == "POST":
        # file = request.FILES['filenameupload'] 
        sender_msg = request.POST.get('smsg')
        reciever = request.POST.get('recv')
        Bcc = request.POST.get('recvBcc')
        Cc = request.POST.get('recvCc')
        sub = request.POST.get('ssub')
        # att = request.POST.get('filenameupload')
        sender = "anish@bimaxpress.com"
        # print(len(file))
        sendemail(sender, reciever, sub, sender_msg,Bcc, Cc,)
    # print(data)    

    imap_server = imaplib.IMAP4_SSL(host='mail.bimaxpress.com')
    imap_server.login("anish@bimaxpress.com","abcd1234")
    imap_server.select('INBOX.Sent')  # Default is `INBOX`
    count = 0
    # Find all emails in inbox
    _, message_numbers_raw = imap_server.search(None, 'ALL')

    message = []
    count = 0
    for message_number in message_numbers_raw[0].split():
        _, msg = imap_server.fetch(message_number, '(RFC822)')

        # Parse the raw email message in to a convenient object
        x = email.message_from_bytes(msg[0][1])
        nameid, emailid = spliteremail(x['from'])
        time = spliterdate(x['date'])


        newtext=""
        for part in x.walk():
            if (part.get('Content-Disposition') and part.get('Content-Disposition').startswith("attachment")):

                part.set_type("text/plain")
                part.set_payload('Attachment removed: %s (%s, %d bytes)'
                        %(part.get_filename(), 
                        part.get_content_type(), 
                        len(part.get_payload(decode=True))))
                del part["Content-Disposition"]
                del part["Content-Transfer-Encoding"]

            if part.get_content_type().startswith("text/plain"):
                newtext += "\n"
                newtext += part.get_payload(decode=False)


        msg_json = {
            "from": emailid,
            "name": nameid,
            "to": x['to'],
            "subject": x['subject'],
            "date": time,
            "id":count,
            "message":newtext,
        }
        count +=1
        message.append(msg_json)

    email_message = json.dumps(message)
    # print(email_message)s
    a=eval(email_message)
    from_list=[]
    to_list=[]
    sub_list=[]
    date_list=[]
    l=[]
    time_list=[]
    

    for i in reversed(range(len(a))):
        # print(a[i]['from'])
        l.append(a[i])
        from_list.append(a[i]['from'])
        to_list.append(a[i]['to'])
        sub_list.append(a[i]['subject'])
        date_list.append(a[i]['date'])
    
    # print(l)
    context['data_from'] = from_list
    context['data_to'] = to_list
    context['data_sub'] = sub_list
    context['data_date'] = date_list
    context['data'] = l
    
    return render(request,"drafts.html",context)

#Starred Folder
def starredemail(request):
    context ={}
    if request.method == "POST":
        # file = request.FILES['filenameupload'] 
        sender_msg = request.POST.get('smsg')
        reciever = request.POST.get('recv')
        Bcc = request.POST.get('recvBcc')
        Cc = request.POST.get('recvCc')
        sub = request.POST.get('ssub')
        # att = request.POST.get('filenameupload')
        sender = "anish@bimaxpress.com"
        # print(len(file))
        sendemail(sender, reciever, sub, sender_msg,Bcc, Cc,)
    # print(data)    

    imap_server = imaplib.IMAP4_SSL(host='mail.bimaxpress.com')
    imap_server.login("anish@bimaxpress.com","abcd1234")
    imap_server.select('INBOX')  # Default is `INBOX`
    count = 0
    # Find all emails in inbox
    _, message_numbers_raw = imap_server.search(None, 'ALL')

    message = []
    count = 0
    for message_number in message_numbers_raw[0].split():
        _, msg = imap_server.fetch(message_number, '(RFC822)')

        # Parse the raw email message in to a convenient object
        x = email.message_from_bytes(msg[0][1])
        nameid, emailid = spliteremail(x['from'])
        time = spliterdate(x['date'])


        newtext=""
        for part in x.walk():
            if (part.get('Content-Disposition') and part.get('Content-Disposition').startswith("attachment")):

                part.set_type("text/plain")
                part.set_payload('Attachment removed: %s (%s, %d bytes)'
                        %(part.get_filename(), 
                        part.get_content_type(), 
                        len(part.get_payload(decode=True))))
                del part["Content-Disposition"]
                del part["Content-Transfer-Encoding"]

            if part.get_content_type().startswith("text/plain"):
                newtext += "\n"
                newtext += part.get_payload(decode=False)


        msg_json = {
            "from": emailid,
            "name": nameid,
            "to": x['to'],
            "subject": x['subject'],
            "date": time,
            "id":count,
            "message":newtext,
        }
        count +=1
        message.append(msg_json)

    email_message = json.dumps(message)
    # print(email_message)s
    a=eval(email_message)
    from_list=[]
    to_list=[]
    sub_list=[]
    date_list=[]
    l=[]
    time_list=[]
    

    for i in reversed(range(len(a))):
        # print(a[i]['from'])
        l.append(a[i])
        from_list.append(a[i]['from'])
        to_list.append(a[i]['to'])
        sub_list.append(a[i]['subject'])
        date_list.append(a[i]['date'])
    
    # print(l)
    context['data_from'] = from_list
    context['data_to'] = to_list
    context['data_sub'] = sub_list
    context['data_date'] = date_list
    context['data'] = l
    
    return render(request,"starred.html",context) 