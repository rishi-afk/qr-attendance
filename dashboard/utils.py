def validate_time_table(cleaned_data):
    errors = []
    monday = [(o.start, o.end) for o in cleaned_data.get("monday")]
    tuesday = [(o.start, o.end) for o in cleaned_data.get("tuesday")]
    wednesday = [(o.start, o.end) for o in cleaned_data.get("wednesday")]
    thursday = [(o.start, o.end) for o in cleaned_data.get("thursday")]
    friday = [(o.start, o.end) for o in cleaned_data.get("friday")]
    if (len(monday) != len(set(monday))):
        errors.append("Monday")
    if (len(tuesday) != len(set(tuesday))):
        errors.append("Tuesday")
    if (len(wednesday) != len(set(wednesday))):
        errors.append("Wednesday")
    if (len(thursday) != len(set(thursday))):
        errors.append("Thursday")
    if (len(friday) != len(set(friday))):
        errors.append("Friday")
    return errors
