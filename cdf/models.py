# from django.db import models
from django.contrib.gis.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from djgeojson.fields import PolygonField,PointField,MultiPolygonField,MultiPointField

from ckeditor.fields import RichTextField 
from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

phases = (
	('phase1','phase1'),
	('phase2','phase2'),
	('phase3','phase3'),
	('phase4','phase4'),
	('phase5','phase5')
	)
status=(
		('Complete','Complete'),
		('Incomplete','Incomplete'),
		('Onprogress','Onprogress'),
		('Stopped','Stopped')
		)
suggest = (
	('Comment','Comment'),
	('Complain','Complain')
	)
APPROVALS = (
	('approved','approved'),
	('notapproved','notapproved')
	)
ACCEPTANCES = (
	('accepted','accepted'),
	('notaccepted','notaccepted')
	)
class Contractor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/ContractorProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_instance(self):
        return self
    def __str__(self):
        return self.user.username

class Manager(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/EngineerProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.IntegerField()
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name

class Engineer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/EngineerProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.IntegerField()
    skill = models.CharField(max_length=500,null=True)
    salary=models.PositiveIntegerField(null=True)
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name


class BaseContent(models.Model):
	title = models.CharField(max_length=150)
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True


class FroudReports(BaseContent):
	photo = models.ImageField(upload_to='reportmedia/%y/%m/%d',blank=True)
	description = models.TextField()
	geom = PointField()

	def __str__(self):
		return self.title

	class Meta:
		verbose_name_plural = 'FroudReports'
		ordering = ['-created']

class Suggestions(models.Model):
	suggestion = models.CharField(max_length=200,choices=suggest)
	body = models.TextField()
	status = models.CharField(max_length=200,choices=status)
	name = models.CharField(max_length=300)
	email = models.EmailField()
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.suggestion

	class Meta:
		verbose_name_plural = 'Suggestions'
		ordering = ['-created']


class Events(BaseContent):
	description = models.TextField()
	mdate = models.DateField()
	mtime = models.TimeField()
	venue = models.CharField(max_length=200)

	def __str__(self):
		return self.title

	class Meta:
		verbose_name_plural = 'Events'
		ordering = ['-created']
class CdfProjects(models.Model): 
	project_manager = models.ForeignKey(Manager,on_delete=models.CASCADE,null=True)
	project = models.CharField(max_length=254)
	descrition = models.CharField(max_length=254)
	phases = models.CharField(max_length=150,choices=phases)
	project_eng = models.ForeignKey(Engineer,on_delete=models.CASCADE,null=True)
	project_cont = models.ForeignKey(Contractor, on_delete=models.CASCADE,null=True)
	duration = models.CharField(max_length=150,null=True,blank=True)
	status = models.CharField(max_length=254,choices=status)
	startdate = models.DateField(null=True,blank=True,auto_now_add=True)
	propdate = models.DateField(null=True,blank=True)
	remarks = models.CharField(max_length=254,null=True,blank=True)
	sectors = models.CharField(max_length=254)
	amount = models.BigIntegerField()
	lat = models.FloatField()
	county_nam = models.CharField(max_length=50)
	location = models.CharField(max_length=100)
	lon = models.FloatField()
	geom = MultiPointField(null=True,blank=True)


	def __str__(self):
		return self.project

	def approved_comments(self):
		return self.comments.filter(approved_comment=True)


class ContractorDetails(models.Model):
	cdfproject = models.ForeignKey(CdfProjects,on_delete=models.CASCADE,null=True)
	contr_report = models.FileField(upload_to='')
	contr_remark = RichTextField(null=True,blank=True)
	progress = models.BigIntegerField(null=True,blank=True)
	contr_images = models.FileField(upload_to='')
	status = models.CharField(max_length=254,choices=status)
	contr_accept = models.CharField(max_length=150,choices=ACCEPTANCES,default="notaccepted")
	phases = models.CharField(max_length=150,choices=phases)	
	finishdate = models.DateField(null=True,blank=True)

	def __str__(self):
		return self.cdfproject.project


	

class EngineerDetails(models.Model):
	cdfproject = models.ForeignKey(CdfProjects,on_delete=models.CASCADE,null=True)
	eng_report = models.FileField(upload_to='document/')
	engineer_remarks = RichTextField(null=True,blank=True)
	eng_images = models.FileField(upload_to='images/')
	phases = models.CharField(max_length=150,choices=phases)	
	eng_approve = models.CharField(max_length=150,choices=APPROVALS, default="notapproved")
	progress = models.BigIntegerField(null=True,blank=True)

	def __str__(self):
		return self.cdfproject.project

class ProjectManager(models.Model):	
	contrdetails = models.ForeignKey(ContractorDetails,on_delete=models.CASCADE,null=True)
	engdetails = models.ForeignKey(EngineerDetails,on_delete=models.CASCADE,null=True)
	proj_report = models.FileField(upload_to='document/')
	project_remark = RichTextField(null=True,blank=True)
	phases = models.CharField(max_length=150,choices=phases)
	proj_approve = models.CharField(max_length=150,choices=APPROVALS, default="notapproved")
	progress = models.BigIntegerField(null=True,blank=True)

class Boundary(models.Model):
    objectid_1 = models.BigIntegerField()
    objectid = models.FloatField()
    province = models.CharField(max_length=50)
    const_nam = models.CharField(max_length=50)
    elec_area_field = models.CharField(max_length=50)
    local_auth = models.CharField(max_length=50)
    st_area_sh = models.FloatField()
    st_length_field = models.FloatField()
    const_no = models.FloatField()
    county_nam = models.CharField(max_length=50)
    county_no = models.FloatField()
    st_length1 = models.FloatField()
    votes = models.BigIntegerField()
    st_lengt_1 = models.FloatField()
    globalid = models.CharField(max_length=38)
    shape_leng = models.FloatField()
    shape_area = models.FloatField()
    geom = MultiPolygonField()



# Comments on CdfProjects
class Comment(models.Model):
    post = models.ForeignKey(CdfProjects, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

    class Meta:
    	ordering = ['-created_date']

class Report(models.Model):
	image = models.ImageField(upload_to='reportImages/%y/%m/%d',blank=True)
	description = models.TextField()
	geom = PointField()
	created = models.DateTimeField(auto_now_add=True)
	opinion = models.CharField(max_length=200,choices=suggest)
	modified = models.DateTimeField(auto_now=True)

	@property
	def image_url(self):
		return self.image.url


	class Meta:
		verbose_name_plural = 'Reports'
		ordering = ['-created']

	def __str__(self):
		return self.description

class SecurityEvent(models.Model):
	title = models.CharField(max_length=200)
	description = models.TextField()
	mdate = models.DateField()
	mtime = models.TimeField()
	geom = PointField()
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name_plural = 'SecurityEvent'
		ordering = ['-created']

	def __str__(self):
		return self.title

class ContactUs(models.Model):
	fullname =  models.CharField(max_length=200)
	email = models.EmailField()
	phonenumber = models.IntegerField()
	body = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)

	def __str__(self):
		return 'Information from {} through {}'.format(self.fullname, self.email)

	class Meta:
		ordering = ['-created']
		verbose_name_plural = 'ContactUs'
