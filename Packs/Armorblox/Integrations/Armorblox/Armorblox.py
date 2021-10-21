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
verify_certificate = not demisto.params().get('insecure', False)
proxy = demisto.params().get('proxy', False)
BASE_URL = f"https://{TENANT_NAME}.armorblox.io/api/v1beta1/organizations/{TENANT_NAME}"

payload: Dict = {}
headers = {
    'x-ab-authorization': f'{API_KEY}'
}


class Client(BaseClient):
    """Client class to interact with the service API
    This Client implements API calls, and does not contain any Demisto logic.
    Should only do requests and return data.
    It inherits from BaseClient defined in CommonServer Python.
    Most calls use _http_request() that handles proxy, SSL verification, etc.
    """

    def get_incidents(self, orderBy="ASC", pageSize=None) -> List[Dict[str, Any]]:
        request_params: Dict[str, Any] = {}

        request_params['orderBy'] = orderBy
        if pageSize:
            request_params['pageSize'] = 1
        return self._http_request(
            method='GET',
            url_suffix='/incidents',
            params=request_params
        )

    def get_incident_details(self, incident_id):
        request_params: Dict[str, Any] = {}
        return self._http_request(
            method='GET',
            url_suffix='/incidents/{}'.format(incident_id),
            params=request_params
        )


def test_module(client: Client) -> str:
    """Tests API connectivity and authentication'
    Returning 'ok' indicates that the integration works like it is supposed to.
    Connection to the service is successful.
    Raises exceptions if something goes wrong.
    :type client: ``Client``
    :param Client: Armorblox client to use
    :type name: ``str``
    :return: 'ok' if test passed, anything else will fail the test.
    :rtype: ``str``
    """

    try:
        client.get_incidents(pageSize=1)

    except DemistoException as e:
        if 'Forbidden' in str(e):
            return 'Authorization Error: make sure API Key is correctly set'
        else:
            raise e
    return 'ok'


def get_incidents_list(client):
    """
    Hits the Armorblox API and returns the list of fetched incidents.
    """
    response = client.get_incidents()
    results = []
    if 'incidents' in response.keys():
        results = response['incidents']

    # For each incident, get the details and extract the message_id
    for result in results:
        result['message_ids'] = get_incident_message_ids(client, result["id"])
    return results


def get_incident_message_ids(client, incident_id):
    """
    Returns the message ids for all the events for the input incident.
    """

    detail_response = client.get_incident_details(incident_id)
    message_ids = []
    # loop through all the events of this incident and collect the message ids
    if 'events' in detail_response.keys():
        for event in detail_response['events']:
            message_ids.append(event['message_id'])

    if 'abuse_events' in detail_response.keys():
        for event in detail_response['abuse_events']:
            message_ids.append(event['message_id'])
    return message_ids


def fetch_incidents_command(client):

    last_run = demisto.getLastRun()
    if last_run and 'start_time' in last_run.keys():
        start_time = dateparser.parse(last_run.get('start_time'))
    else:
        now = datetime.now()
        start_time = now - timedelta(days=1)
        start_time = dateparser.parse(start_time.strftime(DATE_FORMAT))
    start_time = start_time.timestamp()
    demisto.debug(str(start_time))
    incidents_data = get_incidents_list(client)
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


def main():
    ''' EXECUTION '''
    LOG('command is %s' % (demisto.command(), ))
    try:

        client = Client(
            base_url=BASE_URL,
            verify=verify_certificate,
            headers=headers,
            proxy=proxy)

        if demisto.command() == "fetch-incidents":
            return_results(fetch_incidents_command(client))

        elif demisto.command() == 'test-module':
            result = test_module(client)
            return_results(result)
    except Exception as e:
        return_error(str(e))


if __name__ in ['__main__', 'builtin', 'builtins']:
    main()