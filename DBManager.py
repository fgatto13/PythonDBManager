from datetime import date, datetime

import mysql.connector

class DBManager:
    # static queries
    _Q_INSERT_EVENT = """
                      INSERT INTO Event (name, description, t_date, category)
                      VALUES (%s, %s, %s, %s) \
                      """
    _Q_SELECT_TODAY = """
                      SELECT e.id, e.name, e.t_date, e.description, c.name
                      FROM Event AS e
                               LEFT JOIN Category c ON e.category = c.id
                      WHERE DATE(e.t_date) = %s \
                      """
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

        self.conn = None
        self.cursor = None

        self._create_connection()
        self._init_db()

    def _create_connection(self):
        try:
            # initial connection (without selecting DB, just in case DB doesn't exist yet)
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            self.cursor = self.conn.cursor()
        except mysql.connector.Error as err:
            raise Exception(f"Error connecting to MySQL: {err}")

    def _init_db(self):
        # ensure database exists
        self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
        self.cursor.execute(f"USE {self.database}")

        # load schema file
        with open("dbconfig.sql", "r") as f:
            sql_script = f.read()

        for statement in sql_script.split(";"):
            if statement.strip():
                self.cursor.execute(statement)

        self.conn.commit()

    # Now, let's define some CRUD operations

    def add_new(self, name: str, description: str, t_date: datetime, category: int = None):
        self.cursor.execute(self._Q_INSERT_EVENT, (name, description, t_date, category))
        self.conn.commit()
        print(f"Added new event {name} with description {description}")

    def select_all_from_today(self, today: date):
        self.cursor.execute(self._Q_SELECT_TODAY, (today,))
        return self.cursor.fetchall()