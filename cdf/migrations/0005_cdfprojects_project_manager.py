# Generated by Django 3.2.14 on 2022-11-08 03:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cdf', '0004_manager'),
    ]

    operations = [
        migrations.AddField(
            model_name='cdfprojects',
            name='project_manager',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cdf.manager'),
        ),
    ]