FROM astrocrpublic.azurecr.io/runtime:3.0-1

WORKDIR "/usr/local/airflow"
COPY requirements.txt ./
RUN python -m virtualenv dbt_venv && source dbt_venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt && deactivate
