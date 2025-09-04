import json
from datetime import date, datetime

from DBManager import DBManager
class Main:
    @staticmethod
    def load_config(path="config/ConnectionVariables.json"):
        with open(path, "r") as f:
            return json.load(f)

    @staticmethod
    def menu_selection(dbmanager: DBManager):
        flag = True
        # Retrieves today's events
        today = date.today()  # only YYYY-MM-DD
        events = dbmanager.select_all_from_today(today)
        # and prints them
        print("Today's events:")
        if events:
            for (event_id, name, t_date, description, category_name) in events:
                print(f"[{t_date.strftime('%Y-%m-%d %H:%M')}] {name}")
                if description:
                    print(f"   Note: {description}")
                print(f"   Category: {category_name}\n")
        else:
            print("No planned events today.")

        while flag:
            print("Select an option:")
            print("---------------------")
            print("1. Create a new event")
            print("2. Update an event")
            print("3. Delete an event")
            print("4. View all events")
            print("5. Exit")
            print("---------------------")
            try:
                choice = int(input("> "))
                match choice:
                    case 1:
                        print("Create a new event")
                        name = input("Name: ")
                        description = input("Description: ")
                        t_date = datetime.fromisoformat(input("Date: "))
                        print("Category IDs: ")
                        for cat in dbmanager.get_all_categories():
                            print("ID: ", cat[0], " Name: ", cat[1])
                        category = int(input("Category: "))
                        dbmanager.add_new_event(
                            name=name,
                            description=description,
                            t_date=t_date,
                            category=category
                        )
                    case 2:
                        in_flag = False
                        in_event_id = int(input("insert event ID: "))
                        events = dbmanager.select_all_events()
                        for event in events:
                            if in_event_id == event[0]:
                                in_flag = True
                                break
                            else:
                                continue
                        if in_flag:
                            name = input("Insert new Name: ")
                            description = input("Insert new Description: ")
                            t_date = datetime.fromisoformat(input("Insert new Date: "))
                            dbmanager.update_event(event_id, name, description, t_date)
                        else:
                            print("Event not found.")
                    case 3:
                        in_flag = False
                        in_event_id = int(input("insert event ID: "))
                        events = dbmanager.select_all_events()
                        for event in events:
                            if in_event_id == event[0]:
                                in_flag = True
                                break
                            else:
                                continue
                        if in_flag:
                            dbmanager.delete_event(in_event_id)
                        else:
                            print("Event not found")
                    case 4:
                        events = dbmanager.select_all_events()
                        if events:
                            for (event_id, name, t_date, description, category_name) in events:
                                print(f"[{t_date.strftime('%Y-%m-%d %H:%M')}] {name}")
                                if description:
                                    print(f"   Note: {description}")
                                print(f"   Category: {category_name}")
                                print(f"   ID: {event_id}\n")
                        else:
                            print("No planned events.")
                    case _:
                        flag = False
                        print("Exiting...")
            except ValueError:
                print("Please enter an integer")
                Main.menu_selection(dbmanager)

    @staticmethod
    def main():
        # loads the config file data
        config = Main.load_config()

        # creates the dbmanager object
        dbmanager = DBManager(
            host=config.get("host"),
            user=config.get("user"),
            password=config.get("password"),
            database=config.get("database")
        )
        Main.menu_selection(dbmanager)

if __name__ == "__main__":
    Main.main()