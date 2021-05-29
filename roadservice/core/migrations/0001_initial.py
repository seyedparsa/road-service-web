# Generated by Django 3.2.3 on 2021-05-28 17:37

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Citizen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='County',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=280)),
                ('lat', models.DecimalField(decimal_places=6, max_digits=9)),
                ('long', models.DecimalField(decimal_places=6, max_digits=9)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('state', models.CharField(choices=[('RP', 'Reported'), ('RJ', 'Rejected'), ('AC', 'Accepted'), ('AS', 'Assigned'), ('DO', 'Done'), ('SC', 'Scored')], default='RP', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='MachineryType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Mission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('issue', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.issue')),
            ],
        ),
        migrations.CreateModel(
            name='MissionType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Speciality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='SpecialityRequirement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField()),
                ('issue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.issue')),
                ('speciality', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.speciality')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceTeam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('deleted_at', models.DateTimeField(null=True)),
                ('active_mission', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.mission')),
                ('county', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.county')),
                ('speciality', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.speciality')),
            ],
        ),
        migrations.CreateModel(
            name='Serviceman',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.serviceteam')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='mission',
            name='service_teams',
            field=models.ManyToManyField(to='core.ServiceTeam'),
        ),
        migrations.AddField(
            model_name='mission',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.missiontype'),
        ),
        migrations.CreateModel(
            name='MachineryRequirement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField()),
                ('issue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.issue')),
                ('machinery_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.machinerytype')),
            ],
        ),
        migrations.CreateModel(
            name='Machinery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_count', models.PositiveIntegerField()),
                ('available_count', models.PositiveIntegerField()),
                ('county', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.county')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.machinerytype')),
            ],
        ),
        migrations.AddField(
            model_name='issue',
            name='province',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.province'),
        ),
        migrations.AddField(
            model_name='issue',
            name='reporter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.citizen'),
        ),
        migrations.CreateModel(
            name='CountyExpert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('county', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.county')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='county',
            name='province',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.province'),
        ),
    ]