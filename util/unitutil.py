from config.config_init import config


units = {
    "K": 0,
    "M": 1,
    "G": 2
}


def get_power_index():
    try:
        target_unit = config.get("common", "print_unit")
    except:
        target_unit = 'M'
    index = units[target_unit]
    return target_unit, index
