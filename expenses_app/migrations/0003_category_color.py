# Generated by Django 5.0.6 on 2024-05-13 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses_app', '0002_alter_category_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='color',
            field=models.CharField(default='#000000', max_length=7),
        ),
    ]
