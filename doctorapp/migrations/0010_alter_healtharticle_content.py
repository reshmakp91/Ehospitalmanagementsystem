# Generated by Django 4.2.16 on 2024-11-18 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctorapp', '0009_alter_healtharticle_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='healtharticle',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
    ]
