# Generated by Django 3.2 on 2023-02-15 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('placement', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Students',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=130)),
                ('rollnumber', models.CharField(max_length=10)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('department', models.CharField(max_length=25)),
                ('course', models.CharField(max_length=10)),
                ('yearofpassing', models.IntegerField(max_length=5)),
            ],
        ),
    ]