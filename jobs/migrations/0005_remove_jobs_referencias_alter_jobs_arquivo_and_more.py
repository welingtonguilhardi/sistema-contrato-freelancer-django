# Generated by Django 4.0.3 on 2022-04-10 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0004_jobs_arquivo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobs',
            name='referencias',
        ),
        migrations.AlterField(
            model_name='jobs',
            name='arquivo',
            field=models.FileField(null=True, upload_to=None),
        ),
        migrations.DeleteModel(
            name='Referencias',
        ),
    ]