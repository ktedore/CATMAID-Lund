# Generated by Django 2.1.7 on 2019-02-18 16:37

from django.db import migrations

forward = """
    -- Obtain the foreign key constraint name in a particular column of a
    -- specific relation to a target relation.
    CREATE OR REPLACE FUNCTION get_fk_constraint_name(relname text, colname text, targetrelname text)
        RETURNS text AS $$
    DECLARE
        constraint_name text;
    BEGIN
        SELECT conname INTO constraint_name
        FROM pg_constraint c, pg_attribute a
        WHERE conrelid = relname::regclass
        AND confrelid = targetrelname::regclass
        AND attnum in (select unnest(conkey))
        AND a.attrelid = relname::regclass
        AND a.attname = colname;

        RETURN constraint_name;
    END; $$
    LANGUAGE plpgsql;

    DO $$
    BEGIN
        -- catmaid_sampler, change Django's constraint name
        EXECUTE 'ALTER TABLE ONLY catmaid_sampler ' ||
            'DROP CONSTRAINT ' || get_fk_constraint_name('catmaid_sampler', 'project_id', 'project');
        ALTER TABLE ONLY catmaid_sampler
            ADD CONSTRAINT catmaid_sampler_project_id_fkey
            FOREIGN KEY (project_id) REFERENCES project(id)
            ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;

        -- catmaid_samplerconnector, change Django's constraint name
        EXECUTE 'ALTER TABLE ONLY catmaid_samplerconnector ' ||
            'DROP CONSTRAINT ' || get_fk_constraint_name('catmaid_samplerconnector', 'project_id', 'project');
        ALTER TABLE ONLY catmaid_samplerconnector
            ADD CONSTRAINT catmaid_samplerconnector_project_id_fkey
            FOREIGN KEY (project_id) REFERENCES project(id)
            ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;

        -- catmaid_samplerdomain, change Django's constraint name
        EXECUTE 'ALTER TABLE ONLY catmaid_samplerdomain ' ||
            'DROP CONSTRAINT ' || get_fk_constraint_name('catmaid_samplerdomain', 'project_id', 'project');
        ALTER TABLE ONLY catmaid_samplerdomain
            ADD CONSTRAINT catmaid_samplerdomain_project_id_fkey
            FOREIGN KEY (project_id) REFERENCES project(id)
            ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;

        -- catmaid_samplerinterval, change Django's constraint name
        EXECUTE 'ALTER TABLE ONLY catmaid_samplerinterval ' ||
            'DROP CONSTRAINT ' || get_fk_constraint_name('catmaid_samplerinterval', 'project_id', 'project');
        ALTER TABLE ONLY catmaid_samplerinterval
            ADD CONSTRAINT catmaid_samplerinterval_project_id_fkey
            FOREIGN KEY (project_id) REFERENCES project(id)
            ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;

        -- catmaid_skeleton_summary, change Django's constraint name
        EXECUTE 'ALTER TABLE ONLY catmaid_skeleton_summary ' ||
            'DROP CONSTRAINT ' || get_fk_constraint_name('catmaid_skeleton_summary', 'project_id', 'project');
        ALTER TABLE ONLY catmaid_skeleton_summary
            ADD CONSTRAINT catmaid_skeleton_summary_project_id_fkey
            FOREIGN KEY (project_id) REFERENCES project(id)
            ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;

        -- catmaid_stats_summary, change Django's constraint name
        EXECUTE 'ALTER TABLE ONLY catmaid_stats_summary ' ||
            'DROP CONSTRAINT ' || get_fk_constraint_name('catmaid_stats_summary', 'project_id', 'project');
        ALTER TABLE ONLY catmaid_stats_summary
            ADD CONSTRAINT catmaid_stats_summary_project_id_fkey
            FOREIGN KEY (project_id) REFERENCES project(id)
            ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;

        -- change_request
        ALTER TABLE ONLY change_request
            ADD CONSTRAINT change_request_project_id_fkey
            FOREIGN KEY (project_id) REFERENCES project(id)
            ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;

        -- class_instance_class_instance
        ALTER TABLE ONLY class_instance_class_instance
            DROP CONSTRAINT class_instance_class_instance_project_id_fkey;
        ALTER TABLE ONLY class_instance_class_instance
            ADD CONSTRAINT class_instance_class_instance_project_id_fkey
            FOREIGN KEY (project_id) REFERENCES project(id)
            ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;

        -- class_instance
        ALTER TABLE ONLY class_instance
            DROP CONSTRAINT class_instance_project_id_fkey;
        ALTER TABLE ONLY class_instance
            ADD CONSTRAINT class_instance_project_id_fkey
            FOREIGN KEY (project_id) REFERENCES project(id)
            ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;

        -- class
        ALTER TABLE ONLY class
            DROP CONSTRAINT class_project_id_fkey;
        ALTER TABLE ONLY class
            ADD CONSTRAINT class_project_id_fkey
            FOREIGN KEY (project_id) REFERENCES project(id)
            ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;

        -- image_data
        ALTER TABLE ONLY image_data
            DROP CONSTRAINT image_data_project_id_fkey;
        ALTER TABLE ONLY image_data
            ADD CONSTRAINT image_data_project_id_fkey
            FOREIGN KEY (project_id) REFERENCES project(id)
            ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;

        -- interpolatable_section, update Django's constraint name
        EXECUTE 'ALTER TABLE ONLY interpolatable_section '||
            'DROP CONSTRAINT ' || get_fk_constraint_name('interpolatable_section', 'project_id', 'project');
        ALTER TABLE ONLY interpolatable_section
            ADD CONSTRAINT interpolatable_section_project_id_fkey
            FOREIGN KEY (project_id) REFERENCES project(id)
            ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;

        -- location
        ALTER TABLE ONLY location
            DROP CONSTRAINT location_project_id_fkey;
        ALTER TABLE ONLY location
            ADD CONSTRAINT location_project_id_fkey
            FOREIGN KEY (project_id) REFERENCES project(id)
            ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;

        -- nblast_config
        ALTER TABLE ONLY nblast_config
            DROP CONSTRAINT nblast_config_project_id_fkey;
        ALTER TABLE ONLY nblast_config
            ADD CONSTRAINT nblast_config_project_id_fkey
            FOREIGN KEY (project_id) REFERENCES project(id)
            ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;

        -- nblast_sample
        ALTER TABLE ONLY nblast_sample
            DROP CONSTRAINT nblast_sample_project_id_fkey;
        ALTER TABLE ONLY nblast_sample
            ADD CONSTRAINT nblast_sample_project_id_fkey
            FOREIGN KEY (project_id) REFERENCES project(id)
            ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;

        -- nblast_score_container
        ALTER TABLE ONLY nblast_score_container
            DROP CONSTRAINT nblast_score_container_project_id_fkey;
        ALTER TABLE ONLY nblast_score_container
            ADD CONSTRAINT nblast_score_container_project_id_fkey
            FOREIGN KEY (project_id) REFERENCES project(id)
            ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;

        -- reviewer_whitelist, update Django's constraintname
        EXECUTE 'ALTER TABLE ONLY reviewer_whitelist ' ||
            'DROP CONSTRAINT ' || get_fk_constraint_name('reviewer_whitelist', 'project_id', 'project');
        ALTER TABLE ONLY reviewer_whitelist
            ADD CONSTRAINT reviewer_whitelist_project_id_fkey
            FOREIGN KEY (project_id) REFERENCES project(id)
            ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;

        -- textlabel, update Django's constraintname
        EXECUTE 'ALTER TABLE ONLY textlabel ' ||
            'DROP CONSTRAINT ' || get_fk_constraint_name('textlabel', 'project_id', 'project');
        ALTER TABLE ONLY textlabel
            ADD CONSTRAINT textlabel_project_id_fkey
            FOREIGN KEY (project_id) REFERENCES project(id)
            ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;

        -- project_stack, update Django's constraintname
        EXECUTE 'ALTER TABLE ONLY project_stack ' ||
            'DROP CONSTRAINT ' || get_fk_constraint_name('project_stack', 'project_id', 'project');
        ALTER TABLE ONLY project_stack
            ADD CONSTRAINT project_stack_project_id_fkey
            FOREIGN KEY (project_id) REFERENCES project(id)
            ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;

        -- review, update Django's constraintname
        EXECUTE 'ALTER TABLE ONLY review ' ||
            'DROP CONSTRAINT ' || get_fk_constraint_name('review', 'project_id', 'project');
        ALTER TABLE ONLY review
            ADD CONSTRAINT review_project_id_fkey
            FOREIGN KEY (project_id) REFERENCES project(id)
            ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;

        -- client_data, update Django's constraintname
        EXECUTE 'ALTER TABLE ONLY client_data ' ||
            'DROP CONSTRAINT ' || get_fk_constraint_name('client_data', 'project_id', 'project');
        ALTER TABLE ONLY client_data
            ADD CONSTRAINT client_data_project_id_fkey
            FOREIGN KEY (project_id) REFERENCES project(id)
            ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;

        -- catmaid_volume, update Django's constraintname
        EXECUTE 'ALTER TABLE ONLY catmaid_volume ' ||
            'DROP CONSTRAINT ' || get_fk_constraint_name('catmaid_volume', 'project_id', 'project');
        ALTER TABLE ONLY catmaid_volume
            ADD CONSTRAINT catmaid_volume_project_id_fkey
            FOREIGN KEY (project_id) REFERENCES project(id)
            ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;

        -- suppressed_virtual_treenode, update Django's constraintname
        EXECUTE 'ALTER TABLE ONLY suppressed_virtual_treenode ' ||
            'DROP CONSTRAINT ' || get_fk_constraint_name('suppressed_virtual_treenode', 'project_id', 'project');
        ALTER TABLE ONLY suppressed_virtual_treenode
            ADD CONSTRAINT suppressed_virtual_treenode_project_id_fkey
            FOREIGN KEY (project_id) REFERENCES project(id)
            ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;
    END $$;
"""

backward = """
    -- catmaid_sampler, change Django's constraint name
    ALTER TABLE ONLY catmaid_sampler
        DROP CONSTRAINT catmaid_sampler_project_id_fkey;
    ALTER TABLE ONLY catmaid_sampler
        ADD CONSTRAINT catmaid_sampler_project_id_c93395a7_fk_project_id
        FOREIGN KEY (project_id) REFERENCES project(id)
        DEFERRABLE INITIALLY DEFERRED;

    -- catmaid_samplerconnector, change Django's constraint name
    ALTER TABLE ONLY catmaid_samplerconnector
        DROP CONSTRAINT catmaid_samplerconnector_project_id_fkey;
    ALTER TABLE ONLY catmaid_samplerconnector
        ADD CONSTRAINT catmaid_samplerconnector_project_id_01e34db2_fk_project_id
        FOREIGN KEY (project_id) REFERENCES project(id)
        DEFERRABLE INITIALLY DEFERRED;

    -- catmaid_samplerdomain, change Django's constraint name
    ALTER TABLE ONLY catmaid_samplerdomain
        DROP CONSTRAINT catmaid_samplerdomain_project_id_fkey;
    ALTER TABLE ONLY catmaid_samplerdomain
        ADD CONSTRAINT catmaid_samplerdomain_project_id_a6b548dd_fk_project_id
        FOREIGN KEY (project_id) REFERENCES project(id)
        ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;

    -- catmaid_samplerinterval, change Django's constraint name
    ALTER TABLE ONLY catmaid_samplerinterval
        DROP CONSTRAINT catmaid_samplerinterval_project_id_fkey;
    ALTER TABLE ONLY catmaid_samplerinterval
        ADD CONSTRAINT catmaid_samplerinterval_project_id_fee38ad5_fk_project_id
        FOREIGN KEY (project_id) REFERENCES project(id)
        DEFERRABLE INITIALLY DEFERRED;

    -- catmaid_skeleton_summary, change Django's constraint name
    ALTER TABLE ONLY catmaid_skeleton_summary
        DROP CONSTRAINT catmaid_skeleton_summary_project_id_fkey;
    ALTER TABLE ONLY catmaid_skeleton_summary
        ADD CONSTRAINT catmaid_skeleton_summary_project_id_7340fa33_fk_project_id
        FOREIGN KEY (project_id) REFERENCES project(id)
        DEFERRABLE INITIALLY DEFERRED;

    -- catmaid_stats_summary, change Django's constraint name
    ALTER TABLE ONLY catmaid_stats_summary
        DROP CONSTRAINT catmaid_stats_summary_project_id_fkey;
    ALTER TABLE ONLY catmaid_stats_summary
        ADD CONSTRAINT catmaid_stats_summary_project_id_8b6cab99_fk_project_id
        FOREIGN KEY (project_id) REFERENCES project(id)
        DEFERRABLE INITIALLY DEFERRED;

    -- change_request, didn't have constraint before
    ALTER TABLE ONLY change_request
        DROP CONSTRAINT change_request_project_id_fkey;

    -- class_instance_class_instance
    ALTER TABLE ONLY class_instance_class_instance
        DROP CONSTRAINT class_instance_class_instance_project_id_fkey;
    ALTER TABLE ONLY class_instance_class_instance
        ADD CONSTRAINT class_instance_class_instance_project_id_fkey
        FOREIGN KEY (project_id) REFERENCES project(id)
        DEFERRABLE INITIALLY DEFERRED;

    -- class_instance
    ALTER TABLE ONLY class_instance
        DROP CONSTRAINT class_instance_project_id_fkey;
    ALTER TABLE ONLY class_instance
        ADD CONSTRAINT class_instance_project_id_fkey
        FOREIGN KEY (project_id) REFERENCES project(id)
        DEFERRABLE INITIALLY DEFERRED;

    -- class
    ALTER TABLE ONLY class
        DROP CONSTRAINT class_project_id_fkey;
    ALTER TABLE ONLY class
        ADD CONSTRAINT class_project_id_fkey
        FOREIGN KEY (project_id) REFERENCES project(id)
        DEFERRABLE INITIALLY DEFERRED;

    -- image_data
    ALTER TABLE ONLY image_data
        DROP CONSTRAINT image_data_project_id_fkey;
    ALTER TABLE ONLY image_data
        ADD CONSTRAINT image_data_project_id_fkey
        FOREIGN KEY (project_id) REFERENCES project(id)
        ON DELETE CASCADE;

    -- interpolatable_section, update Django's constraint name
    ALTER TABLE ONLY interpolatable_section
        DROP CONSTRAINT interpolatable_section_project_id_fkey;
    ALTER TABLE ONLY interpolatable_section
        ADD CONSTRAINT interpolatable_section_project_id_d504b3eb_fk_project_id
        FOREIGN KEY (project_id) REFERENCES project(id)
        DEFERRABLE INITIALLY DEFERRED;

    -- location
    ALTER TABLE ONLY location
        DROP CONSTRAINT location_project_id_fkey;
    ALTER TABLE ONLY location
        ADD CONSTRAINT location_project_id_fkey
        FOREIGN KEY (project_id) REFERENCES project(id)
        DEFERRABLE INITIALLY DEFERRED;

    -- nblast_config
    ALTER TABLE ONLY nblast_config
        DROP CONSTRAINT nblast_config_project_id_fkey;
    ALTER TABLE ONLY nblast_config
        ADD CONSTRAINT nblast_config_project_id_fkey
        FOREIGN KEY (project_id) REFERENCES project(id)
        ON DELETE CASCADE;

    -- nblast_sample
    ALTER TABLE ONLY nblast_sample
        DROP CONSTRAINT nblast_sample_project_id_fkey;
    ALTER TABLE ONLY nblast_sample
        ADD CONSTRAINT nblast_sample_project_id_fkey
        FOREIGN KEY (project_id) REFERENCES project(id)
        ON DELETE CASCADE;

    -- nblast_score_container
    ALTER TABLE ONLY nblast_score_container
        DROP CONSTRAINT nblast_score_container_project_id_fkey;
    ALTER TABLE ONLY nblast_score_container
        ADD CONSTRAINT nblast_score_container_project_id_fkey
        FOREIGN KEY (project_id) REFERENCES project(id)
        ON DELETE CASCADE;

    -- reviewer_whitelist, update Django's constraintname
    ALTER TABLE ONLY reviewer_whitelist
        DROP CONSTRAINT reviewer_whitelist_project_id_fkey;
    ALTER TABLE ONLY reviewer_whitelist
        ADD CONSTRAINT project_id_refs_id_2779ef3d
        FOREIGN KEY (project_id) REFERENCES project(id)
        DEFERRABLE INITIALLY DEFERRED;

    -- textlabel, update Django's constraintname
    ALTER TABLE ONLY textlabel
        DROP CONSTRAINT textlabel_project_id_fkey;
    ALTER TABLE ONLY textlabel
        ADD CONSTRAINT project_id_refs_id_71989805
        FOREIGN KEY (project_id) REFERENCES project(id)
        DEFERRABLE INITIALLY DEFERRED;

    -- project_stack, update Django's constraintname
    ALTER TABLE ONLY project_stack
        DROP CONSTRAINT project_stack_project_id_fkey;
    ALTER TABLE ONLY project_stack
        ADD CONSTRAINT project_id_refs_id_73ad1fa9
        FOREIGN KEY (project_id) REFERENCES project(id)
        DEFERRABLE INITIALLY DEFERRED;

    -- review, update Django's constraintname
    ALTER TABLE ONLY review
        DROP CONSTRAINT review_project_id_fkey;
    ALTER TABLE ONLY review
        ADD CONSTRAINT project_id_refs_id_8650befd
        FOREIGN KEY (project_id) REFERENCES project(id)
        DEFERRABLE INITIALLY DEFERRED;

    -- client_data, update Django's constraintname
    ALTER TABLE ONLY client_data
        DROP CONSTRAINT client_data_project_id_fkey;
    ALTER TABLE ONLY client_data
        ADD CONSTRAINT project_id_refs_id_bcd3fbdc
        FOREIGN KEY (project_id) REFERENCES project(id)
        DEFERRABLE INITIALLY DEFERRED;

    -- catmaid_volume, update Django's constraintname
    ALTER TABLE ONLY catmaid_volume
        DROP CONSTRAINT catmaid_volume_project_id_fkey;
    ALTER TABLE ONLY catmaid_volume
        ADD CONSTRAINT project_id_refs_id_c0c82ac5
        FOREIGN KEY (project_id) REFERENCES project(id)
        DEFERRABLE INITIALLY DEFERRED;

    -- suppressed_virtual_treenode, update Django's constraintname
    ALTER TABLE ONLY suppressed_virtual_treenode
        DROP CONSTRAINT suppressed_virtual_treenode_project_id_fkey;
    ALTER TABLE ONLY suppressed_virtual_treenode
        ADD CONSTRAINT project_id_refs_id_cb81a05a
        FOREIGN KEY (project_id) REFERENCES project(id)
        DEFERRABLE INITIALLY DEFERRED;
"""

class Migration(migrations.Migration):

    dependencies = [
        ('catmaid', '0063_add_additional_neuron_similarity_fields'),
    ]

    operations = [
        migrations.RunSQL(forward, backward),
    ]
