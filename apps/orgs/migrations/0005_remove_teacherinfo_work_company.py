# Generated by Django 3.0.5 on 2020-04-11 21:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orgs', '0004_auto_20200411_1911'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacherinfo',
            name='work_company',
        ),
    ]