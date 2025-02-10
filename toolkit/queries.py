def query_challenges():
    """Return the total number of newly-created user accounts in Synapse for each year."""

    return """
    WITH syn_users AS (
        SELECT
            id,
            user_name
        FROM
            synapse_data_warehouse.synapse.userprofile_latest
    )
    SELECT
        DATE(created_on) as date,
        user_name AS project_creator,
        name,
        project_id
    FROM
        synapse_data_warehouse.synapse.node_latest
    LEFT JOIN
        syn_users
    ON syn_users.id = created_by
    WHERE
        node_type = 'project'
        AND name LIKE ANY('%Challenge', 'BraTS ____' ,'FeTS% ____')
        AND is_public
    ORDER BY date DESC
    """
