
# Generated by Django 4.0.1 on 2022-02-13 11:52

# Generated by Django 4.0.1 on 2022-02-13 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subsite', '0007_auto_20220211_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
