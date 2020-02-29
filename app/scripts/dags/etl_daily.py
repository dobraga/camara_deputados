import sys
sys.path.append('/app/scripts/deputados/')

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

from datetime import datetime, timedelta

from fetcher import extrai
from loader import load
from settings import Settings

conf = Settings()

# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'Douglas Braga',
    'schedule_interval': '@daily',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email': ['douglasmartinsbraga@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=1)
}

def _print_context(**context):
    print(context)

with DAG('ETL', default_args=default_args, description='Processo diário para extração, carga e transformação', catchup=False) as dag:
    print_context = PythonOperator(
        task_id="print_context",
        python_callable=_print_context,
        provide_context=True,
        dag=dag
    )

    ext_partidos = PythonOperator(
        task_id='ext_partidos',
        python_callable=extrai,
        op_kwargs={'conf': conf, 'query': 'partidos'},
        dag=dag,
        provide_context=True
    )

    ext_partidos_det = PythonOperator(
        task_id='ext_partidos_det',
        python_callable=extrai,
        op_kwargs={'conf': conf, 'query': 'partidos_det'},
        dag=dag,
        provide_context=True
    )

    ext_partidos_membros = PythonOperator(
        task_id='ext_partidos_membros',
        python_callable=extrai,
        op_kwargs={'conf': conf, 'query': 'partidos_membros'},
        dag=dag,
        provide_context=True
    )

    ext_deputados = PythonOperator(
        task_id='ext_deputados',
        python_callable=extrai,
        op_kwargs={'conf': conf, 'query': 'deputados'},
        dag=dag,
        provide_context=True
    )

    load_partidos = PythonOperator(
        task_id='load_partidos',
        python_callable=load,
        op_kwargs={'conf': conf, 'file': 'partidos_det'},
        dag=dag,
        provide_context=True
    )

    load_deputados = PythonOperator(
        task_id='load_deputados',
        python_callable=load,
        op_kwargs={'conf': conf, 'file': 'deputados'},
        dag=dag,
        provide_context=True
    )


print_context >> ext_partidos >> [ext_partidos_det, ext_partidos_membros]
ext_partidos_membros >> ext_deputados >> load_deputados 
ext_partidos_det >> load_partidos
