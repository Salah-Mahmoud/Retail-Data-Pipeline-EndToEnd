from cosmos import DbtDag, ProjectConfig
from include.profiles import airflow_db
from include.constants import DBT_PROJECT_PATH, venv_execution_config

simple_dag = DbtDag(
    project_config=ProjectConfig(DBT_PROJECT_PATH),
    profile_config=airflow_db,
    execution_config=venv_execution_config,
    schedule="@daily",
    catchup=False,
    dag_id="retail_dag"
)