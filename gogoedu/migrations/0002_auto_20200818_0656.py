# Generated by Django 3.0.9 on 2020-08-18 06:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gogoedu', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gogoedu.Question'),
        ),
        migrations.AlterField(
            model_name='user_test',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gogoedu.Test'),
        ),
        migrations.AlterField(
            model_name='user_test',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='word',
            name='type',
            field=models.CharField(choices=[('V', 'Verb'), ('N', 'Noun'), ('Adj', 'Adjective')], max_length=10),
        ),
    ]