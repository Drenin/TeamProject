# Generated by Django 4.0.1 on 2022-02-04 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subsite', '0002_post_subsitephoto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='postname',
            field=models.CharField(default='', max_length=50, null=True),
        ),
    ]
