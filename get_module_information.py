import json
import requests
import datetime

NUS_MODS_API = 'https://api.nusmods.com/v2/'


def getCurrentAcademicYear():
    now = datetime.datetime.now()
    currentYear = now.year
    if now.month < 8:
        currentYear -= 1
    return f'{currentYear}-{currentYear + 1}'


def getCurrentSemester():
    month = datetime.datetime.now().month
    if 1 <= month <= 5:
        return 2
    elif 8 <= month <= 12:
        return 1


def getModuleInformation(acadYear, moduleCode):
    url = NUS_MODS_API + acadYear + '/modules/' + moduleCode + '.json'
    try:
        response = requests.get(url)
        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        return response.json()
