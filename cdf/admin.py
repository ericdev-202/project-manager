from django.contrib import admin

from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from cdf import models as cdf_models
from django.contrib import admin
from .models import User 
from .models import Contractor, Engineer,ContractorDetails,EngineerDetails,ProjectManager,Manager

class CdfAdmin(LeafletGeoAdmin):
	list_display = ['project','location','descrition','sectors','amount','status','remarks','geom','county_nam']


# class FroudReportsAdmin(LeafletGeoAdmin):
# 	list_display = ['title','photo','description','created','modified','geom']

class SuggestionsAdmin(LeafletGeoAdmin):
	list_display = ['suggestion','body','status','name','email','created','modified']

class ReportAdmin(LeafletGeoAdmin):
	list_display = ['description','image','opinion','geom','created','modified']

class EventAdmin(LeafletGeoAdmin):
	list_display = ['title','description','mdate','mtime','geom']

class ActivityAdmin(LeafletGeoAdmin):
	list_display = ['title','venue','description','mtime','mdate','created','modified']

class ContactUsAdmin(LeafletGeoAdmin):
	list_display = ['fullname','email','phonenumber','body','created','modified']
	list_editable = ['email','phonenumber','body']
	list_filter = ['created']


admin.site.register(Contractor)
admin.site.register(Engineer)
admin.site.register(Manager)
admin.site.register(ContractorDetails)
admin.site.register(EngineerDetails)
admin.site.register(ProjectManager)
# admin.site.register(cdf_models.ContactUs,ContactUsAdmin)
# admin.site.register(cdf_models.Events,ActivityAdmin)
# admin.site.register(cdf_models.Suggestions,SuggestionsAdmin)
admin.site.register(cdf_models.Boundary,LeafletGeoAdmin)
admin.site.register(cdf_models.CdfProjects,CdfAdmin)
# admin.site.register(cdf_models.Comment)
admin.site.register(cdf_models.Report,ReportAdmin)
# admin.site.register(cdf_models.SecurityEvent,EventAdmin)

# Register your models here.
