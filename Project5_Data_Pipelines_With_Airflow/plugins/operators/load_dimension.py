from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 table="",
                 select_sql="",
                 append_data=True,
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.select_sql = select_sql
        self.append_data = append_data

    def execute(self, context):
        # self.log.info('LoadDimensionOperator not implemented yet')

        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        self.log.info("INSERT data from staging table to dim table")
        if self.append_data == False:
            redshift.run("TRUNCATE TABLE {}".format(self.table))
        redshift.run("INSERT INTO {} ({})".format(self.table, self.select_sql))