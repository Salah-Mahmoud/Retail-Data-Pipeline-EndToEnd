"Contains profile mappings used in the project"

import os
from cosmos import ProfileConfig

airflow_db = ProfileConfig(
    profile_name="default",
    target_name="dev",
    profiles_yml_filepath=f"{os.environ['AIRFLOW_HOME']}/dags/dbt/retail_dbt/profiles.yml"
)
