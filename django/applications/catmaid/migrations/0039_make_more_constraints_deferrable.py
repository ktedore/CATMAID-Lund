# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-08 02:03

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    """Make the foreign keys in different tables deferrable. This can be useful
    to data ingestion and import. It makes those constraints also more
    consistent with others.
    """

    dependencies = [
        ('catmaid', '0038_add_missing_initial_skeleton_summaries'),
    ]

    operations = [
        migrations.RunSQL("""
            DO $$
            DECLARE
                -- Unfortunately, some older CATMAID instances have never been
                -- updated to use the constraint names defined in the current
                -- initial migration. The DO command below, will rectify this.

                location_editor_fkey_name text := (
                    SELECT conname from pg_constraint c, pg_attribute a
                    WHERE conrelid = 'location'::regclass
                    AND confrelid = 'auth_user'::regclass
                    AND attnum in (select unnest(conkey))
                    AND a.attrelid = 'location'::regclass
                    AND a.attname = 'editor_id_1'
                );
                location_user_fkey_name text := (
                    SELECT conname from pg_constraint c, pg_attribute a
                    WHERE conrelid = 'location'::regclass
                    AND confrelid = 'auth_user'::regclass
                    AND attnum in (select unnest(conkey))
                    AND a.attrelid = 'location'::regclass
                    AND a.attname = 'user_id'
                );
                location_project_fkey_name text := (
                    SELECT conname from pg_constraint c, pg_attribute a
                    WHERE conrelid = 'location'::regclass
                    AND confrelid = 'project'::regclass
                    AND attnum in (select unnest(conkey))
                    AND a.attrelid = 'location'::regclass
                    AND a.attname = 'project_id'
                );
                treenode_skeleton_fkey_name text := (
                    SELECT conname from pg_constraint c, pg_attribute a
                    WHERE conrelid = 'treenode'::regclass
                    AND confrelid = 'class_instance'::regclass
                    AND attnum in (select unnest(conkey))
                    AND a.attrelid = 'treenode'::regclass
                    AND a.attname = 'skeleton_id'
                );
                roi_stack_fkey_name text := (
                    SELECT conname from pg_constraint c, pg_attribute a
                    WHERE conrelid = 'region_of_interest'::regclass
                    AND confrelid = 'stack'::regclass
                    AND attnum in (select unnest(conkey))
                    AND a.attrelid = 'region_of_interest'::regclass
                    AND a.attname = 'stack_id'
                );
                treenode_connector_connector_fkey_name text := (
                    SELECT conname from pg_constraint c, pg_attribute a
                    WHERE conrelid = 'treenode_connector'::regclass
                    AND confrelid = 'connector'::regclass
                    AND attnum in (select unnest(conkey))
                    AND a.attrelid = 'treenode_connector'::regclass
                    AND a.attname = 'connector_id'
                );
                treenode_connector_treenode_fkey_name text := (
                    SELECT conname from pg_constraint c, pg_attribute a
                    WHERE conrelid = 'treenode_connector'::regclass
                    AND confrelid = 'treenode'::regclass
                    AND attnum in (select unnest(conkey))
                    AND a.attrelid = 'treenode_connector'::regclass
                    AND a.attname = 'treenode_id'
                );
            BEGIN
                -- If a declared variables has no result (i.e. the constraint
                -- doesn't exist), then the conditionals below will not execute
                -- their consequence (which is what we want).

                IF location_editor_fkey_name <> 'location_editor_id_fkey'
                THEN
                    EXECUTE 'ALTER TABLE ONLY location' ||
                        ' RENAME CONSTRAINT ' || location_editor_fkey_name ||
                        ' TO location_editor_id_fkey';
                END IF;

                IF location_user_fkey_name <> 'location_user_id_fkey'
                THEN
                    EXECUTE 'ALTER TABLE ONLY location' ||
                        ' RENAME CONSTRAINT ' || location_user_fkey_name ||
                        ' TO location_user_id_fkey';
                END IF;

                IF location_project_fkey_name <> 'location_project_id_fkey'
                THEN
                    EXECUTE 'ALTER TABLE ONLY location' ||
                        ' RENAME CONSTRAINT ' || location_project_id_fkey ||
                        ' TO location_project_id_fkey';
                END IF;

                IF treenode_skeleton_fkey_name <> 'treenode_skeleton_id_fkey'
                THEN
                    EXECUTE 'ALTER TABLE ONLY treenode' ||
                        ' RENAME CONSTRAINT ' || treenode_skeleton_fkey_name ||
                        ' TO treenode_skeleton_id_fkey';
                END IF;

                -- The '1' suffix is a typo in the original initial migration.
                -- This will be fixed in a separate migration for consistency.
                IF roi_stack_fkey_name <> 'region_of_interest_stack_id_fkey1'
                THEN
                    EXECUTE 'ALTER TABLE ONLY region_of_interest' ||
                        ' RENAME CONSTRAINT ' || roi_stack_fkey_name ||
                        ' TO region_of_interest_stack_id_fkey1';
                END IF;

                IF treenode_connector_connector_fkey_name <> 'treenode_connector_connector_id_fkey'
                THEN
                    EXECUTE 'ALTER TABLE ONLY treenode_connector' ||
                        ' RENAME CONSTRAINT ' || treenode_connector_connector_fkey_name ||
                        ' TO treenode_connector_connector_id_fkey';
                END IF;

                IF treenode_connector_treenode_fkey_name <> 'treenode_connector_treenode_id_fkey'
                THEN
                    EXECUTE 'ALTER TABLE ONLY treenode_connector' ||
                        ' RENAME CONSTRAINT ' || treenode_connector_treenode_id_fkey ||
                        ' TO treenode_connector_treenode_id_fkey';
                END IF;

                -- Update constraints and add missing constraints. Unfortunately
                -- some older CATMAID databases don't have all constraints specified
                -- in the initial migration, because they skipped this migration.

                -- location_editor_id_fkey
                IF NOT EXISTS (
                    SELECT constraint_schema, constraint_name
                    FROM   information_schema.referential_constraints
                    WHERE  constraint_name = 'location_editor_id_fkey'
                )
                THEN
                    ALTER TABLE ONLY location
                    ADD CONSTRAINT location_editor_id_fkey FOREIGN KEY (editor_id)
                    REFERENCES auth_user(id) ON DELETE CASCADE
                    DEFERRABLE INITIALLY DEFERRED;
                ELSE
                    ALTER TABLE ONLY location
                    ALTER CONSTRAINT location_editor_id_fkey
                    DEFERRABLE INITIALLY DEFERRED;
                END IF;


                -- location_project_id_fkey
                IF NOT EXISTS (
                    SELECT constraint_schema, constraint_name
                    FROM   information_schema.referential_constraints
                    WHERE  constraint_name = 'location_project_id_fkey'
                )
                THEN
                    ALTER TABLE ONLY location
                    ADD CONSTRAINT location_project_id_fkey FOREIGN KEY (project_id)
                    REFERENCES project(id) ON DELETE CASCADE
                    DEFERRABLE INITIALLY DEFERRED;
                ELSE
                    ALTER TABLE ONLY location
                    ALTER CONSTRAINT location_project_id_fkey
                    DEFERRABLE INITIALLY DEFERRED;
                END IF;


                -- location_user_id_fkey
                IF NOT EXISTS (
                    SELECT constraint_schema, constraint_name
                    FROM   information_schema.referential_constraints
                    WHERE  constraint_name = 'location_user_id_fkey'
                )
                THEN
                    ALTER TABLE ONLY location
                    ADD CONSTRAINT location_user_id_fkey FOREIGN KEY (user_id)
                    REFERENCES auth_user(id) ON DELETE CASCADE
                    DEFERRABLE INITIALLY DEFERRED;
                ELSE
                    ALTER TABLE location
                    ALTER CONSTRAINT location_user_id_fkey
                    DEFERRABLE INITIALLY DEFERRED;
                END IF;


                -- treenode_skeleton_id_fkey
                IF NOT EXISTS (
                    SELECT constraint_schema, constraint_name
                    FROM   information_schema.referential_constraints
                    WHERE  constraint_name = 'treenode_skeleton_id_fkey'
                )
                THEN
                    ALTER TABLE ONLY treenode
                    ADD CONSTRAINT treenode_skeleton_id_fkey FOREIGN KEY (skeleton_id)
                    REFERENCES class_instance(id) ON DELETE CASCADE;
                ELSE
                    ALTER TABLE treenode
                    ALTER CONSTRAINT treenode_skeleton_id_fkey
                    DEFERRABLE INITIALLY DEFERRED;
                END IF;


                -- region_of_interest_stack_id_fkey1
                IF NOT EXISTS (
                    SELECT constraint_schema, constraint_name
                    FROM   information_schema.referential_constraints
                    WHERE  constraint_name = 'region_of_interest_stack_id_fkey1'
                )
                THEN
                    ALTER TABLE ONLY region_of_interest
                    ADD CONSTRAINT region_of_interest_stack_id_fkey1 FOREIGN KEY (stack_id)
                    REFERENCES stack(id) ON DELETE CASCADE;
                ELSE
                    ALTER TABLE region_of_interest
                    ALTER CONSTRAINT region_of_interest_stack_id_fkey1
                    DEFERRABLE INITIALLY DEFERRED;
                END IF;


                -- treenode_connector_connector_id_fkey
                IF NOT EXISTS (
                    SELECT constraint_schema, constraint_name
                    FROM   information_schema.referential_constraints
                    WHERE  constraint_name = 'treenode_connector_connector_id_fkey'
                )
                THEN
                    ALTER TABLE ONLY treenode_connector
                    ADD CONSTRAINT treenode_connector_connector_id_fkey FOREIGN KEY (connector_id)
                    REFERENCES connector(id) ON DELETE CASCADE;
                ELSE
                    ALTER TABLE treenode_connector
                    ALTER CONSTRAINT treenode_connector_connector_id_fkey
                    DEFERRABLE INITIALLY DEFERRED;
                END IF;


                -- treenode_connector_treenode_id_fkey
                IF NOT EXISTS (
                    SELECT constraint_schema, constraint_name
                    FROM   information_schema.referential_constraints
                    WHERE  constraint_name = 'treenode_connector_treenode_id_fkey'
                )
                THEN
                    ALTER TABLE ONLY treenode_connector
                    ADD CONSTRAINT treenode_connector_treenode_id_fkey FOREIGN KEY (treenode_id)
                    REFERENCES treenode(id) ON DELETE CASCADE;
                ELSE
                    ALTER TABLE treenode_connector
                    ALTER CONSTRAINT treenode_connector_treenode_id_fkey
                    DEFERRABLE INITIALLY DEFERRED;
                END IF;
            END $$;
        """,
        """
            ALTER TABLE location
            ALTER CONSTRAINT location_editor_id_fkey
            NOT DEFERRABLE INITIALLY IMMEDIATE;

            ALTER TABLE location
            ALTER CONSTRAINT location_project_id_fkey
            NOT DEFERRABLE INITIALLY IMMEDIATE;

            ALTER TABLE location
            ALTER CONSTRAINT location_user_id_fkey
            NOT DEFERRABLE INITIALLY IMMEDIATE;

            ALTER TABLE treenode
            ALTER CONSTRAINT treenode_skeleton_id_fkey
            NOT DEFERRABLE INITIALLY IMMEDIATE;

            ALTER TABLE region_of_interest
            ALTER CONSTRAINT region_of_interest_stack_id_fkey1
            NOT DEFERRABLE INITIALLY IMMEDIATE;

            ALTER TABLE treenode_connector
            ALTER CONSTRAINT treenode_connector_connector_id_fkey
            NOT DEFERRABLE INITIALLY IMMEDIATE;

            ALTER TABLE treenode_connector
            ALTER CONSTRAINT treenode_connector_treenode_id_fkey
            NOT DEFERRABLE INITIALLY IMMEDIATE;
        """)
    ]
