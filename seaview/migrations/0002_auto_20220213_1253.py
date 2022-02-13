# Generated by Django 3.1.3 on 2022-02-13 03:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('seaview', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='voter',
            field=models.ManyToManyField(related_name='voter_review', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='review',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_review', to=settings.AUTH_USER_MODEL),
        ),
    ]
