# Generated by Django 5.1.7 on 2025-03-18 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diagnosis', '0002_remove_plantdiagnosis_when_planted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plantdiagnosis',
            name='health_status',
        ),
        migrations.RemoveField(
            model_name='plantdiagnosis',
            name='location',
        ),
        migrations.RemoveField(
            model_name='plantdiagnosis',
            name='possible_cause',
        ),
        migrations.RemoveField(
            model_name='plantdiagnosis',
            name='treatment_recommendation',
        ),
        migrations.AlterField(
            model_name='plantdiagnosis',
            name='month',
            field=models.CharField(choices=[('January', 'January'), ('February', 'February'), ('March', 'March'), ('April', 'April'), ('May', 'May'), ('June', 'June'), ('July', 'July'), ('August', 'August'), ('September', 'September'), ('October', 'October'), ('November', 'November'), ('December', 'December')], max_length=20),
        ),
        migrations.AlterField(
            model_name='plantdiagnosis',
            name='sunlight_hours',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='plantdiagnosis',
            name='watering_frequency',
            field=models.CharField(max_length=20),
        ),
    ]
