import sqlite3
from pathlib import Path

settings_path = Path("settings.sqlite")


class DatabaseConnection:
    def __init__(self, db_name=settings_path):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection is not None:
            self.connection.close()
        else:
            print("No connection to close.")

    def connect(self):
        try:
            # Check if table is created if not create it
            if not settings_path.is_file():
                self.create_table()
            # Connect to the SQLite database
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
        except sqlite3.Error as e:
            print(f"Error connecting to SQLite database: {e}")

    def create_table(self):
        # Connect to the SQLite database (creates the file if it doesn't exist)
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        if self.cursor is not None:
            try:
                # table creation query with default values
                create_table_query = """
                    CREATE TABLE IF NOT EXISTS settings (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        language TEXT NOT NULL DEFAULT 'EN',
                        font_weight TEXT NOT NULL DEFAULT 'NORMAL',
                        text_colour TEXT NOT NULL DEFAULT '#000000',
                        widget_colour TEXT NOT NULL DEFAULT '#ffffff',
                        widget_x_position INTEGER NOT NULL DEFAULT 1155,
                        widget_y_position INTEGER NOT NULL DEFAULT 201,
                        option_window_x_position INTEGER NOT NULL DEFAULT 1370,
                        option_window_y_position INTEGER NOT NULL DEFAULT 50,
                        data_window_x_position INTEGER NOT NULL DEFAULT 0.0,
                        data_window_y_position INTEGER NOT NULL DEFAULT 0.0,
                        opacity TEXT NOT NULL DEFAULT '80%',
                        reciever_email TEXT,
                        date_last_warning TEXT,
                        warning_period INTEGER,
                        send_warning_email BOOLEAN
                    );                
                    """

                insert_data_query = """
                    INSERT INTO settings (
                        language, font_weight, text_colour,
                        widget_colour, widget_x_position, widget_y_position,
                        option_window_x_position, option_window_y_position,
                        data_window_x_position, data_window_y_position,
                        opacity, reciever_email, date_last_warning, 
                        warning_period, send_warning_email
                    ) VALUES (
                        'EN', 'NORMAL', '#000000', '#ffffff', 1155, 201, 1370, 50, 0.0, 0.0, '80%', ' ', 01-jan-2022, 1, 1
                    );
                    """

                self.cursor.execute(create_table_query)
                self.cursor.execute(insert_data_query)
                self.connection.commit()
                print("Table 'settings' created successfully")
            except sqlite3.Error as e:
                print(f"Error creating table: {e}")
        else:
            print("Not connected to a database. Call 'connect' method first.")

    def get_settings(self, key=None):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()

        try:
            # Fetch all rows from the 'settings' table
            cursor.execute("SELECT * FROM settings")
            rows = cursor.fetchall()

            # Get column names
            column_names = [description[0] for description in cursor.description]

            # Create a list of dictionaries with column names as keys and values as values
            result = [
                {column_names[i]: row[i] for i in range(len(column_names))}
                for row in rows
            ]
            # if getting specific key return only value
            if key is not None:
                return result[0][key]
            else:
                return result
        except sqlite3.Error as e:
            print(f"Error reading settings: {e}")

    def update_row(self, row_id, values):
        if self.cursor is not None:
            try:
                # Construct the UPDATE query dynamically based on the provided values
                update_query = "UPDATE settings SET "
                update_values = []

                for key, value in values.items():
                    update_query += f"{key} = ?, "
                    update_values.append(value)

                # Remove the trailing comma and space
                update_query = update_query.rstrip(", ")

                # Add the WHERE clause to update the specific row
                update_query += f" WHERE id = ?"
                update_values.append(row_id)

                # Execute the update query
                self.cursor.execute(update_query, tuple(update_values))
                self.connection.commit()
            except sqlite3.Error as e:
                print(f"Error updating row: {e}")
        else:
            print("Not connected to a database. Call 'connect' method first.")


# If the settings.sqlite is deleted run this db_connection.py to create the sqlite table again with default values
if __name__ == "__main__":
    ...
    # # Using the 'with' statement automatically manages the connection
    # with DatabaseConnection() as db_connection:
    #     # Connect to the SQLite database
    #     db_connection.connect()

    #     # Create a table in the database
    #     db_connection.create_table()
    # Connection is automatically closed when exiting the 'with' block

    # # Inserting some dummy data for testing
    # with sqlite3.connect("settings.sqlite") as connection:
    #     cursor = connection.cursor()
    #     cursor.execute(
    #         "INSERT INTO settings (language, font_weight, text_colour) VALUES (?, ?, ?)",
    #         ("EN", "BOLD", "#ff0000"),
    #     )
    #     connection.commit()

    # # Reading and printing settings
    # dbc = DatabaseConnection()
    # settings = dbc.get_settings()
    # print(settings)

    # # Updating values for row with ID 1
    # update_values = {"font_weight": "NORMAL", "text_colour": "#00ff00"}
    # db_connection.update_row(1, update_values)

    # # Reading and printing settings after update
    # settings_after_update = db_connection.get_settings()
    # print("\nSettings after update:")
    # print(settings_after_update)

    # Getting specific value "font_weight"
    # font_weight = db_connection.get_settings("font_weight")
    # print(font_weight)
