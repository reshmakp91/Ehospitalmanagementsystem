# Generated by Django 4.2.16 on 2024-11-18 09:47

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doctorapp', '0008_healtharticle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='healtharticle',
            name='content',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
