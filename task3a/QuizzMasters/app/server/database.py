import os
import socket
import mysql.connector.pooling


pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=int(os.getenv("MYSQL_POOL_SIZE")),
    database=os.getenv("MYSQL_DATABASE"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_ROOT_PASSWORD"),
    host=socket.gethostbyname(os.getenv("MYSQL_HOST")),
    port=os.getenv("MYSQL_PORT")
)

