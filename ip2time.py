import platform
import ctypes
import requests
import subprocess
import json
import time

print("ip2time - https://github.com/Shinryin/ip2time - V1.0.0")
print("Please report any bugs by creating a new issue on GitHub.")
# Custom IANA -> Windows TZ Mappings. Please add if your timezone does not exist.

timezone_mapping = {
    'America/New_York': 'Eastern Standard Time',
    'America/Chicago': 'Central Standard Time',
    'America/Denver': 'Mountain Standard Time',
    'America/Los_Angeles': 'Pacific Standard Time',
    'America/Anchorage': 'Alaskan Standard Time',
    'Pacific/Honolulu': 'Hawaiian Standard Time',
    'America/Phoenix': 'US Mountain Standard Time',
    'America/Indiana/Indianapolis': 'US Eastern Standard Time',
    'America/Detroit': 'Eastern Standard Time',
    'America/Kentucky/Louisville': 'Eastern Standard Time',
    'America/Kentucky/Monticello': 'Eastern Standard Time',
    'America/Indiana/Vincennes': 'Eastern Standard Time',
    'America/Indiana/Winamac': 'Eastern Standard Time',
    'America/Indiana/Marengo': 'Eastern Standard Time',
    'America/Indiana/Petersburg': 'Eastern Standard Time',
    'America/Indiana/Vevay': 'Eastern Standard Time',
    'America/Indiana/Tell_City': 'Central Standard Time',
    'America/Indiana/Knox': 'Central Standard Time',
    'America/Menominee': 'Central Standard Time',
    'America/North_Dakota/Center': 'Central Standard Time',
    'America/North_Dakota/New_Salem': 'Central Standard Time',
    'America/North_Dakota/Beulah': 'Central Standard Time',
    'America/Denver': 'Mountain Standard Time',
    'America/Boise': 'Mountain Standard Time',
    'America/Juneau': 'Alaskan Standard Time',
    'America/Sitka': 'Alaskan Standard Time',
    'America/Yakutat': 'Alaskan Standard Time',
    'America/Nome': 'Alaskan Standard Time',
    'America/Adak': 'Hawaiian Standard Time',
    'America/Metlakatla': 'Pacific Standard Time',
    'Europe/London': 'GMT Standard Time',
    'Europe/Paris': 'Romance Standard Time',
    'Asia/Tokyo': 'Tokyo Standard Time',
    'Australia/Sydney': 'AUS Eastern Standard Time',
    'Asia/Shanghai': 'China Standard Time',
    'Asia/Dubai': 'Arabian Standard Time',
    'Asia/Kolkata': 'India Standard Time',
    'Asia/Singapore': 'Singapore Standard Time',
    'Asia/Bangkok': 'SE Asia Standard Time',
    'Asia/Jakarta': 'W. Indonesia Standard Time',
    'Asia/Seoul': 'Korea Standard Time',
    'Asia/Taipei': 'Taipei Standard Time',
    'Asia/Hong_Kong': 'Hong Kong Standard Time',
    'Asia/Riyadh': 'Arab Standard Time',
    'Asia/Qatar': 'Arab Standard Time',
    'Asia/Baghdad': 'Arabic Standard Time',
    'Asia/Tehran': 'Iran Standard Time',
    'Asia/Jerusalem': 'Israel Standard Time',
    'Africa/Cairo': 'Egypt Standard Time',
    'Africa/Johannesburg': 'South Africa Standard Time',
    'Africa/Casablanca': 'Morocco Standard Time',
    'Europe/Moscow': 'Russian Standard Time',
    'Europe/Istanbul': 'Turkey Standard Time',
    'Europe/Berlin': 'W. Europe Standard Time',
    'Europe/Rome': 'W. Europe Standard Time',
    'Europe/Amsterdam': 'W. Europe Standard Time',
    'Europe/Zurich': 'W. Europe Standard Time',
    'Europe/Stockholm': 'W. Europe Standard Time',
    'Europe/Vienna': 'W. Europe Standard Time',
    'Europe/Budapest': 'Central Europe Standard Time',
    'Europe/Warsaw': 'Central Europe Standard Time',
    'Europe/Prague': 'Central Europe Standard Time',
    'Europe/Athens': 'GTB Standard Time',
    'Europe/Bucharest': 'GTB Standard Time',
    'Europe/Helsinki': 'FLE Standard Time',
    'Pacific/Auckland': 'New Zealand Standard Time',
    'Pacific/Fiji': 'Fiji Standard Time',
    'Pacific/Guam': 'West Pacific Standard Time',
    'Pacific/Port_Moresby': 'West Pacific Standard Time',
    'America/Toronto': 'Eastern Standard Time',
    'America/Vancouver': 'Pacific Standard Time',
    'America/Mexico_City': 'Central Standard Time (Mexico)',
    'America/Bogota': 'SA Pacific Standard Time',
    'America/Santiago': 'Pacific SA Standard Time',
    'America/Caracas': 'Venezuela Standard Time',
    'Atlantic/Cape_Verde': 'Cape Verde Standard Time',
    'Europe/Belgrade': 'Central Europe Standard Time',
    'Europe/Brussels': 'Romance Standard Time',
    'Europe/Copenhagen': 'Central Europe Standard Time',
    'Europe/Dublin': 'GMT Standard Time',
    'Europe/Lisbon': 'GMT Standard Time',
    'Europe/Luxembourg': 'W. Europe Standard Time',
    'Europe/Madrid': 'Romance Standard Time',
    'Europe/Oslo': 'W. Europe Standard Time',
    'Asia/Colombo': 'Sri Lanka Standard Time',
    'Asia/Dhaka': 'Bangladesh Standard Time',
    'Asia/Kabul': 'Afghanistan Standard Time',
    'Asia/Kathmandu': 'Nepal Standard Time',
    'Asia/Kuala_Lumpur': 'Singapore Standard Time',
    'Asia/Muscat': 'Arabian Standard Time',
    'Asia/Tashkent': 'West Asia Standard Time',
    'Asia/Yerevan': 'Caucasus Standard Time',
    'Atlantic/South_Georgia': 'UTC-02',
    'Australia/Adelaide': 'Cen. Australia Standard Time',
    'Australia/Brisbane': 'E. Australia Standard Time',
    'Australia/Darwin': 'AUS Central Standard Time',
    'Australia/Hobart': 'Tasmania Standard Time',
    'Australia/Perth': 'W. Australia Standard Time',
    'Australia/Sydney': 'AUS Eastern Standard Time',
    'Pacific/Guadalcanal': 'Central Pacific Standard Time',
    'Pacific/Noumea': 'Central Pacific Standard Time',
    'Pacific/Tongatapu': 'Tonga Standard Time',
    'Asia/Amman': 'Jordan Standard Time',
    'Asia/Beirut': 'Middle East Standard Time',
    'Asia/Baku': 'Azerbaijan Standard Time',
    'Asia/Kuwait': 'Arab Standard Time',
    'Europe/Chisinau': 'E. Europe Standard Time',
    'Europe/Kiev': 'FLE Standard Time',
    'Europe/Minsk': 'Belarus Standard Time',
    'Europe/Riga': 'FLE Standard Time',
    'Europe/Sofia': 'E. Europe Standard Time',
    'Europe/Tallinn': 'FLE Standard Time',
    'Europe/Vilnius': 'FLE Standard Time',
    'Africa/Cairo': 'Egypt Standard Time',
    'Pacific/Chatham': 'Chatham Standard Time'
}

def get_external_ip():
    response = requests.get("http://ip-api.com/json/")
    return response.json()['query']

def get_timezone(ip):
    while True:
        try:
            response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
            data = response.json()
            timezone = data['timezone']
            location = (data['city'], data['regionName'], data['country'])
            return (timezone, location)
        except Exception as e:
            print(f"Error getting timezone: {e}")
            print("Retrying in 3 seconds...")
            time.sleep(3)

def set_timezone(timezone):
    system = platform.system()
    if system == 'Windows':
        # Admin check
        if not ctypes.windll.shell32.IsUserAnAdmin():
            print('Please run this tool as an administrator to set the timezone.')
            return

        # Windows
        subprocess.run(f'tzutil /s "{timezone_mapping.get(timezone[0], "UTC")}"', shell=True, check=True)
    elif system == 'Darwin':
        # Mac
        subprocess.run(f'sudo systemsetup -settimezone "{timezone[0]}"', shell=True, check=True)
    else:
        # Linux
        subprocess.run(f'sudo timedatectl set-timezone "{timezone[0]}"', shell=True, check=True)

    print(f"Location: {timezone[1][0]}, {timezone[1][1]}, {timezone[1][2]}")

def main():
    try:
        ip = get_external_ip()
        print(f"External IP: {ip}")

        start_time = time.monotonic()
        timezone = get_timezone(ip)
        end_time = time.monotonic()
        ping_time = round((end_time - start_time) * 1000)
        print(f"Timezone: {timezone[0]} (ping: {ping_time} ms)")

        set_timezone(timezone)
        print(f"Timezone updated successfully to {timezone[0]}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

input("Press enter to close...")
