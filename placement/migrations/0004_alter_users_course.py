# Generated by Django 3.2 on 2023-02-28 20:02

from django.db import migrations
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('placement', '0003_alter_users_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='course',
            field=smart_selects.db_fields.ChainedForeignKey(blank=True, chained_field='department', chained_model_field='name', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='student_course', to='placement.department'),
        ),
    ]
