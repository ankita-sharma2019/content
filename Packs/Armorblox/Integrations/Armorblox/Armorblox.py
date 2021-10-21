import demistomock as demisto
from CommonServerPython import *
from CommonServerUserPython import *
import dateparser
import requests
import json
from datetime import datetime, timedelta


# disable insecure warnings
requests.packages.urllib3.disable_warnings()

DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
# MAX_INCIDENTS_TO_FETCH = 50

TENANT_NAME = demisto.params().get('tenantName')
INSECURE = demisto.params().get('insecure')
PROXY = demisto.params().get('proxy')
API_KEY = demisto.params().get('apikey')

BASE_URL = f"https://{TENANT_NAME}.armorblox.io/api/v1beta1/organizations/{TENANT_NAME}/incidents"

payload: Dict = {}
headers = {
    'x-ab-authorization': API_KEY
}


def get_incident_message_ids(incident_id):
    """
    Returns the message ids for all the events for the input incident.
    """
    incident_details_url = "{}/{}".format(BASE_URL, incident_id)
    detail_response = requests.request("GET", incident_details_url, headers=headers, data=payload).json()
    message_ids = []
    # loop through all the events of this incident and collect the message ids
    if 'events' in detail_response.keys():
        for event in detail_response['events']:
            message_ids.append(event['message_id'])

    if 'abuse_events' in detail_response.keys():
        for event in detail_response['abuse_events']:
            message_ids.append(event['message_id'])
    return message_ids


def get_incidents():
    """
    Hits the Armorblox API and returns the list of fetched incidents.
    """
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


def fetch_incidents_command():

    last_run = demisto.getLastRun()
    if last_run and 'start_time' in last_run.keys():
        start_time = dateparser.parse(last_run.get('start_time'))
    else:
        now = datetime.now()
        start_time = now - timedelta(days=1)
        start_time = dateparser.parse(start_time.strftime(DATE_FORMAT))
    start_time = start_time.timestamp()
    demisto.debug(str(start_time))
    incidents_data = get_incidents()
    last_time = start_time
    incidents = []
    for incident in incidents_data:
        dt = incident['date']
        dt = dateparser.parse(dt).timestamp()
        # Update last run and add incident if the incident is newer than last fetch
        if dt > start_time:

            curr_incident = {'rawJSON': json.dumps(incident), 'details': json.dumps(incident)}
            last_time = dt
            incidents.append(curr_incident)

    # Save the next_run as a dict with the start_time key to be stored
    demisto.setLastRun({'start_time': str(last_time)})
    demisto.incidents(incidents)
    readable_output = f'## {incidents}'
    return CommandResults(
        readable_output=readable_output,
        outputs_prefix='Armorblox',
        outputs_key_field='',
        outputs=incidents
    )


def test_module():
    # Run a sample request to retrieve mock data
    response = requests.request("GET", BASE_URL + "?&pageSize=1", headers=headers, data=payload)
    demisto.results("ok")


def main():
    ''' EXECUTION '''
    LOG('command is %s' % (demisto.command(), ))
    try:
        if demisto.command() == "fetch-incidents":
            return_results(fetch_incidents_command())

        elif demisto.command() == 'test-module':
            test_module()
    except Exception as e:
        return_error(str(e))


if __name__ in ['__main__', 'builtin', 'builtins']:
    main()
