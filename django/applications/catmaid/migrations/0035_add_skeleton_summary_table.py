# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-22 01:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catmaid', '0034_add_node_query_cache_timestamp_and_unique_constraint'),
    ]

    operations = [
        migrations.CreateModel(
            name='SkeletonSummary',
            fields=[
                # Create skeleton ID constraint manually below
                ('skeleton', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True, serialize=False, to='catmaid.ClassInstance', db_constraint=False)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catmaid.Project')),
                ('last_summary_update', models.DateTimeField(default=django.utils.timezone.now)),
                ('original_creation_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_edition_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('num_nodes', models.IntegerField(default=0)),
                ('cable_length', models.FloatField(default=0))
            ],
            options={
                'db_table': 'catmaid_skeleton_summary',
            },
        ),
        migrations.RunSQL("""
            ALTER TABLE catmaid_skeleton_summary ALTER COLUMN num_nodes SET DEFAULT 0;
            ALTER TABLE catmaid_skeleton_summary ALTER COLUMN cable_length SET DEFAULT 0;
            ALTER TABLE catmaid_skeleton_summary ADD CONSTRAINT catmaid_skeleton_summary_skeleton_id_fk
                FOREIGN KEY (skeleton_id) REFERENCES class_instance (id) ON DELETE CASCADE;
        """, migrations.RunSQL.noop),

        # Add trigger functions for treenode table to update summary
        migrations.RunSQL("""
            DROP TRIGGER on_insert_treenode_update_edges ON treenode;
            DROP TRIGGER on_edit_treenode_update_edges ON treenode;
            DROP TRIGGER on_delete_treenode_update_edges ON treenode;

            DROP FUNCTION on_insert_treenode_update_edges();
            DROP FUNCTION on_edit_treenode_update_edges();
            DROP FUNCTION on_delete_treenode_update_edges();

            -- If a new node is inserted: add a new row to the summary table if
            -- inserted node has no parent. If this results in a conflict,
            -- increase node count of existing.
            CREATE OR REPLACE FUNCTION on_insert_treenode_update_summary_and_edges() RETURNS trigger
            LANGUAGE plpgsql AS
            $$
            BEGIN
                WITH new_edges AS (
                    -- Compute new edges and collect some other needed information
                    SELECT c.id, c.project_id, c.skeleton_id, c.creation_time,
                        c.edition_time, ST_MakeLine(
                            ST_MakePoint(c.location_x, c.location_y, c.location_z),
                            ST_MakePoint(p.location_x, p.location_y, p.location_z)
                        ) AS edge
                    FROM inserted_treenode c JOIN treenode p ON
                        (c.parent_id = p.id) OR (c.parent_id IS NULL AND c.id = p.id)
                ), edge_insert AS (
                    -- Insert new edges into edge table
                    INSERT INTO treenode_edge (id, project_id, edge)
                    SELECT e.id, e.project_id, e.edge FROM new_edges e
                ), skeleton_data AS (
                    -- Aggregate data over skeletons to prepare for summary update.
                    SELECT e.skeleton_id, e.project_id,
                        COUNT(*) AS num_nodes,
                        SUM(ST_3DLength(e.edge)) AS length,
                        MIN(creation_time) AS min_creation_time,
                        MAX(edition_time) AS max_edition_time
                    FROM new_edges e
                    GROUP BY skeleton_id, project_id
                )
                INSERT INTO catmaid_skeleton_summary (project_id, skeleton_id,
                    last_summary_update, original_creation_time,
                    last_edition_time, num_nodes, cable_length)
                (
                    SELECT s.project_id, s.skeleton_id, now(), s.min_creation_time,
                        s.max_edition_time, s.num_nodes, s.length
                    FROM skeleton_data s
                )
                ON CONFLICT (skeleton_id) DO UPDATE
                SET num_nodes = catmaid_skeleton_summary.num_nodes + EXCLUDED.num_nodes,
                    last_summary_update = EXCLUDED.last_summary_update, 
                    original_creation_time = LEAST(
                        catmaid_skeleton_summary.original_creation_time,
                        EXCLUDED.original_creation_time),
                    last_edition_time = GREATEST(
                        catmaid_skeleton_summary.last_edition_time,
                        EXCLUDED.last_edition_time),
                    cable_length = catmaid_skeleton_summary.cable_length + EXCLUDED.cable_length;

                RETURN NEW;

            END;
            $$;


            CREATE OR REPLACE FUNCTION on_edit_treenode_update_summary_and_edges() RETURNS trigger
            LANGUAGE plpgsql AS
            $$
            DECLARE
            tmp text;
            BEGIN
                -- Transition tables (old_treenode and new_treenode) can only be
                -- read once per statement. This is why we select them
                -- completely into a CTE. With Postgres 10.4 this can be replaced
                -- by direct transition table access, because it fixes the bug
                -- causing the current behavior.
                WITH old_treenode_data AS (
                    SELECT * FROM old_treenode
                ), new_treenode_data AS (
                    SELECT * FROM new_treenode
                ), updated_parent_edge_data AS (
                    -- Find all nodes that changed their position or parent
                    SELECT t.id, t.project_id, t.skeleton_id, t.creation_time,
                        t.edition_time, ST_MakeLine(
                            ST_MakePoint(t.location_x, t.location_y, t.location_z),
                            ST_MakePoint(p.location_x, p.location_y, p.location_z)
                        ) AS edge,
                        t.parent_id,
                        ot.edition_time as old_edition_time,
                        ot.creation_time AS old_creation_time,
                        ot.skeleton_id AS old_skeleton_id
                    FROM new_treenode_data t
                    JOIN old_treenode_data ot
                        ON t.id = ot.id
                    JOIN treenode p
                        ON (t.parent_id IS NOT NULL AND p.id = t.parent_id) OR
                           (t.parent_id IS NULL AND p.id = t.id)
                    WHERE ot.parent_id IS DISTINCT FROM t.parent_id OR
                       ot.location_x != t.location_x OR
                       ot.location_y != t.location_y OR
                       ot.location_z != t.location_z OR
                       ot.skeleton_id != t.skeleton_id
                ), updated_child_edge_data AS (
                    -- Find all unseen child nodes of the nodes with a changed
                    -- edge using an anti join.
                    SELECT c.id, c.project_id, c.skeleton_id, c.creation_time,
                        c.edition_time, ST_MakeLine(
                            ST_MakePoint(c.location_x, c.location_y, c.location_z),
                            ST_MakePoint(e.location_x, e.location_y, e.location_z)
                        ) AS edge,
                        c.parent_id,
                        c.edition_time AS old_edition_time,
                        c.creation_time AS old_creation_time,
                        c.skeleton_id AS old_skeleton_id
                    FROM treenode c
                    JOIN new_treenode_data e
                        ON c.parent_id = e.id
                    LEFT JOIN new_treenode_data c2
                        ON c.id = c2.id
                    WHERE c2.id IS NULL
                ), updated_edge_data AS (
                    -- Combine all directly changed nodes with a changed
                    -- location as well as the extra child nodes where the
                    -- parent changed location. The limit is needed to indicate
                    -- to the planner an upper limit of this CTE. This is
                    -- unfortunately needed, because no real estimates are done
                    -- on CTEs and no actual stats are used. This leads to
                    -- unfortunate join plans in the updated_edge CTE.
                    (SELECT *
                    FROM updated_parent_edge_data
                    LIMIT (SELECT COUNT(*) FROM updated_parent_edge_data))
                    UNION ALL
                    (SELECT *
                    FROM updated_child_edge_data
                    LIMIT (SELECT COUNT(*) FROM updated_child_edge_data))
                ), old_edge AS (
                    -- Get all old edges of changed nodes as well as their
                    -- children (if any). Child edges contribute to the cable
                    -- length as well and need to be updated.
                    SELECT t.id, t.project_id, t.old_skeleton_id AS skeleton_id,
                        t.old_creation_time AS creation_time,
                        t.old_edition_time AS edition_time,
                        e.edge
                    FROM updated_edge_data t
                    JOIN treenode_edge e
                        ON e.id = t.id
                ), updated_edge AS (
                    -- Update all changed edges. To have this join work fast, we
                    -- rely on reasonable statistics on the row count of
                    -- updated_edge_data. This is provided, by setting (obivious)
                    -- limits on its size when creating it.
                    UPDATE treenode_edge e
                    SET edge = ue.edge
                    FROM updated_edge_data ue
                    WHERE e.id = ue.id
                    RETURNING e.id
                ), new_edge AS (
                    -- Collect changed nodes both with and without location
                    -- change. Updated edge information takes precedence.
                    SELECT ue.id, ue.project_id, ue.skeleton_id,
                        ue.creation_time, ue.edition_time, ue.edge
                    FROM updated_edge_data ue
                    UNION ALL
                    SELECT nt.id, nt.project_id, nt.skeleton_id,
                        nt.creation_time, nt.edition_time, oe.edge
                    FROM new_treenode_data nt
                    LEFT JOIN updated_edge_data ue
                        ON nt.id = ue.id
                    JOIN old_edge oe
                        ON nt.id = oe.id
                    WHERE ue.id IS NULL
                ), old_skeleton_data AS (
                    -- Aggregate data over old skeleton datas to delete for summary.
                    SELECT e.skeleton_id, e.project_id,
                        -COUNT(*) AS num_nodes,
                        -SUM(ST_3DLength(e.edge)) AS length,
                        MIN(creation_time) AS min_creation_time,
                        MAX(edition_time) AS max_edition_time
                    FROM old_edge e
                    GROUP BY skeleton_id, project_id
                ), new_skeleton_data AS (
                    -- Aggregate data over skeletons to prepare for summary update.
                    SELECT e.skeleton_id, e.project_id,
                            COUNT(*) AS num_nodes,
                        SUM(ST_3DLength(e.edge)) AS length,
                        MIN(e.creation_time) AS min_creation_time,
                        MAX(e.edition_time) AS max_edition_time
                    FROM new_edge e
                    GROUP BY e.skeleton_id, e.project_id
                ), summary_update_delta AS (
                    SELECT skeleton_id, project_id,
                        SUM(num_nodes) AS num_nodes,
                        SUM(length) AS length,
                        MIN(min_creation_time) AS min_creation_time,
                        MAX(max_edition_time) AS max_edition_time
                    FROM (
                        SELECT os.skeleton_id, os.project_id, os.num_nodes,
                            os.length, os.min_creation_time, os.max_edition_time
                        FROM old_skeleton_data os
                        UNION ALL
                        SELECT ns.skeleton_id, ns.project_id, ns.num_nodes,
                            ns.length, ns.min_creation_time, ns.max_edition_time
                        FROM new_skeleton_data ns
                    ) update_data
                    GROUP BY skeleton_id, project_id
                )
                INSERT INTO catmaid_skeleton_summary (project_id, skeleton_id,
                    last_summary_update, original_creation_time,
                    last_edition_time, num_nodes, cable_length)
                (
                    SELECT s.project_id, s.skeleton_id, now(), s.min_creation_time,
                        s.max_edition_time, s.num_nodes, s.length
                    FROM summary_update_delta s
                )
                ON CONFLICT (skeleton_id) DO UPDATE
                SET num_nodes = catmaid_skeleton_summary.num_nodes + EXCLUDED.num_nodes,
                    last_summary_update = EXCLUDED.last_summary_update,
                    last_edition_time = GREATEST(
                        catmaid_skeleton_summary.last_edition_time,
                        EXCLUDED.last_edition_time),
                    cable_length = catmaid_skeleton_summary.cable_length + EXCLUDED.cable_length;

                RETURN NEW;
            END;
            $$;


            -- Remove all deleted nodes and their contributed cable length from
            -- skeleton summary and delete the edge reference.
            CREATE OR REPLACE FUNCTION on_delete_treenode_update_summary_and_edges()
                RETURNS trigger
                LANGUAGE plpgsql AS
            $$
            BEGIN
                -- Compute aggregated node count and cable length of deleted
                -- nodes per skeleton. Use this information to update summary.
                WITH skeleton_data AS (
                    SELECT t.skeleton_id,
                        t.project_id AS project_id,
                        COUNT(*) AS num_nodes,
                        SUM(ST_3DLength(e.edge)) AS length
                    FROM deleted_treenode t
                    JOIN treenode_edge e
                        ON t.id = e.id
                    GROUP BY t.skeleton_id, t.project_id
                )
                UPDATE catmaid_skeleton_summary s
                SET num_nodes = s.num_nodes - d.num_nodes,
                    cable_length = s.cable_length - d.length
                FROM skeleton_data d
                WHERE d.skeleton_id = s.skeleton_id
                AND d.project_id = s.project_id;

                -- Delete existing edge
                DELETE FROM treenode_edge e
                USING deleted_treenode t
                WHERE t.id = e.id
                AND t.project_id = e.project_id;

                RETURN OLD;
            END;
            $$;


            CREATE TRIGGER on_insert_treenode_update_summary_and_edges
            AFTER INSERT ON treenode
            REFERENCING NEW TABLE as inserted_treenode
            FOR EACH STATEMENT EXECUTE PROCEDURE on_insert_treenode_update_summary_and_edges();

            CREATE TRIGGER on_edit_treenode_update_summary_and_edges
            AFTER UPDATE ON treenode
            REFERENCING NEW TABLE as new_treenode OLD TABLE as old_treenode
            FOR EACH STATEMENT EXECUTE PROCEDURE on_edit_treenode_update_summary_and_edges();

            CREATE TRIGGER on_delete_treenode_update_summary_and_edges
            AFTER DELETE ON treenode
            REFERENCING OLD TABLE as deleted_treenode
            FOR EACH STATEMENT EXECUTE PROCEDURE on_delete_treenode_update_summary_and_edges();
        """, """
            DROP TRIGGER on_edit_treenode_update_summary_and_edges ON treenode;
            DROP TRIGGER on_insert_treenode_update_summary_and_edges ON treenode;
            DROP TRIGGER on_delete_treenode_update_summary_and_edges ON treenode;

            DROP FUNCTION on_edit_treenode_update_summary_and_edges();
            DROP FUNCTION on_insert_treenode_update_summary_and_edges();
            DROP FUNCTION on_delete_treenode_update_summary_and_edges();

            CREATE FUNCTION on_insert_treenode_update_edges()
                RETURNS trigger
                LANGUAGE plpgsql AS
            $$
            BEGIN
                INSERT INTO treenode_edge (id, project_id, edge) (
                    SELECT c.id, c.project_id, ST_MakeLine(
                        ST_MakePoint(c.location_x, c.location_y, c.location_z),
                        ST_MakePoint(p.location_x, p.location_y, p.location_z))
                    FROM treenode c JOIN treenode p ON
                        (c.parent_id = p.id) OR (c.parent_id IS NULL AND c.id = p.id)
                    WHERE c.id=NEW.id);
                RETURN NEW;
            END;
            $$;

            CREATE FUNCTION on_edit_treenode_update_edges()
                RETURNS trigger
                LANGUAGE plpgsql AS
            $$
            BEGIN
                IF OLD.parent_id IS DISTINCT FROM NEW.parent_id OR
                       OLD.location_x != NEW.location_x OR
                       OLD.location_y != NEW.location_y OR
                       OLD.location_z != NEW.location_z then
                    DELETE FROM treenode_edge WHERE id=OLD.id;
                    INSERT INTO treenode_edge (id, project_id, edge) (
                        SELECT NEW.id, NEW.project_id, ST_MakeLine(
                            ST_MakePoint(NEW.location_x, NEW.location_y, NEW.location_z),
                            ST_MakePoint(p.location_x, p.location_y, p.location_z))
                        FROM treenode p
                        WHERE (NEW.parent_id IS NOT NULL AND p.id = NEW.parent_id) OR
                              (NEW.parent_id IS NULL AND NEW.id = p.id));
                end if;
                RETURN NEW;
            END;
            $$;

            CREATE FUNCTION on_delete_treenode_update_edges()
                RETURNS trigger
                LANGUAGE plpgsql AS
            $$
            BEGIN
                DELETE FROM treenode_edge WHERE id=OLD.id;
                RETURN OLD;
            END;
            $$;

            CREATE TRIGGER on_insert_treenode_update_edges
            AFTER INSERT ON treenode
            FOR EACH ROW EXECUTE PROCEDURE on_insert_treenode_update_edges();

            CREATE TRIGGER on_edit_treenode_update_edges
            AFTER UPDATE ON treenode
            FOR EACH ROW EXECUTE PROCEDURE on_edit_treenode_update_edges();

            CREATE TRIGGER on_delete_treenode_update_edges
            BEFORE DELETE ON treenode
            FOR EACH ROW EXECUTE PROCEDURE on_delete_treenode_update_edges();
        """),

        # Insert initial data
        migrations.RunSQL("""
            -- Cable length, nodes, creation info, edition info
            WITH node_data AS (
                SELECT creation.skeleton_id, creation.project_id,
                    creation.user_id, creation.creation_time,edit.editor_id,
                    edit.edition_time, counter.nodes, len.cable_length
                FROM
                (
                  SELECT *, row_number() OVER(PARTITION BY skeleton_id ORDER BY edition_time DESC) AS rn
                  FROM treenode
                ) edit
                JOIN
                (
                  SELECT *, row_number() OVER(PARTITION BY skeleton_id ORDER BY creation_time ASC) AS rn
                  FROM treenode
                ) creation
                ON edit.skeleton_id = creation.skeleton_id
                JOIN
                (
                  SELECT skeleton_id, COUNT(*) AS nodes FROM treenode GROUP BY skeleton_id
                ) counter
                ON creation.skeleton_id = counter.skeleton_id
                JOIN
                (
                  SELECT t1.skeleton_id, SUM(
                    ST_3DLength(ST_MakeLine(ARRAY[
                        ST_MakePoint(t1.location_x, t1.location_y, t1.location_z),
                        ST_MakePoint(t2.location_x, t2.location_y, t2.location_z)
                    ]::geometry[]))
                  ) AS cable_length
                  FROM treenode t1
                  JOIN treenode t2
                  ON t1.parent_id = t2.id
                  GROUP BY t1.skeleton_id
                ) len
                ON creation.skeleton_id = len.skeleton_id
                WHERE edit.rn = 1 AND creation.rn = 1
            )
            INSERT INTO catmaid_skeleton_summary (skeleton_id,
                project_id, last_summary_update, original_creation_time,
                last_edition_time, num_nodes, cable_length)
            (
                SELECT d.skeleton_id, d.project_id, now(), d.creation_time,
                    d.edition_time, d.nodes, d.cable_length
                FROM node_data d
            );
        """, migrations.RunSQL.noop)
    ]
