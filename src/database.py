import sqlite3


class GladiatusDB:
    def __init__(self, table, db_name="gladiatus.db"):
        """Initialize the SQLite database connection."""
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.table = table

    def create_table(self):
        """Create a table in the database."""
        self.cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {self.table} (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            server TEXT NOT NULL,
            link_player TEXT NOT NULL,
            link_battle TEXT NOT NULL,
            date_attack TEXT NOT NULL,
            gold INTEGER NOT NULL
        )
        ''')
        self.conn.commit()

    def insert_player(self, player):
        """Insert a new user into the users table."""
        command = f'''
            INSERT INTO {self.table} 
            VALUES (?, ?, ?, ?, ?, ?, ?)
            '''
        values = (
                player["id"],
                player["name"],
                player["server"],
                player["link_player"],
                player["link_battle"],
                player["date_attack"],
                player["gold"]
                                )
        try:
            self.cursor.execute(command, values)
        except sqlite3.IntegrityError:
            self.cursor.execute(f'DELETE FROM {self.table} where id = "{player["id"]}"')
            self.cursor.execute(command, values)
        self.conn.commit()

    def query_players(self):
        """Query all users from the users table."""
        self.cursor.execute(f'SELECT * FROM {self.table} order by gold')
        return self.cursor.fetchall()


    def close(self):
        """Close the database connection."""
        self.conn.close()

