# Generated by Django 4.2.17 on 2024-12-09 17:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0010_alter_category_organisation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='organisation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leads.userprofile'),
        ),
    ]