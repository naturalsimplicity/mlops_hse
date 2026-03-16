from __future__ import annotations
from airflow.decorators import dag
from airflow.operators.python import PythonOperator
from pendulum import datetime

def _print(msg: str):
    print(msg)

@dag(
    dag_id="deps_dag",
    schedule=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["demo"],
)
def deps_dag():
    t1 = PythonOperator(task_id="extract", python_callable=_print, op_args=["extract ok"])
    t2 = PythonOperator(task_id="transform", python_callable=_print, op_args=["transform ok"])
    t3 = PythonOperator(task_id="load", python_callable=_print, op_args=["load ok"])

    t1 >> t2 >> t3

deps_dag()
