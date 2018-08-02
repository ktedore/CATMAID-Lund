# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-26 20:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    """Add a statistics summary table. This table stores aggregated data per
    user per hour and can be recreated from scratch off of other existing tables
    (in that sense it is like a materialized view). Therefore, there is no need
    to add history tracking to it.
    """

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catmaid', '0024_add_neuron_history_indices'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatsSummary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('n_connector_links', models.IntegerField(default=0)),
                ('n_reviewed_nodes', models.IntegerField(default=0)),
                ('n_treenodes', models.IntegerField(default=0)),
                ('n_edited_treenodes', models.IntegerField(default=0)),
                ('n_edited_connectors', models.IntegerField(default=0)),
                ('n_imported_treenodes', models.IntegerField(default=0)),
                ('n_imported_connectors', models.IntegerField(default=0)),
                ('cable_length', models.FloatField(default=0)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catmaid.Project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'catmaid_stats_summary',
            },
        ),
        migrations.RunSQL("""
            ALTER TABLE catmaid_stats_summary ALTER COLUMN n_connector_links SET DEFAULT 0;
            ALTER TABLE catmaid_stats_summary ALTER COLUMN n_reviewed_nodes SET DEFAULT 0;
            ALTER TABLE catmaid_stats_summary ALTER COLUMN n_treenodes SET DEFAULT 0;
            ALTER TABLE catmaid_stats_summary ALTER COLUMN n_edited_treenodes SET DEFAULT 0;
            ALTER TABLE catmaid_stats_summary ALTER COLUMN n_edited_connectors SET DEFAULT 0;
            ALTER TABLE catmaid_stats_summary ALTER COLUMN n_imported_treenodes SET DEFAULT 0;
            ALTER TABLE catmaid_stats_summary ALTER COLUMN n_imported_connectors SET DEFAULT 0;
            ALTER TABLE catmaid_stats_summary ALTER COLUMN cable_length SET DEFAULT 0;
        """, migrations.RunSQL.noop),
        migrations.AlterUniqueTogether(
            name='statssummary',
            unique_together=set([('project', 'user', 'date')]),
        ),
        migrations.RunSQL("""
            -- Add missing indices that help some statistics queries
            CREATE INDEX treenode_connector_creation_time_idx ON treenode_connector (creation_time);
            CREATE INDEX review_review_time_idx ON review (review_time);
        """, """
            DROP INDEX treenode_connector_creation_time_idx;
            DROP INDEX review_review_time_idx;
        """)
    ]
