import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def UserRegister(conn, username, password):
    insert_user_query = "INSERT INTO users VALUES (?, ?)"
    c = conn.cursor()
    c.execute(insert_user_query, (username, password))
    conn.commit()
    return (username, password)


def main():
    database = r"E:\Long\Web\Flask\database\data.db"
    create_table_query = "CREATE TABLE users (username text PRIMARY KEY, password text)"

    # create a database connection
    conn = create_connection(database)

    # create table
    if conn is not None:
        create_table(conn, create_table_query)
    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    # main()
    conn = create_connection(r"E:\Long\Web\Flask\database\data.db")
    UserRegister(conn, username='admin', password='admin')
