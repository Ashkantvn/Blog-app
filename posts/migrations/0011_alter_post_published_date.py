# Generated by Django 5.0.6 on 2024-09-03 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0010_post_counted_views_alter_post_published_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='published_date',
            field=models.DateTimeField(blank=True),
        ),
    ]
