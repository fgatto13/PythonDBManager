from datetime import date, datetime

import mysql.connector

class DBManager:
    # static queries for event
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
    _Q_UPDATE_EVENT = """
                      UPDATE Event
                      SET name        = %s, \
                          description = %s, \
                          t_date      = %s, \
                          category    = %s
                      WHERE id = %s \
                      """
    _Q_DELETE_EVENT = "DELETE FROM Event WHERE id = %s"
    _Q_SELECT_EVENTS = "SELECT * FROM Event"

    # static queries for Category
    _Q_INSERT_CATEGORY = "INSERT INTO Category (name) VALUES (%s)"
    _Q_SELECT_ALL_CATEGORIES = "SELECT * FROM Category"
    _Q_UPDATE_CATEGORY = "UPDATE Category SET name = %s WHERE id = %s"
    _Q_DELETE_CATEGORY = "DELETE FROM Category WHERE id = %s"

    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

        self.conn = None
        self.cursor = None

        self._create_connection()
        self._init_db()

    # private function to create the connection
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

    # private function to initialize the db using the config file
    def _init_db(self):
        # ensure database exists
        self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
        self.cursor.execute(f"USE {self.database}")

        # load schema file
        with open("config/dbconfig.sql", "r") as f:
            sql_script = f.read()

        for statement in sql_script.split(";"):
            if statement.strip():
                self.cursor.execute(statement)

        self.conn.commit()

    # Now, let's define some CRUD operations

    def add_new_event(self, name: str, description: str, t_date: datetime, category: int = None):
        self.cursor.execute(self._Q_INSERT_EVENT, (name, description, t_date, category))
        self.conn.commit()
        print(f"Added new event {name} with description {description}")

    def select_all_from_today(self, today: date):
        self.cursor.execute(self._Q_SELECT_TODAY, (today,))
        return self.cursor.fetchall()

    def update_event(self, event_id: int, name: str, description: str, t_date: datetime, category: int = None):
        self.cursor.execute(self._Q_UPDATE_EVENT, (name, description, t_date, category, event_id))
        self.conn.commit()
        print(f"Updated event with ID {event_id}")

    def delete_event(self, event_id: int):
        self.cursor.execute(self._Q_DELETE_EVENT, (event_id,))
        self.conn.commit()
        print(f"Deleted event with ID {event_id}")

    def select_all_events(self):
        self.cursor.execute(self._Q_SELECT_EVENTS)
        return self.cursor.fetchall()

    # And some CRUD operations for category, too

    def add_category(self, name: str):
        self.cursor.execute(self._Q_INSERT_CATEGORY, (name,))
        self.conn.commit()
        print(f"Added category '{name}'")

    def get_all_categories(self):
        self.cursor.execute(self._Q_SELECT_ALL_CATEGORIES)
        return self.cursor.fetchall()

    def update_category(self, category_id: int, new_name: str):
        self.cursor.execute(self._Q_UPDATE_CATEGORY, (new_name, category_id))
        self.conn.commit()
        print(f"Updated category ID {category_id} → '{new_name}'")

    def delete_category(self, category_id: int):
        self.cursor.execute(self._Q_DELETE_CATEGORY, (category_id,))
        self.conn.commit()
        print(f"Deleted category with ID {category_id}")
