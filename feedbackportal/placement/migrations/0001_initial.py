# Generated by Django 3.2 on 2023-02-13 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Carausel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='pics/%y/%m/%d/')),
                ('title', models.CharField(max_length=150)),
                ('sub_title', models.CharField(max_length=100)),
            ],
        ),
    ]
