# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-09-30 09:13
from __future__ import unicode_literals

from django.db import migrations, models

from corehq.sql_db.operations import RawSQLMigration

migrator = RawSQLMigration(('custom', 'icds_reports', 'migrations', 'sql_templates'))


class Migration(migrations.Migration):

    dependencies = [
        ('icds_reports', '0135_add_vhnd_field'),
    ]

    operations = [
        migrations.RunSQL("ALTER table daily_attendance ADD COLUMN open_bfast_count smallint "),
        migrations.RunSQL("ALTER table daily_attendance ADD COLUMN open_hotcooked_count smallint "),
        migrations.RunSQL("ALTER table daily_attendance ADD COLUMN days_thr_provided_count smallint "),
        migrations.RunSQL("ALTER table daily_attendance ADD COLUMN open_pse_count smallint "),
    ]
