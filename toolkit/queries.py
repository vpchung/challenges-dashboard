import re

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


def query_challenge_info(syn_id):
    syn_id = re.search(r"^(syn)?(\d{1,8})$", syn_id).group(2)
    return f"""
    SELECT
        name
    FROM
        synapse_data_warehouse.synapse.node_latest
    WHERE
        project_id = {syn_id} AND
        node_type = 'project'
    LIMIT 1
    """


def query_data_download_counts(syn_id):
    """Return the number of data downloads for a given challenge."""

    syn_id = re.search(r"^(syn)?(\d{1,8})$", syn_id).group(2)
    return f"""
    WITH challenge_files AS (
        SELECT
            id AS node_id,
            name as filename,
            file_handle_id
        FROM
            synapse_data_warehouse.synapse.node_latest
        WHERE
            project_id = {syn_id} AND
            node_type = 'file' AND
            name NOT LIKE '%_logs.zip' AND
            name NOT LIKE '%_log.txt' AND
            name NOT LIKE '%_docker.log' AND
            name NOT LIKE '%predictions.%' AND
            name NOT LIKE 'mlcube.yaml' AND
            name NOT LIKE 'parameters.yaml' AND
            name NOT LIKE 'additional_files.tar.gz' AND
            name NOT LIKE '%scores.csv'
    ), dedup_download_records AS (
        SELECT
            DISTINCT user_id, file_handle_id, record_date
        FROM
            synapse_data_warehouse.synapse.filedownload
        WHERE
            project_id = {syn_id}
    ), downloads AS (
        SELECT
            *
        FROM
            challenge_files
        LEFT JOIN
            dedup_download_records
        ON
            challenge_files.file_handle_id = dedup_download_records.file_handle_id
    )

    SELECT
        node_id,
        MAX(filename) AS filename,
        COUNT(record_date) AS number_of_downloads
    FROM
        downloads
    GROUP BY
        node_id
    ORDER BY
        number_of_downloads DESC;
    """
