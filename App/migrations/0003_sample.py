# Generated by Django 4.1.6 on 2024-01-09 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0002_categories_course_discount_order_subcategories_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to='sample/')),
            ],
        ),
    ]