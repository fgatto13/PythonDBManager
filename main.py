import json
from datetime import date, datetime

from DBManager import DBManager

def load_config(path="config/ConnectionVariables.json"):
    with open(path, "r") as f:
        return json.load(f)

def menu_selection(dbmanager: DBManager):
    flag = True
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
                    name = input("Name: ")
                    description = input("Description: ")
                    t_date = datetime.fromisoformat(input("Date: "))
                    category = int(input("Category: "))
                    dbmanager.add_new_event(name=name, description=description, t_date=t_date, category=category)
                case 2:
                    dbmanager.update_event()
                case 3:
                    dbmanager.delete_event()
                case 4:
                    events = dbmanager.select_all_events()
                    if events:
                        for (event_id, name, t_date, description, category_name) in events:
                            print(f"[{t_date.strftime('%Y-%m-%d %H:%M')}] {name}")
                            if description:
                                print(f"   Note: {description}")
                            print(f"   Category: {category_name}\n")
                    else:
                        print("No planned events.")
                case _:
                    flag = False
                    print("Exiting...")
        except ValueError:
            print("Please enter an integer")
            menu_selection(dbmanager)


def main():
    # loads the config file data
    config = load_config()

    # creates the dbmanager object
    dbmanager = DBManager(
        host=config.get("host"),
        user=config.get("user"),
        password=config.get("password"),
        database=config.get("database")
    )

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
    menu_selection(dbmanager)

if __name__ == "__main__":
    main()