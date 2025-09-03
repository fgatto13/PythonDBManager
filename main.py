import json
from datetime import date, datetime

from DBManager import DBManager

def load_config(path="ConnectionVariables.json"):
    with open(path, "r") as f:
        return json.load(f)

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


if __name__ == "__main__":
    main()