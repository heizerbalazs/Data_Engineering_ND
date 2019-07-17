from cassandra.cluster import Cluster
from cql_queries import create_table_queries, drop_table_queries


def create_database():
    """
    This function connects to an Apache Cassandra cluster.
    
    Inputs:
    -------
    This function does not have any inputs.
    
    Outputs:
    -------
    cluster - object represents the Apache Cassandra cluster
    session - object represents the connection to the cluster
    """
    
    # connect to default database
    cluster = Cluster()
    session = cluster.connect()
    
    session.execute("DROP KEYSPACE IF EXISTS sparkifydb")
    
    # create sparkify database with UTF8 encoding
    session.execute("CREATE KEYSPACE IF NOT EXISTS sparkifydb \
                 WITH REPLICATION = { \
                                     'class' : 'SimpleStrategy', \
                                     'replication_factor' : 1 \
                                     }")
    
    session.set_keyspace("sparkifydb")
    
    return cluster, session


def drop_tables(session):
    """
    This function execute the queries listed in the drop_table_queries list.
    
    Inputs:
    -------
    session - object represents the Apache Cassandra cluster connection
    
    Outputs:
    --------
    This function does not return anything.
    """
    for query in drop_table_queries:
        session.execute(query)


def create_tables(session):
    """
    This function execute the queries listed in the create_table_queries list.
    
    Inputs:
    -------
    session - object represents the Apache Cassandra cluster connection
    
    Outputs:
    --------
    This function does not return anything.
    """
    for query in create_table_queries:
        session.execute(query)

def main():
    cluster, session = create_database()
    
    drop_tables(session)
    create_tables(session)

    cluster.shutdown()
    session.shutdown()


if __name__ == "__main__":
    main()