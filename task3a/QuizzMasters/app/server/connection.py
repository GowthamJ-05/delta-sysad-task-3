import mysql.connector.errors


class Connection:
    def __init__(self, pool):
        self.pool = pool
        self.conn = self.pool.get_connection()
        self.cursor = self.conn.cursor()

    def accept_query(self, query, placeholders=tuple()):
        self.cursor.execute(query, placeholders)
        try:
            result = self.cursor.fetchall()
            self.conn.commit()
            if len(result) > 1:
                return result
            elif len(result) == 0:
                return None
            else:
                return result[0]
        except mysql.connector.errors.InterfaceError as e:
            print(f"Error: Connecting to database: {e}")
            self.conn.commit()
            return

