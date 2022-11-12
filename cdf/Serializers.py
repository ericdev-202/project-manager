from rest_framework import serializers
from cdf import models as c_models

class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = c_models.CdfProjects
        fields = [
	        'county_nam',
	        'project',
	        'sectors',
	        'amount',
	        'status',
	        'descrition',
	        'location',
	        'remarks',
	        'lat',
	        'lon',
	        'id'
        ]
class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = c_models.Comment
        fields = [
	        'post',
	        'author',
	        'text',
        ]

