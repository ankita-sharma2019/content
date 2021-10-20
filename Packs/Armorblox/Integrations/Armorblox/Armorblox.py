import demistomock as demisto  # noqa: F401
from CommonServerPython import *  # noqa: F401
import dateparser
import requests
import json
from datetime import datetime, timedelta


# disable insecure warnings
requests.packages.urllib3.disable_warnings()

DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
MAX_INCIDENTS_TO_FETCH = 50

TENANT_NAME = demisto.params().get('tenantName')
INSECURE = demisto.params().get('insecure')
PROXY = demisto.params().get('proxy')
API_KEY = demisto.params().get('apikey')
BASE_URL = f"https://{TENANT_NAME}.armorblox.io/api/v1beta1/organizations/{TENANT_NAME}/incidents"

payload: Dict = {}
headers = {
    'x-ab-authorization': API_KEY
}
# contains all the incident severity types
# IncidentSeverity = {
#     'LOW' : 1,
#     'MEDIUM' : 2,
#     'HIGH' : 3
# }


def get_incident_message_ids(incident_id):
    incident_details_url = "{}/{}".format(BASE_URL, incident_id)
    detail_response = requests.request("GET", incident_details_url, headers=headers, data=payload).json()
    message_ids = []
    # loop through all the events of this incident
    if 'events' in detail_response.keys():
        for event in detail_response['events']:
            message_ids.append(event['message_id'])

    if 'abuse_events' in detail_response.keys():
        for event in detail_response['abuse_events']:
            message_ids.append(event['message_id'])
    return message_ids


def get_incidents():
    # incident_list_url = f"https://{opt_tenant_name}.armorblox.io/api/v1beta1/organizations/{opt_tenant_name}/incidents"

    response = requests.request("GET", BASE_URL + "?&orderBy=ASC", headers=headers, data=payload)

    r_json = response.json()

    r_status = response.status_code
    if r_status != 200:
        # check the response status, if the status is not sucessful, raise requests.HTTPError
        response.raise_for_status()

    results = []
    if 'incidents' in r_json.keys():
        results = response.json()['incidents']

    # For each incident, get the details and extract the message_id
    for result in results:
        result['message_ids'] = get_incident_message_ids(result["id"])
    return results


def get_armorblox_incidents_command():
    results = get_incidents()
    for incident in results:
        occured_time = incident['date']
        demisto.results('The user : ' + incident['users'] + 'has reported an alert as of ' + occured_time)


def fetch_incidents_command():

    # demisto.debug("Incidents: "+str(len(results)))

    last_run = demisto.getLastRun()
    if last_run and 'start_time' in last_run.keys():
        start_time = dateparser.parse(last_run.get('start_time'))
    else:
        now = datetime.now()
        start_time = now - timedelta(days=1)
        start_time = dateparser.parse(start_time.strftime(DATE_FORMAT))
    start_time = start_time.timestamp()
    demisto.debug(str(start_time))
    data = get_incidents()
    last_time = start_time
    inc = []
    for res in data:
        # demisto.debug(res)
        res['name'] = "Armorblox"
        dt = res['date']
        dt = dateparser.parse(dt).timestamp()
        if dt > start_time:

            # , 'details': json.dumps(res), 'severity': IncidentSeverity[res.get('priority')], 'CustomFields': {'details' : res}}
            temp = {'name': "Armorblox", 'rawJSON': json.dumps(res), 'details': json.dumps(res), 'CustomFields': {'details': res}}
            last_time = dt
            inc.append(temp)

        demisto.debug(str(last_time))
    demisto.setLastRun({'start_time': str(last_time)})
    demisto.incidents(inc)
    readable_output = f'## {inc}'
    return CommandResults(
        readable_output=readable_output,
        outputs_prefix='Armorblox',
        outputs_key_field='',
        outputs=inc
    )


''' EXECUTION '''
LOG('command is %s' % (demisto.command(), ))
try:
    if demisto.command() == 'armorblox':
        get_armorblox_incidents_command()
    elif demisto.command() == "fetch-incidents":
        a = fetch_incidents_command()
        return_results(a)
        demisto.results("Incidents fetched")
    elif demisto.command() == 'test-module':
        fetch_incidents_command()
        demisto.results("OK")
except Exception as e:
    demisto.debug('Error!')
    return_error(e)
