import os
from utils import log_error, log_info
import subprocess
import countryflag

CONFIG_DIR = "configs"
ISO_NAMES = [{"PE": "Peru"}, {"TH": "Thailand"}, {"PK": "Pakistan"}, {"LU": "Luxembourg"}, {"SI": "Slovenia"}, {"HU": "Hungary"}, {"SK": "Slovakia"}, {"IS": "Iceland"}, {"SE": "Sweden"}, {"KR": "South Korea"}, {"TW": "Taiwan"}, {"AE": "United Arab Emirates"}, {"PL": "Poland"}, {"HR": "Croatia"}, {"MD": "Moldova"}, {"AR": "Argentina"}, {"SG": "Singapore"}, {"RS": "Serbia"}, {"BG": "Bulgaria"}, {"IE": "Ireland"}, {"GR": "Greece"}, {"RO": "Romania"}, {"PH": "Philippines"}, {"CZ": "Czechia"}, {"AL": "Albania"}, {"BR": "Brazil"}, {"IN": "India"}, {"CH": "Switzerland"}, {
    "IT": "Italy"}, {"HK": "Hong Kong"}, {"CR": "Costa Rica"}, {"UA": "Ukraine"}, {"MX": "Mexico"}, {"PT": "Portugal"}, {"ES": "Spain"}, {"FI": "Finland"}, {"DK": "Denmark"}, {"IL": "Israel"}, {"CA": "Canada"}, {"NL": "Netherlands"}, {"FR": "France"}, {"AT": "Austria"}, {"TR": "Turkiye"}, {"CO": "Colombia"}, {"LV": "Latvia"}, {"NZ": "New Zealand"}, {"UK": "United Kingdom"}, {"CL": "Chile"}, {"DE": "Germany"}, {"EE": "Estonia"}, {"MY": "Malaysia"}, {"JP": "Japan"}, {"BE": "Belgium"}, {"ZA": "South Africa"}, {"NO": "Norway"}, {"AU": "Australia"}, {"US": "United States"}]


def short_to_iso(code):
    try:
        for cont in ISO_NAMES:
            if list(cont.keys())[0] == code:
                return list(cont.items())[0]
        return ""
    except Exception as e:
        return ""


def resolve_country(code):
    standard_names = short_to_iso(code)
    flag_ = countryflag.flag.flag(code)

    return flag_, standard_names[1]


def get_all_configs():
    cfg = []
    i = 0
    for file in os.listdir(CONFIG_DIR):
        if file.endswith(".ovpn"):
            parsed_cfg = parse_details(file)
            if not parsed_cfg:
                continue
            parsed_cfg["file"] = file
            parsed_cfg["id"] = i
            flag, name = resolve_country(parsed_cfg["country"])

            parsed_cfg["flag"] = flag
            parsed_cfg["iso_name"] = name

            i += 1
            cfg.append(parsed_cfg)

    return cfg


def get_config_by_id(id):
    for cfg in VPN.CONFIGS:
        if cfg["id"] == id:
            return cfg
    return None


def search_config(search_term):
    for cfg in VPN.CONFIGS:
        cfg_ = str(cfg).lower()
        if search_term.lower() in cfg_:
            return cfg
    return None


def remove_duplicate_keys(key_name, my_dict_list):
    seen = set()
    new_list = []
    for d in my_dict_list:
        key = d[key_name]
        if key not in seen:
            seen.add(key)
            new_list.append(d)
    return new_list


def is_capitalized(word):
    """Check if the first letter of the word is capitalized."""
    return word[0].isupper()


def parse_details(cfg_name):
    try:
        parts = cfg_name.split("-")

        _country = parts[1]
        _remaining = "-".join(parts[2:])

        _splitted = _remaining.split("-")
        _city = _splitted[0]

        if len(_splitted) > 1:
            if is_capitalized(_splitted[1]):
                _city += " " + _splitted[1]
                _city_code = _splitted[2]
            else:
                _city_code = _splitted[1]
        else:
            _city_code = None

        _server = _splitted[-1].split(".")[0]

    except Exception as e:
        log_error(f"error parsing config file: {cfg_name}")
        return None

    return {
        "country": _country,
        "city": _city,
        "city_code": _city_code,
        "server": _server,
    }


class VPN:
    is_active = False
    CONFIGS = get_all_configs()
    active_id = None
    active_process = None
    active_process_id = None

    def __init__(self, user, password):
        self.user = user
        self.password = password

    def set_active(self, id):
        self.active_id = id
        self.is_active = True

    def get_pid(self):
        return self.active_process_id

    def connect(self, id):
        self.set_active(id)

        config = get_config_by_id(id)
        if not config:
            return False

        with open("./configs/auth.txt", "w") as f:
            f.write(f"{self.user}\n{self.password}")

        CMD = f"cd configs && sudo openvpn --config {
            config['file']} --auth-user-pass ./auth.txt"
        process = subprocess.Popen(
            CMD, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        log_info(f"connected to VPN: {
                 config['country']} - {config['city']} - {config['server']}")
        self.active_process_id = process.pid + 1
        self.active_process = process
        return True

    def disconnect(self):
        if not self.is_active:
            return False

        CMD = f"sudo kill -9 {self.active_process_id}"
        subprocess.Popen(
            CMD, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.active_process.kill()
        log_info("disconnected from VPN")

        os.remove("./configs/auth.txt")
        self.active_process_id = None
        self.active_process = None
        self.is_active = False
        return True
