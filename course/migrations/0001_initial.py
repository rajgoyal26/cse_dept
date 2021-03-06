# Generated by Django 2.0.6 on 2018-08-01 07:48

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import enumerations.enum


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('program', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CoPo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(choices=[('N', 'None'), ('H', 'High'), ('S', 'Slight'), ('M', 'Minimum')], default=enumerations.enum.CoPoLink('None'), max_length=10)),
                ('date', models.DateField(default=datetime.date.today, verbose_name='Date')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester', models.CharField(choices=[('SEM_1', '1st Semester'), ('SEM_2', '2nd Semester'), ('SEM_3', '3rd Semester'), ('SEM_4', '4th Semester'), ('SEM_5', '5th Semester'), ('SEM_6', '6th Semester'), ('SEM_7', '7th Semester'), ('SEM_8', '8th Semester')], default=enumerations.enum.Semester('1st Semester'), max_length=10)),
                ('name', models.CharField(max_length=50)),
                ('course_code', models.CharField(max_length=50)),
                ('course_type', models.CharField(choices=[('MTH', 'Mandatory Theory'), ('MLAB', 'Mandatory Lab'), ('ELECTH', 'Elective Theory'), ('ELECLAB', 'Elective lab'), ('VOL', 'Voluntary')], default=enumerations.enum.CourseType('Mandatory Theory'), max_length=10)),
                ('max_marks', models.IntegerField()),
                ('credits', models.PositiveSmallIntegerField()),
                ('objective', models.TextField()),
                ('syllabus', models.TextField()),
                ('text_books', models.TextField()),
                ('ref_material', models.TextField()),
                ('prerequisite', models.TextField()),
                ('duration', models.PositiveSmallIntegerField()),
                ('hours', models.PositiveSmallIntegerField()),
                ('updated_on', models.DateField(default=datetime.date.today, verbose_name='Date')),
                ('deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='CourseAvailable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.PositiveIntegerField()),
                ('active', models.BooleanField(default=True)),
                ('course', models.ForeignKey(on_delete=None, to='course.Course')),
                ('faculty', models.ForeignKey(on_delete=None, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CourseEnrollment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.PositiveIntegerField(default='2000')),
                ('course', models.ForeignKey(on_delete=None, to='course.Course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CourseFeedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.PositiveIntegerField()),
                ('active', models.BooleanField(default=False)),
                ('course', models.ForeignKey(on_delete=None, to='course.Course')),
                ('created_by', models.ForeignKey(on_delete=None, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CourseOutcome',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('course', models.ForeignKey(on_delete=None, to='course.Course')),
            ],
        ),
        migrations.CreateModel(
            name='CourseProgram',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=None, to='course.Course')),
                ('program', models.ForeignKey(on_delete=None, to='program.Program')),
            ],
        ),
        migrations.AddField(
            model_name='copo',
            name='course_outcome',
            field=models.ForeignKey(on_delete=None, to='course.CourseOutcome'),
        ),
        migrations.AddField(
            model_name='copo',
            name='program_outcome',
            field=models.ForeignKey(on_delete=None, to='program.ProgramOutcome'),
        ),
        migrations.AddField(
            model_name='copo',
            name='user',
            field=models.ForeignKey(on_delete=None, to=settings.AUTH_USER_MODEL),
        ),
    ]
