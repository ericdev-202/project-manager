
from django.urls import path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from cdf import views as cdf_views, views 
from django.views.generic import TemplateView
from djgeojson.views import GeoJSONLayerView

from cdf import models as c_models
from . import views
from django.contrib.auth.views import LoginView,LogoutView

from django.contrib.auth import views as auth_views
urlpatterns = [
	path('', cdf_views.home,name='home'),
    path('about/',cdf_views.AboutPage,name='about'),
    path('contact/',cdf_views.ContactPage,name='contact'),
	path('projects/', cdf_views.projectsview,name='projects'),
    url(r'^projectsdata.geojson$', GeoJSONLayerView.as_view(model=c_models.CdfProjects, properties=('project','location','descrition','sectors','amount','status','remarks','county_nam')), name='projectsdata'),
	path('report/',cdf_views.ReportView,name='report'),
	path(r'details/<int:pk>/',cdf_views.projectdetail, name = "details"),
    path('suggest/',cdf_views.suggestionview,name='suggest'),
    url(r'^incidents.geojson$', GeoJSONLayerView.as_view(model=c_models.Report, properties=('title','description','mdate','mtime')), name='incidents'),
    path(r'^incidents/',cdf_views.ReportDisplay,name='incidents'),
    path(r'incidentdata/',cdf_views.Incidence_json,name='incidentdata'),
    # path(r'projectsdata/',cdf_views.Projects_json,name='projectsdata'),
    url(r'^inform/',cdf_views.ContactU,name='inform'),
    path(r'boundary/',cdf_views.ConstBoundary,name='boundary'),
    path(r'^event/',cdf_views.EventDisplay,name='event'),
    path(r'^comj/',cdf_views.commentjson,name='comj'),
    path(r'^buffer/',cdf_views.bufferPoints,name='buffer'),
    path(r'eventsdata/',cdf_views.Events_json,name='eventsdata'),
    path(r'^activity/$',cdf_views.ActivityData, name='activity'),
    path(r'^post/(?P<pk>\d+)/comment/', cdf_views.add_comment_to_post, name='add_comment_to_post'),
    path(r'^comment/(?P<pk>\d+)/approve/', cdf_views.comment_approve, name='comment_approve'),
    path(r'^comment/(?P<pk>\d+)/remove/', cdf_views.comment_remove, name='comment_remove'),
    path('allprojects',views.all_projects,name='allprojects'),



    path('adminclick', views.adminclick_view),
    path('contractorclick', views.contractorclick_view),
    path('engineerclick', views.engineerclick_view),
    # path('gd',views.home_view),

    
    # path('updatedetails/<int:id>',views.updateassigned),
    # path('makerequest/',views.MakeRequest,name="makerequest"),
    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    # path('view_approved_request_view/',views.view_approved_request_view,name="view_approved_request_view"),
    # path('ViewProgress/',views.ViewProgress,name="ViewProgress"),

    path('contractorsignup', views.contractor_signup_view,name='manage-cont'),
    path('engineersignup', views.engineer_signup_view,name='manage-engi'),
    path('managersignup',views.admin_signup_view,name="manager-signup"),

    path('contractor_login', LoginView.as_view(template_name='login/contractorlogin.html'),name='contractorlogin'),
    path('projectmanager_login', LoginView.as_view(template_name='login/ProjectManagerLogin.html'),name='projectmanlogin'),
    path('engineerlogin', LoginView.as_view(template_name='login/engineerlogin.html'),name='engineerlogin'),
    path('adminlogin', LoginView.as_view(template_name='login/adminlogin.html'),name='adminlogin'),

    path('logout', LogoutView.as_view(template_name='temps/dashboard.html'),name='logout'),

    #admin urls
     path('deleteproject',views.deleteproject,name='deleteproject'),
    path('admin-dashboard', views.admin_dashboard,name='admin-dashboard'),
    path('projectdetail',views.admin_projectdetails,name='projectdetails'),
    path('adminprojects/', cdf_views.admin_projectsview,name='admin-projects'),

    path('admin-view-engineer',views.admin_engineer_view,name='admin-view-engineer'),
    path('approve-engineer/<int:pk>', views.approve_engineer_view,name='approve-engineer'),
    path('delete-engineer/<int:pk>', views.delete_engineer_view,name='delete-engineer'),
    path(r'^adminincidents/',cdf_views.AdminReportDisplay,name='adminincidents'),
    path('contractor-view',views.admin_contractor_view,name='contractor-view'),
    path('AdminView_ContReport',views.AdminView_ContractorReport,name="AdminView_ContractorReport"),
    path('AdminView_EngReport',views.AdminView_EngineerReport,name="AdminView_EngineerReport"),
    path('ProjectMDetails/',views.ProjectManagerDetails,name="ProjectManagerDetails"),
    path('proj/',views.admin_all_project,name="projs"),
    path('project_manager_progress/',views.Project_manager_progress,name="project_manager_progress"),




    #engineer
    path('engineer',views.engineer_dashboard,name='engineer'),
    path('engassignedprojects/',views.engassignedprojects,name="assignedprojects"),
    # path('projectss',views.engdashboard,name='project-details'),
    path('engineer_view_contractor_pro',views.engineer_view_contractor_pro,name="eng-view-cont-project"),
    path('engdashboard/',views.engdashboard,name='engdashboard'),
    path('viewlog',views.viewProgress,name='engineer-view-progress'),
    path('engineerprojects/', views.engineer_projectsview,name='engineer-projectsview'),
    path('updateapproval/',views.saveassign),
    path('engineer_approved_projects/',views.Engineer_view_approved_Project,name="engineer-approved-projects"),
    # path('viewlog/<slug:project>/',views.viewProgress),

    ##Contractor
    path('contractor/',views.contractor_dashboard,name="contractor-dash"),
    
    path('assignedproj/',views.assignedprojects,name="assignedproj"),
    # path('updatedetails/<int:id>',views.updateassign),
    # path('editdetails/<int:id>',views.editcompany),
    path('updatecompany/',views.saveassigned),
    # path('update/',views.showprogress),
    path('population-chart/', views.showprogress, name='population-chart'),
    path('contprojects/', views.cont_project,name='cont-projects'),
    path('Viewp/',views.ViewProjectsAsign,name="view-cont-projects"),
    path('projview/',views.contdashboard,name="contractor-view-progress"),
    path('contractor_all_project/',views.contractor_all_project,name="contractor-all-project"),


]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
# 	urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)