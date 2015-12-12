import psycopg2


def get_postsql_server_port():
    return 5432


def wait_for_postgres_sql():
    retry_cnt = 0
    # Define our connection string
    conn_string = "host='localhost' dbname='postgres' user='postgres' password=''"
    conn_string += " port='%d'" % get_postsql_server_port()
    while True:
        try:
            # get a connection, if a connect cannot be made an exception will be raised here
            conn = psycopg2.connect(conn_string)
            break
        except psycopg2.OperationalError:
            retry_cnt += 1
            print "retrying to connect postgresql server"
            if retry_cnt > 80:
                print "postgresql start failed"
                break
