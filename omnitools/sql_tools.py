from typing import Union, Optional
from pyodbc import connect, Connection
from pandas import read_sql_query


user_authentication='ActiveDirectoryInteractive'
def get_edge_sql_connection(username:str, server:str, database:str, authentication:str=user_authentication,
                            driver:str='{ODBC Driver 17 for SQL Server}') -> Connection:
    return connect(DRIVER=driver, Authentication=authentication,
                   SERVER=server, DATABASE=database, UID=username)


def build_sql_query_str(select:Union[str, list], table:str, where:Optional[Union[str, list]]=None) -> str:
    # add SELECT data
    select = [select] if isinstance(select, str) else select
    sql_query = "SELECT " + ", ".join(select)
    # add FROM database
    sql_query += f" FROM {table}"
    # add WHERE condition to sql_query
    if where is not None:
        where = [where] if isinstance(where, str) else where
        sql_query += f" WHERE " + " AND ".join(where)

    return sql_query


def columns_of_a_sql_table(table:str, connection) -> list:

    select_sql = "TOP(0)*"
    sql_query = build_sql_query_str(select=select_sql, table=table)
    df = read_sql_query(sql_query, connection)

    return df.columns.tolist()


