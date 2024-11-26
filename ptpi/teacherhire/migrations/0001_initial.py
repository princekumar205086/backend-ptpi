# Generated by Django 5.1.3 on 2024-11-26 03:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Nursery to U.K.G', 'Nursery to U.K.G'), ('1 to 5', '1 to 5'), ('6 to 8', '6 to 8'), ('9 to 10', '9 to 10'), ('10 to 12', '10 to 12')], max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='EducationalQualification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_name', models.CharField(max_length=100)),
                ('subject_description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=255)),
                ('gender', models.CharField(choices=[('Female', 'Female'), ('Male', 'Male'), ('other', 'other')], max_length=10)),
                ('religion', models.CharField(max_length=100)),
                ('nationality', models.CharField(choices=[('Indian', 'Indian'), ('other', 'other')], max_length=100)),
                ('image', models.ImageField(upload_to='images/')),
                ('aadhar_no', models.CharField(max_length=12, unique=True)),
                ('phone', models.CharField(max_length=15)),
                ('alternate_phone', models.CharField(blank=True, max_length=15, null=True)),
                ('verified', models.BooleanField(default=False)),
                ('rating', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True)),
                ('date_of_birth', models.DateField()),
                ('availability_status', models.CharField(default='Available', max_length=50)),
                ('class_categories', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacherhire.classcategory')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TeacherExperiences',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institution', models.CharField(max_length=255)),
                ('role', models.CharField(max_length=255)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('achievements', models.TextField(blank=True, null=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TeacherQualification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institution', models.CharField(max_length=225)),
                ('year_of_passing', models.PositiveIntegerField()),
                ('grade_or_percentage', models.CharField(blank=True, max_length=50, null=True)),
                ('qualification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacherhire.educationalqualification')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TeachersAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_type', models.CharField(choices=[('current', 'Current'), ('permanent', 'Permanent')], max_length=10)),
                ('state', models.CharField(default='Bihar', max_length=100)),
                ('division', models.CharField(max_length=100)),
                ('district', models.CharField(max_length=100)),
                ('block', models.CharField(max_length=100)),
                ('village', models.CharField(max_length=100)),
                ('area', models.TextField(blank=True, null=True)),
                ('pincode', models.CharField(max_length=6)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TeacherSkill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proficiency_level', models.CharField(blank=True, max_length=100, null=True)),
                ('years_of_experience', models.PositiveIntegerField(default=0)),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacherhire.skill')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]