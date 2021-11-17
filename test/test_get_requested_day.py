import datetime

def get_requested_day(day_slot: str, is_next_week: bool) -> datetime.date:
    
    day_of_week = datetime.date.today().weekday()
    day_name = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']
    today = datetime.date.today()

    if day_slot == "Heute":
        return today
    elif day_slot == "Morgen":
        return today + datetime.timedelta(days = 1) # return date of tomorrow
    elif day_slot == "Übermorgen":
        return today + datetime.timedelta(days = 2) # return date of tomorrow

    # day_slot is in Montag, ..., Sonntag

    requested_slot_number = day_name.index(day_slot)

    # requested day is in the next week (e.g. today is Mittwoch and Montag is requested)
    if (requested_slot_number < day_of_week):
        is_next_week = True

    if not is_next_week:
        # return date that is part of the current week
        return today + datetime.timedelta(days = requested_slot_number - day_of_week)
    else:
        # return date that is part of the next week
        return today + datetime.timedelta(days = 7 - day_of_week + day_name.index(day_slot))

if __name__ == "__main__":
    print(get_requested_day("Übermorgen", False))