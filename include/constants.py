"Contains constants used in the DAGs"

import os
from cosmos import ExecutionConfig

DBT_PROJECT_PATH = f"{os.environ['AIRFLOW_HOME']}/dags/dbt/retail_dbt"
DBT_EXECUTABLE_PATH = f"{os.environ['AIRFLOW_HOME']}/dbt_venv/bin/dbt"

venv_execution_config = ExecutionConfig(
    dbt_executable_path=str(DBT_EXECUTABLE_PATH),
)