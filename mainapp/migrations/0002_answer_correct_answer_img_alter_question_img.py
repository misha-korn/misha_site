# Generated by Django 5.0.6 on 2024-07-03 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='correct',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='answer',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='answer_img'),
        ),
        migrations.AlterField(
            model_name='question',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='question_img'),
        ),
    ]
