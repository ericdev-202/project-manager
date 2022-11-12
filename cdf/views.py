from django.shortcuts import render

# Create your views here.
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render,redirect
from django.contrib.gis.geos import Point
from django.core.serializers import serialize
from cdf import models as cdf_models
from cdf import forms as cdf_forms
from cdf.models import Suggestions,Report,SecurityEvent,CdfProjects,Comment
from django.utils import timezone
from django.http import HttpResponse,JsonResponse
from cdf import Serializers as c_serializers
from rest_framework import generics
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from collections import Counter
import simplejson
import pandas
from django.db.models import Count, Q
from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from django.db.models import Q

from .forms import LoginForm,EngineerActiveForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from  django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from .models import Engineer,Contractor



def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'login/index.html')


#for showing signup/login button for customer
def contractorclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'login/contractorclick.html')

#for showing signup/login button for mechanics
def engineerclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'login/engineerclick.html')


#for showing signup/login button for ADMIN(by sumit)
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')



def contractor_signup_view(request):
    userForm=forms.ContractorUserForm()
    contractorForm=forms.ContractorForm()
    mydict={'userForm':userForm,'contractorForm':contractorForm}
    if request.method=='POST':
        userForm=forms.ContractorUserForm(request.POST)
        contractorForm=forms.ContractorForm(request.POST,request.FILES)
        if userForm.is_valid() and contractorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            contractor=contractorForm.save(commit=False)
            contractor.user=user
            contractor.save()
            my_contractor_group = Group.objects.get_or_create(name='CONTRACTOR')
            my_contractor_group[0].user_set.add(user)
        return HttpResponseRedirect('contractor-view')
    return render(request,'login/contractorsignup.html',context=mydict)


def engineer_signup_view(request):
    userForm=forms.EngineerUserForm()
    engineerForm=forms.EngineerForm()
    mydict={'userForm':userForm,'engineerForm':engineerForm}
    if request.method=='POST':
        userForm=forms.EngineerUserForm(request.POST)
        engineerForm=forms.EngineerForm(request.POST,request.FILES)
        if userForm.is_valid() and engineerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            engineer=engineerForm.save(commit=False)
            engineer.user=user
            engineer.save()
            my_engineer_group = Group.objects.get_or_create(name='ENGINEER')
            my_engineer_group[0].user_set.add(user)
        return HttpResponseRedirect('admin-view-engineer')
    return render(request,'login/engineersignup.html',context=mydict)

def admin_signup_view(request):
    userForm=forms.AdminUserForm()
    adminForm=forms.AdminForm()
    mydict={'userForm':userForm,'adminForm':adminForm}
    if request.method=='POST':
        userForm=forms.AdminUserForm(request.POST)
        adminForm=forms.AdminForm(request.POST,request.FILES)
        if userForm.is_valid() and adminForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            admin=adminForm.save(commit=False)
            admin.user=user
            admin.save()
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)
        return HttpResponseRedirect('adminlogin')
    return render(request,'login/adminsignup.html',context=mydict)


#for checking user customer, mechanic or admin(by sumit)
def is_contractor(user):
    return user.groups.filter(name='CONTRACTOR').exists()
def is_engineer(user):
    return user.groups.filter(name='ENGINEER').exists()

def is_admin(user):
	return user.groups.filter(name='ADMIN').exists()


def afterlogin_view(request):
    if is_contractor(request.user):
        return redirect('contractor-dash')
    elif is_engineer(request.user):
        return redirect('engineer')
    else:
        return redirect('admin-dashboard')



def admin_dashboard_view(request):
	return render(request,'Admin/base.html')


# def contdashboard(request):
	# return render(request,'Contractor/index.html')

def engineer(request):	
	return render(request,'Engineer/engineerdash.html')





















def bufferPoints(request):
	bufferingpoints = []
	data = cdf_models.CdfProjects.objects.all()
	for p in data:
		bufferingpoints.append(tuple((p.lat,p.lon)))
	serializedpoints = list(bufferingpoints)
	# serializedpoints = serialize('geojson',serializedpoints)
	return JsonResponse(serializedpoints, safe=False)
def commentjson(request):
	relatedproject = []
	data = cdf_models.Comment.objects.all()
	p = cdf_models.Comment.objects.all().values()
	q = []
	counts = []
	latitudes = []
	longitude = []
	for w in p:
		q.append(w['post_id'])

	incidents_count = Counter(q)
	for x in incidents_count:
		counts.append(incidents_count[x])
	for r in data:
		latitudes.append(r.post.lat)

	for r in data:
		longitude.append(r.post.lon)

	for c,m,n in zip(counts,latitudes,longitude):
		relatedproject.append(tuple((m,n,c)))
	
	return JsonResponse(relatedproject, safe=False)


###puplic use
	
def home(request):
	dict={
    'total_complete':CdfProjects.objects.filter(status="Complete").count(),
    'total_onprogress':CdfProjects.objects.filter(status="Onprogress").count(),
    'total_incomplete':CdfProjects.objects.filter(status="Incomplete").count(),
    'total_delayed':CdfProjects.objects.filter(status="Stopped").count(),
    'projects':CdfProjects.objects.all(),
    }
	return render(request,'temps/dashboard.html',context=dict)

def all_projects(request):
	projects = CdfProjects.objects.all()
	return render(request,'temps/allprojectdetails.html',{'projects':projects})


def ContactPage(request):
	return render(request,'temps/contact.html')
def AboutPage(request):
	return render(request,'temps/about.html')
def projectsview(request):
	IGC = []
	IGS = []
	IGN = []
	NI = []
	CI = []
	SI = []
	BU = []
	TE = []
	TW =[]
	# sectors
	Education = []
	Security = []
	Health = []
	Administration = []
	Water = []
	Sports = []
	Environment = []
	projects = cdf_models.CdfProjects.objects.all()
	# Pagination

	paginator = Paginator(projects,4)
	page = request.GET.get('page')
	# End Pagination

	for m in projects:
		if m.location == 'Igembe Central':
			IGC.append(m.amount)
		elif m.location == 'Igembe South':
			IGS.append(m.amount)
		elif m.location == 'Igembe North':
			IGN.append(m.amount)
		elif m.location == 'North Imenti':
			NI.append(m.amount)
		elif m.location == 'Cental Imenti':
			CI.append(m.amount)
		elif m.location == 'South Imenti':
			SI.append(m.amount)
		elif m.location == 'Buuri':	
			BU.append(m.amount)
		elif m.location == 'Tigania East':	
			TE.append(m.amount)
		elif m.location == 'Tigania West':	
			TW.append(m.amount)
		else:
			print('No location')

	for s in projects:
		if s.sectors == 'Education':
			Education.append(s.amount)
		elif s.sectors == 'Security':
			Security.append(s.amount)
		elif s.sectors == 'Health':
			Health.append(s.amount)
		elif s.sectors == 'Administration':
			Administration.append(s.amount)
		elif s.sectors == 'Water':
			Water.append(s.amount)
		elif s.sectors == 'Sports':
			Sports.append(s.amount)
		elif s.sectors == 'Enviroment':
			Environment.append(s.amount)

	# Sectors
	eamount = sum(Education)
	samount = sum(Security)
	hamount = sum(Health)
	aamount = sum(Administration)
	wamount = sum(Water)
	samount = sum(Sports)
	evamount = sum(Environment)
	# Wards
	IGCamount = sum(IGC)
	IGSamount = sum(IGS)
	IGNamount = sum(IGN)
	NIamount = sum(NI)
	CIamount = sum(CI)
	SIamount = sum(SI)
	BUamount = sum(BU)
	TEamount = sum(TE)
	TWamount = sum(TW)
	print(NIamount)
	query = request.GET.get('q')
	if query:
		projects = projects.filter(project__iexact=query) or projects.filter(sectors__iexact=query)
		paginator = Paginator(projects,4)
		page = request.GET.get('page')

	try:
		reports = paginator.page(page)
	except PageNotAnInteger:
		reports = paginator.page(1)
	except EmptyPage:
		reports = paginator.page(paginator.num_pages)
	index = reports.number - 1
	max_index = len(paginator.page_range)
	start_index = index - 5 if index >= 5 else 0
	end_index = index + 5 if index <= max_index - 5 else max_index
	page_range = paginator.page_range[start_index:end_index]
	return render(request,'temps/projects.html',
		{
			# 'saf':projects,
			'IGC':IGCamount,
			'IGS':IGSamount,
			'IGN':IGNamount,
			'NI':NIamount,
			'CI':CIamount,
			'SI':SIamount,
			'BU':BUamount,
			'TE':TEamount,
			'TW':TWamount,

			'edu':eamount,
			'sec':samount,
			'hea':hamount,
			'admi':aamount,
			'wtr':wamount,
			'sprt':samount,
			'env':evamount,

			'reports':reports,
			'page_range':page_range,
		})
def projectdetail(request,pk):
	proj = cdf_models.CdfProjects.objects.get(pk=pk)
	return render(request,'temps/projdetail.html',{'projd':proj})

def add_comment_to_post(request, pk):
    post = get_object_or_404(cdf_models.CdfProjects, pk=pk)
    if request.method == "POST":
        form = cdf_forms.CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('details', pk=post.pk)
    else:
        form = cdf_forms.CommentForm()
    return render(request, 'temps/add_comment_to_post.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('details', pk=comment.post.pk) 

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('details', pk=comment.post.pk)

def suggestionview(request):
	form_class = cdf_forms.SuggestionForm
	if request.method == 'POST':
		form = form_class(data=request.POST)
		if form.is_valid():
			NewSuggestion = Suggestions()
			NewSuggestion.suggestion = request.POST.get('suggestion')
			NewSuggestion.body = request.POST.get('body')
			NewSuggestion.status = request.POST.get('status')
			NewSuggestion.name = request.POST.get('name')
			NewSuggestion.email = request.POST.get('email')
			NewSuggestion.created = timezone.now()
			NewSuggestion.save()
			return redirect('home')
		else:
			form = form_class
	return render(request,'temps/suggestion.html',{'sugg':form_class})


def ReportView(request):
	if request.method == 'POST':
		description = request.POST.get('description')
		opinion = request.POST.get('opinion')
		images = request.FILES.getlist('images')
		coordinate_p = request.POST.get('coordinates').split(',')
		geom = {
		"type":"Point",
		"coordinates":[float(coordinate_p[0]),float(coordinate_p[1])]
		}

		for image in images:
			report = Report.objects.create(
				description=description,
				opinion=opinion,
				image=image,
				geom=geom,
				)
		return redirect('home')
	return render(request,'temps/report.html')	


def ReporView(request):
	form_class = cdf_forms.SecurityReportForm
	if request.method == 'POST':
		form = form_class(request.POST,request.FILES)
		if form.is_valid():
			NewReport = Report()
			NewReport.description = request.POST.get('description')
			NewReport.opinion = request.POST.get('opinion')
			# NewReport.image = request.FILES.get('image')
			# coordinate_p = request.POST.get('coordinates').split(',')
			# NewReport.geom = {
		 #        "type": "Point",
		 #        "coordinates": [float(coordinate_p[0]), float(coordinate_p[1])] 
		 #    }
			NewReport.created = timezone.now()
			NewReport.save() 
			return redirect('home')
		else:
			form = form_class
	return render(request,'temps/report.html',{'reports':form_class})


def ReportDisplay(request):
	incidents = cdf_models.Report.objects.all()
	paginator = Paginator(incidents,2)
	page = request.GET.get('page')
	query = request.GET.get('q')
	if query:
		incidents = incidents.filter(opinion__icontains=query)
		paginator = Paginator(incidents,2)
		page = request.GET.get('page')
	try:
		reports = paginator.page(page)
	except PageNotAnInteger:
		reports = paginator.page(1)
	except EmptyPage:
		reports = paginator.page(paginator.num_pages)
	index = reports.number - 1
	max_index = len(paginator.page_range)
	start_index = index - 5 if index >= 5 else 0
	end_index = index + 5 if index <= max_index - 5 else max_index
	page_range = paginator.page_range[start_index:end_index]
	return render(request,'Admin/reported_incidences.html',
		{
			'reports':reports,
			'page_range':page_range,
		})

def Incidence_json(request):
	data = serialize('geojson',cdf_models.Report.objects.all())
	return HttpResponse(data, content_type='json')
def Projects_json(request):
	data = serialize('geojson',cdf_models.CdfProjects.objects.all())
	return HttpResponse(data, content_type='json')

def ConstBoundary(request):
	data = serialize('geojson',cdf_models.Boundary.objects.all())
	return HttpResponse(data, content_type='json')

def EventView(request):
	form_class = cdf_forms.SecurityEventForm

	if request.method == 'POST':
		
		form = form_class(data=request.POST)
		if form.is_valid():
			form.save()
		else:
			form = form_class

	return render(request,'temps/event.html',{'events':form_class})

def EventDisplay(request):
	eventss = cdf_models.SecurityEvent.objects.all()
	return render(request,'temps/event.html',{'eventss':eventss})

def Events_json(request):
	data = serialize('geojson',cdf_models.SecurityEvent.objects.all())
	return HttpResponse(data, content_type='json')

def ActivityData(request):
	form_class = cdf_forms.SecurityEventForm
	if request.method == 'POST':
		form = form_class(data=request.POST)
		if form.is_valid():
			NewEvent = SecurityEvent()
			NewEvent.description = request.POST.get('description')
			NewEvent.title = request.POST.get('title')
			NewEvent.mdate = request.POST.get('mdate')
			NewEvent.mtime = request.POST.get('mtime')
			coordinate_p = request.POST.get('coordinates').split(',')
			NewEvent.venue = {
		        "type": "Point",
		        "coordinates": [float(coordinate_p[0]), float(coordinate_p[1])] 
		    }
			NewEvent.created = timezone.now()
			NewEvent.save() 
			return redirect('home')
		else:
			form = form_class
	return render(request,'temps/activities.html',{'form':form_class})

def ContactU(request):
	form_class = cdf_forms.ContactUsForm
	if request.method == 'POST':
		fullname = request.POST.get('fullname')
		email = request.POST.get('email')
		phonenumber = request.POST.get('phonenumber')
		body = request.POST.get('info')
		created = timezone.now()
		feedback = cdf_models.ContactUs.objects.create(fullname=fullname,
				email=email,
				phonenumber=phonenumber,
				body=body,
				created=created)
		feedback.save()
		return JsonResponse({'data':'Your Information has been received, Thank you for your contribution'})
	return JsonResponse({'data':'Fill The forms'})

# Serialization 

class ListCreateProjects(generics.ListCreateAPIView):
    queryset = CdfProjects.objects.all()
    serializer_class = c_serializers.ProjectSerializer

class ListCreateComment(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = c_serializers.CommentSerializer







def deleteproject(request):
    id = request.GET.get('id',None)
    CdfProjects.objects.get(id=id).delete()
    response_data = {
        'deleted':True
    }
    return JsonResponse(response_data)

### ADMIN VIEWS
def admin_dashboard(request):
	user = request.user
	dict={
    'total_projects':CdfProjects.objects.filter(project_manager__user=user).count(),
    'total_onprogress':CdfProjects.objects.filter(status="Onprogress",project_manager__user=user).count(),
    'total_incomplete':CdfProjects.objects.filter(status="Incomplete",project_manager__user=user).count(),
    'total_complete':CdfProjects.objects.filter(status="Complete",project_manager__user=user).count(),
    'projects':CdfProjects.objects.filter(project_manager__user=user),
    }
	return render(request,'Admin/dashboard.html',context=dict)


###project manager creates project views
def admin_projectdetails(request):
	user = request.user
	projects = Manager.objects.filter(user=user)

	form =forms.AdminRequestForm()
	mydict={'form':form,'projects':projects}
	if request.method == 'POST':
		descrition = request.POST.get('descrition')
		project_manager = request.POST.get('project_manager')
		project = request.POST.get('project')
		# image = request.FILES.get('image')
		# phases = request.POST.get('phases')
		sectors = request.POST.get('sectors')
		# image = request.FILES.get('image')
		amount = request.POST.get('amount')
		# status = request.POST.get('status')
		county_nam = request.POST.get('county_nam')
		location = request.POST.get('location')
		project_eng = request.POST.get('project_eng')
		project_cont = request.POST.get('project_cont')
		startdate = request.POST.get('startdate')
		propdate = request.POST.get('propdate')
		lat = request.POST.get('lat')
		lon = request.POST.get('lon')
		# image = request.FILES.get('image')
		coordinate_p = request.POST.get('coordinates').split(',')
		geom = {
		"type":"Point",
		"coordinates":[float(coordinate_p[0]),float(coordinate_p[1])]
		}

		data = request.POST
		if data['project_manager'] != 'none':
			project_manager = Manager.objects.get(id=data['project_manager'])
		else:
			project_manager = None

		form = forms.AdminRequestForm(request.POST)
		if form.is_valid():
			# enquiry_x=adminenquiry.save(commit=False)
			project_eng=form.cleaned_data['project_eng']
			project_cont=form.cleaned_data['project_cont']
			# form.save()
			project_eng.save()
			project_cont.save()
		else:
			print("form is invalid")

		report = CdfProjects.objects.create(
			project_manager=project_manager,
			descrition=descrition,
			project = project,
			# phases=phases,
			sectors=sectors,
			amount=amount,
			# status=status,
			county_nam=county_nam,
			location=location,
			project_eng=project_eng,
			project_cont=project_cont,
			startdate = startdate,
			propdate = propdate,
			lat=lat,
			lon=lon,
			geom=geom,
			)
		return redirect('admin-dashboard')
	return render(request,'Admin/projectdetails.html',context=mydict)

###project manager view project
def admin_projectsview(request):
	user = request.user
	IGC = []
	IGS = []
	IGN = []
	NI = []
	CI = []
	SI = []
	BU = []
	TE = []
	TW =[]
	# sectors
	Education = []
	Security = []
	Health = []
	Administration = []
	Water = []
	Sports = []
	Environment = []
	projects = cdf_models.CdfProjects.objects.filter(project_manager__user=user)
	# Pagination

	paginator = Paginator(projects,4)
	page = request.GET.get('page')
	# End Pagination

	for m in projects:
		if m.location == 'Igembe Central':
			IGC.append(m.amount)
		elif m.location == 'Igembe South':
			IGS.append(m.amount)
		elif m.location == 'Igembe North':
			IGN.append(m.amount)
		elif m.location == 'North Imenti':
			NI.append(m.amount)
		elif m.location == 'Cental Imenti':
			CI.append(m.amount)
		elif m.location == 'South Imenti':
			SI.append(m.amount)
		elif m.location == 'Buuri':	
			BU.append(m.amount)
		elif m.location == 'Tigania East':	
			TE.append(m.amount)
		elif m.location == 'Tigania West':	
			TW.append(m.amount)
		else:
			print('No location')

	for s in projects:
		if s.sectors == 'Education':
			Education.append(s.amount)
		elif s.sectors == 'Security':
			Security.append(s.amount)
		elif s.sectors == 'Health':
			Health.append(s.amount)
		elif s.sectors == 'Administration':
			Administration.append(s.amount)
		elif s.sectors == 'Water':
			Water.append(s.amount)
		elif s.sectors == 'Sports':
			Sports.append(s.amount)
		elif s.sectors == 'Enviroment':
			Environment.append(s.amount)

	# Sectors
	eamount = sum(Education)
	samount = sum(Security)
	hamount = sum(Health)
	aamount = sum(Administration)
	wamount = sum(Water)
	samount = sum(Sports)
	evamount = sum(Environment)
	# Wards
	IGCamount = sum(IGC)
	IGSamount = sum(IGS)
	IGNamount = sum(IGN)
	NIamount = sum(NI)
	CIamount = sum(CI)
	SIamount = sum(SI)
	BUamount = sum(BU)
	TEamount = sum(TE)
	TWamount = sum(TW)
	print(NIamount)
	query = request.GET.get('q')
	if query:
		projects = projects.filter(project__iexact=query) or projects.filter(sectors__iexact=query)
		paginator = Paginator(projects,4)
		page = request.GET.get('page')

	try:
		reports = paginator.page(page)
	except PageNotAnInteger:
		reports = paginator.page(1)
	except EmptyPage:
		reports = paginator.page(paginator.num_pages)
	index = reports.number - 1
	max_index = len(paginator.page_range)
	start_index = index - 5 if index >= 5 else 0
	end_index = index + 5 if index <= max_index - 5 else max_index
	page_range = paginator.page_range[start_index:end_index]
	return render(request,'Admin/project.html',
		{
			# 'saf':projects,
			'IGC':IGCamount,
			'IGS':IGSamount,
			'IGN':IGNamount,
			'NI':NIamount,
			'CI':CIamount,
			'SI':SIamount,
			'BU':BUamount,
			'TE':TEamount,
			'TW':TWamount,

			'edu':eamount,
			'sec':samount,
			'hea':hamount,
			'admi':aamount,
			'wtr':wamount,
			'sprt':samount,
			'env':evamount,

			'reports':reports,
			'page_range':page_range,
		})



@login_required(login_url='adminlogin')
def admin_engineer_view(request):
    engineer=Engineer.objects.all()
    return render(request,'Admin/engineers.html',{'engineer':engineer})

@login_required(login_url='adminlogin')
def admin_contractor_view(request):
	contractor = Contractor.objects.all()
	return render(request,'Admin/contractor.html',{'contractor':contractor})
 

@login_required(login_url='adminlogin')
def approve_engineer_view(request,pk):
    engineers=forms.EngineerActiveForm()
    if request.method=='POST':
        engineers=forms.EngineerActiveForm(request.POST)
        if engineers.is_valid():
            engineer=Engineer.objects.get(id=pk)
            engineer.salary=engineers.cleaned_data['salary']
            engineer.status=True
            engineer.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-approve-engineer')
    return render(request,'Admin/approve_engi_details.html',{'engineers':engineers})



@login_required(login_url='adminlogin')
def delete_engineer_view(request,pk):
    engineer=Engineer.objects.get(id=pk)
    user=User.objects.get(id=engineer.user_id)
    user.delete()
    engineer.delete()
    return redirect('admin-approve-engineer')


def AdminReportDisplay(request):
	incidents = cdf_models.Report.objects.all()
	paginator = Paginator(incidents,2)
	page = request.GET.get('page')
	query = request.GET.get('q')
	if query:
		incidents = incidents.filter(opinion__icontains=query)
		paginator = Paginator(incidents,2)
		page = request.GET.get('page')
	try:
		reports = paginator.page(page)
	except PageNotAnInteger:
		reports = paginator.page(1)
	except EmptyPage:
		reports = paginator.page(paginator.num_pages)
	index = reports.number - 1
	max_index = len(paginator.page_range)
	start_index = index - 5 if index >= 5 else 0
	end_index = index + 5 if index <= max_index - 5 else max_index
	page_range = paginator.page_range[start_index:end_index]
	return render(request,'Admin/admin_reported_incidence.html',
		{
			'reports':reports,
			'page_range':page_range,
		})


def AdminView_ContractorReport(request):
	enquiry= ContractorDetails.objects.all()
	contractors = []
	for enq in enquiry:
		contractor = CdfProjects.objects.get(project=enq.cdfproject)
		contractors.append(contractor)
	return render(request,'Admin/ContractorReportView.html',{'data':zip(contractors,enquiry)})


def AdminView_EngineerReport(request):
	enquiry= EngineerDetails.objects.all()
	engineers = []
	for enq in enquiry:
		engineer = CdfProjects.objects.get(id=enq.cdfproject_id)
		engineers.append(engineer)
	return render(request,'Admin/EngineerReportView.html',{'data':zip(engineers,enquiry)})

def admin_all_project(request):
	engs = EngineerDetails.objects.all()
	conts = ContractorDetails.objects.all()
	return render(request,'Admin/Proj.html',{'data':zip(conts,engs)})


def ProjectManagerDetails(request):
	cdfs = ProjectManager.objects.all()
	projs = []
	projects = []
	for p in cdfs:
		proj = ContractorDetails.objects.get(id=p.contrdetails_id)
		project = EngineerDetails.objects.get(id=p.engdetails_id)
		projs.append(proj)
		projects.append(project)
		print(p)
	return render(request,'Admin/ProjectManagedetails.html',{'data':zip(projs,projects,cdfs)})	

def Project_manager_progress(request):
	form =forms.AdminReportsForm()
	# form_class=forms.DetailsProjectForm()
	mydict={'form':form}
	if request.method == 'POST':
		# engdetails= request.POST.get('engdetails')
		# contrdetails = request.POST.get('contrdetails')
		proj_report = request.POST.get('proj_report')
		# phases = request.POST.get('phases')
		# progress = request.POST.get('progress')
		proj_approve = request.POST.get('proj_approve')

		form = forms.AdminReportsForm(request.POST)
		# form_class = forms.DetailsProjectForm()
		if form.is_valid():
			contrdetails=form.cleaned_data['contrdetails']
			engdetails = form.cleaned_data['engdetails']
			contrdetails.save()
			engdetails.save()
		# 	form_class.save()
		
		else:
			print("form is invalid")

		report = ProjectManager.objects.create(
			engdetails = engdetails,
			contrdetails = contrdetails,
			proj_report = proj_report,
			# progress=progress,
			# phases = phases,
			proj_approve = proj_approve,
			)
		return redirect('ProjectManagerDetails')
	return render(request,'Admin/ProjectManagerReport.html',mydict)









###contractor
def contractor_dashboard(request):
	user = request.user
	dict={
    'total_complete':CdfProjects.objects.filter(status="Complete",project_cont__user=user).count(),
    'total_onprogress':CdfProjects.objects.filter(status="Onprogress",project_cont__user=user).count(),
    'total_incomplete':CdfProjects.objects.filter(status="Incomplete",project_cont__user=user).count(),
    'total_delayed':CdfProjects.objects.filter(status="Stopped",project_cont__user=user).count(),
    'projects':CdfProjects.objects.filter(project_cont__user=user),
    }
	return render(request,'Contractor/dashboard.html',context=dict)

def assignedprojects(request):
	user = request.user
	cdf = CdfProjects.objects.filter(project_cont__user=user)
	return render(request,'Contractor/assignedproject.html',{'cdf':cdf})


def ViewProjectsAsign(request):
	projs = []
	user = request.user
	oneproject = []
	cdfproject = request.GET.get('cdfproject')
	if cdfproject == None:
		c = ContractorDetails.objects.select_related().filter(cdfproject__project_cont__user=user)
	else:	
		c = ContractorDetails.objects.select_related().filter(cdfproject__project_cont__project=project,cdfproject__project_cont__user=user)
	for l in c:
		projs.append(l.cdfproject.project) 
	keys = set(r for r in projs)	
	cdf = CdfProjects.objects.filter(project_cont__user=user)
	return render(request,'Contractor/contractorview.html',{'cdf':cdf,'c':keys})


@login_required
def ViewProjctsAsign(request):
    projs = []
    user = request.user
    oneproject = []
    c = ContractorDetails.objects.select_related().filter(cdfproject__project_cont__user=user)
    for l in c:
        projs.append(l.cdfproject.project)
    keys = set(r for r in projs)
        
    return render(request,'Contractor/contractorview.html',{'c':keys})


def contractor_all_project(request):
	engs = EngineerDetails.objects.all()
	conts = ContractorDetails.objects.all()
	return render(request,'Contractor/approved_projects.html',{'data':zip(conts,engs)})

def contdashboard(request):
	print('before')
	cdfs = ContractorDetails.objects.all()
	for p in cdfs:
		print(p)
	return render(request,'Contractor/contractordetails.html',{'cdfs':cdfs})	
# def contdashboard(request, project):
# 	user = request.user
# 	cdfproject = request.GET.get('cdfproject')
# 	if cdfproject == None:
# 		cdfs = ContractorDetails.objects.filter(cdfproject__project=project)
# 	else:	
# 		cdfs = ContractorDetails.objects.filter(cdfproject__project_cont__project=project,cdfproject__project_cont__user=user)
# 	cdf = CdfProjects.objects.filter(project_cont__user=user)
# 	return render(request,'Contractor/contractordetails.html',{'cdf':cdf,'cdfs':cdfs})



def editcompany(request, id):
    companydetails = CdfProjects.objects.get(id=id)
    return render(request,'Contractor/updatedetails.html',{'companydetails':companydetails})

def saveassigned(request):
	form =forms.CdfProjectRequestForm()
	# form_class = forms.DetailsContractorForm()
	projects = CdfProjects.objects.all()
	mydict={'form':form,'projects':projects}
	

	if request.method == 'POST':
		cdfproject = request.POST.get('cdfproject')
		contr_report = request.POST.get('contr_report')
		progress = request.POST.get('progress')
		contr_images = request.POST.get('contr_images')
		# contr_images = request.FILES.get('contr_images')
		status = request.POST.get('status')
		phases = request.POST.get('phases')
		finishdate = request.POST.get('finishdate')
		# data = request.POST

		# if data['cdfproject'] != 'none':
		# 	cdfproject = CdfProjects.objects.get(id=data['cdfproject'])
		# else:
		# 	cdfproject = None


		form = forms.CdfProjectRequestForm(request.POST)
		# form_class = forms.DetailsContractorForm(request.POST)
		if form.is_valid():
			cdfproject=form.cleaned_data['cdfproject']
			cdfproject.save()
			# form_class.save()
		
		else:
			print("form is invalid")
		# for contr_images in images:
		report = ContractorDetails.objects.create(
			cdfproject = cdfproject,
			contr_report = contr_report,
			# contr_remark=contr_remark,
			progress = progress,
			contr_images = contr_images,
			status = status,
			phases = phases,
			finishdate = finishdate,
			)
		return redirect('contractor-view-progress')
	return render(request,'Contractor/updatedetails.html',context=mydict)



def showprogress(request):
	labels = []
	data = []
	queryset = ContractorDetails.values('phases').annotate(progress=Sum('progress'))
	for entry in queryset:
		labels.append(entry['phases'])
		data.append(entry['progress'])

	return JsonResponse(data={
        'labels': labels,
        'data': data,
    })


def cont_project(request):
	user = request.user
	IGC = []
	IGS = []
	IGN = []
	NI = []
	CI = []
	SI = []
	BU = []
	TE = []
	TW =[]
	# sectors
	Education = []
	Security = []
	Health = []
	Administration = []
	Water = []
	Sports = []
	Environment = []
	projects = CdfProjects.objects.filter(project_cont__user=user)
	project = ContractorDetails.objects.all()
	# Pagination

	paginator = Paginator(projects,4)
	page = request.GET.get('page')
	# End Pagination

	for m in projects:
		if m.location == 'Igembe Central':
			IGC.append(m.amount)
		elif m.location == 'Igembe South':
			IGS.append(m.amount)
		elif m.location == 'Igembe North':
			IGN.append(m.amount)
		elif m.location == 'North Imenti':
			NI.append(m.amount)
		elif m.location == 'Cental Imenti':
			CI.append(m.amount)
		elif m.location == 'South Imenti':
			SI.append(m.amount)
		elif m.location == 'Buuri':	
			BU.append(m.amount)
		elif m.location == 'Tigania East':	
			TE.append(m.amount)
		elif m.location == 'Tigania West':	
			TW.append(m.amount)
		else:
			print('No location')

	for s in projects:
		if s.sectors == 'Education':
			Education.append(s.amount)
		elif s.sectors == 'Security':
			Security.append(s.amount)
		elif s.sectors == 'Health':
			Health.append(s.amount)
		elif s.sectors == 'Administration':
			Administration.append(s.amount)
		elif s.sectors == 'Water':
			Water.append(s.amount)
		elif s.sectors == 'Sports':
			Sports.append(s.amount)
		elif s.sectors == 'Enviroment':
			Environment.append(s.amount)

	# Sectors
	eamount = sum(Education)
	samount = sum(Security)
	hamount = sum(Health)
	aamount = sum(Administration)
	wamount = sum(Water)
	samount = sum(Sports)
	evamount = sum(Environment)
	# Wards
	IGCamount = sum(IGC)
	IGSamount = sum(IGS)
	IGNamount = sum(IGN)
	NIamount = sum(NI)
	CIamount = sum(CI)
	SIamount = sum(SI)
	BUamount = sum(BU)
	TEamount = sum(TE)
	TWamount = sum(TW)
	print(NIamount)
	query = request.GET.get('q')
	if query:
		projects = projects.filter(project__iexact=query) or projects.filter(sectors__iexact=query)
		paginator = Paginator(projects,4)
		page = request.GET.get('page')

	try:
		reports = paginator.page(page)
	except PageNotAnInteger:
		reports = paginator.page(1)
	except EmptyPage:
		reports = paginator.page(paginator.num_pages)
	index = reports.number - 1
	max_index = len(paginator.page_range)
	start_index = index - 5 if index >= 5 else 0
	end_index = index + 5 if index <= max_index - 5 else max_index
	page_range = paginator.page_range[start_index:end_index]
	return render(request,'Contractor/project.html',
		{
			# 'saf':projects,
			'IGC':IGCamount,
			'IGS':IGSamount,
			'IGN':IGNamount,
			'NI':NIamount,
			'CI':CIamount,
			'SI':SIamount,
			'BU':BUamount,
			'TE':TEamount,
			'TW':TWamount,

			'edu':eamount,
			'sec':samount,
			'hea':hamount,
			'admi':aamount,
			'wtr':wamount,
			'sprt':samount,
			'env':evamount,

			'reports':reports,
			'page_range':page_range,
		})




###engineer
def engineer_dashboard(request):
	user = request.user
	dict={
    'total_complete':CdfProjects.objects.filter(status="Complete",project_eng__user=user).count(),
    'total_onprogress':CdfProjects.objects.filter(status="Onprogress",project_eng__user=user).count(),
    'total_incomplete':CdfProjects.objects.filter(status="Incomplete",project_eng__user=user).count(),
    'total_delayed':CdfProjects.objects.filter(status="Stopped",project_eng__user=user).count(),
    'projects':CdfProjects.objects.filter(project_eng__user=user),
    }
	return render(request,'Engineer/dashboard.html',context=dict)

def engassignedprojects(request):
	user = request.user
	cdfproject = CdfProjects.objects.filter(project_eng__user=user)
	return render(request,'Engineer/assignedproject.html',{'cdfproject':cdfproject})

def engineer_view_contractor_pro(request):
	proj = ContractorDetails.objects.all()
	return render(request,'Engineer/Engineercontractorproject.html',{'proj':proj})

def engdashboard(request):
	projs = []
	user = request.user
	oneproject = []
	cdf = EngineerDetails.objects.select_related().filter(cdfproject__project_eng__user=user)
	# else:	
		# cdfs = EngineerDetails.objects.select_related().filter(cdfproject__project_eng__project=project,cdfproject__project_eng__user=user)
	for l in cdf:
		projs.append(l.cdfproject.project) 
	keys = set(r for r in projs)	
	# cdf = CdfProjects.objects.filter(project_eng__user=user)
	return render(request,'Engineer/engineerview.html',{'cdf':keys})

def viewProgress(request):
	user = request.user
	print('before')
	# user = request.user
	cdfs = EngineerDetails.objects.filter(cdfproject__project_eng__user=user)
	for p in cdfs:
		print(p)
	# else:	
		# cdfs = EngineerDetails.objects.filter(cdfproject__project_eng__project=project,cdfproject__project_eng__user=user)
	# cdf = CdfProjects.objects.filter(project_eng__user=user)
	return render(request,'Engineer/engineerdetails.html',{'cdfs':cdfs})

def Engineer_view_approved_Project(request):
	cdfs = ProjectManager.objects.filter(proj_approve='approved')
	projs = []
	projects = []
	for p in cdfs:
		proj = ContractorDetails.objects.get(id=p.contrdetails_id)
		project = EngineerDetails.objects.get(id=p.engdetails_id)
		projs.append(proj)
		projects.append(project)
		print(p)
	return render(request,'Engineer/viewapprovedprojects.html',{'data':zip(projs,projects,cdfs)})	



def editcomp(request, id):
    companydetails = CdfProjects.objects.get(id=id)
    return render(request,'Engineer/updatedetails.html',{'companydetails':companydetails})


def saveassign(request):
	form =forms.CdfProjectRequestForm()
	# form_class = forms.DetailsEngineerForm()
	mydict={'form':form}
	if request.method == 'POST':
		cdfproject = request.POST.get('cdfproject')
		eng_report = request.POST.get('eng_report')
		images = request.POST.getlist('images')
		eng_approve = request.POST.get('eng_approve')
		progress = request.POST.get('progress')
		phases = request.POST.get('phases')

		form = forms.CdfProjectRequestForm(request.POST)
		# form_class = forms.DetailsEngineerForm(request.POST)
		if form.is_valid():
			cdfproject=form.cleaned_data['cdfproject']
			cdfproject.save()
			# form_class.save()
		
		else:
			print("form is invalid")
		for eng_images in images:
			report = EngineerDetails.objects.create(
				cdfproject = cdfproject,
				eng_report = eng_report,
				eng_images = eng_images,
				eng_approve = eng_approve,
				phases = phases,
				progress=progress,
				)
		return redirect('engineer-view-progress')
	return render(request,'Engineer/updatedetails.html',context=mydict)



def engineer_projectsview(request):
	user = request.user
	IGC = []
	IGS = []
	IGN = []
	NI = []
	CI = []
	SI = []
	BU = []
	TE = []
	TW =[]
	# sectors
	Education = []
	Security = []
	Health = []
	Administration = []
	Water = []
	Sports = []
	Environment = []
	projects = cdf_models.CdfProjects.objects.filter(project_eng__user=user)
	# Pagination

	paginator = Paginator(projects,4)
	page = request.GET.get('page')
	# End Pagination

	for m in projects:
		if m.location == 'Igembe Central':
			IGC.append(m.amount)
		elif m.location == 'Igembe South':
			IGS.append(m.amount)
		elif m.location == 'Igembe North':
			IGN.append(m.amount)
		elif m.location == 'North Imenti':
			NI.append(m.amount)
		elif m.location == 'Cental Imenti':
			CI.append(m.amount)
		elif m.location == 'South Imenti':
			SI.append(m.amount)
		elif m.location == 'Buuri':	
			BU.append(m.amount)
		elif m.location == 'Tigania East':	
			TE.append(m.amount)
		elif m.location == 'Tigania West':	
			TW.append(m.amount)
		else:
			print('No location')

	for s in projects:
		if s.sectors == 'Education':
			Education.append(s.amount)
		elif s.sectors == 'Security':
			Security.append(s.amount)
		elif s.sectors == 'Health':
			Health.append(s.amount)
		elif s.sectors == 'Administration':
			Administration.append(s.amount)
		elif s.sectors == 'Water':
			Water.append(s.amount)
		elif s.sectors == 'Sports':
			Sports.append(s.amount)
		elif s.sectors == 'Enviroment':
			Environment.append(s.amount)

	# Sectors
	eamount = sum(Education)
	samount = sum(Security)
	hamount = sum(Health)
	aamount = sum(Administration)
	wamount = sum(Water)
	samount = sum(Sports)
	evamount = sum(Environment)
	# Wards
	IGCamount = sum(IGC)
	IGSamount = sum(IGS)
	IGNamount = sum(IGN)
	NIamount = sum(NI)
	CIamount = sum(CI)
	SIamount = sum(SI)
	BUamount = sum(BU)
	TEamount = sum(TE)
	TWamount = sum(TW)
	print(NIamount)
	query = request.GET.get('q')
	if query:
		projects = projects.filter(project__iexact=query) or projects.filter(sectors__iexact=query)
		paginator = Paginator(projects,4)
		page = request.GET.get('page')

	try:
		reports = paginator.page(page)
	except PageNotAnInteger:
		reports = paginator.page(1)
	except EmptyPage:
		reports = paginator.page(paginator.num_pages)
	index = reports.number - 1
	max_index = len(paginator.page_range)
	start_index = index - 5 if index >= 5 else 0
	end_index = index + 5 if index <= max_index - 5 else max_index
	page_range = paginator.page_range[start_index:end_index]
	return render(request,'Engineer/project.html',
		{
			# 'saf':projects,
			'IGC':IGCamount,
			'IGS':IGSamount,
			'IGN':IGNamount,
			'NI':NIamount,
			'CI':CIamount,
			'SI':SIamount,
			'BU':BUamount,
			'TE':TEamount,
			'TW':TWamount,

			'edu':eamount,
			'sec':samount,
			'hea':hamount,
			'admi':aamount,
			'wtr':wamount,
			'sprt':samount,
			'env':evamount,

			'reports':reports,
			'page_range':page_range,
		})


