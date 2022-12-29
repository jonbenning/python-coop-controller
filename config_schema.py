from schema import Schema, SchemaError, Optional

def check(yaml):
    base_schema = Schema({
        "pins": dict,
        "location": dict,
        "schedule": dict,
        "pushover": dict
    })

    pins_schema = Schema({
        "open_limit": int,
        "close_limit": int,
        "obs_limit": int
    })

    location_schema = Schema({
        "latitude": float,
        "longitude": float
    })

    schedule_schema = Schema({
        "sunrise_offset": int,
        "sunset_offset": int
    })

    pushover_schema = Schema({
        "app_token": str,
        "group_key": str
    })

    try:
        base_schema.validate(yaml)
        pins_schema.validate(yaml['pins'])
        location_schema.validate(yaml['location'])
        schedule_schema.validate(yaml['schedule'])
        pushover_schema.validate(yaml['pushover'])
    except SchemaError as e:
        raise e

    return True
