import demistomock as demisto  # noqa: F401
from CommonServerPython import *  # noqa: F401
"""Base Script for Cortex XSOAR (aka Demisto)
This is an empty script with some basic structure according
to the code conventions.
MAKE SURE YOU REVIEW/REPLACE ALL THE COMMENTS MARKED AS "TODO"
Developer Documentation: https://xsoar.pan.dev/docs/welcome
Code Conventions: https://xsoar.pan.dev/docs/integrations/code-conventions
Linting: https://xsoar.pan.dev/docs/integrations/linting
"""

from typing import Dict, Any
import traceback
import smtplib

''' STANDALONE FUNCTION '''


# TODO: REMOVE the following dummy function:
def send_email(email: str, incident_id: str, remediation_action: str) -> Dict[str, str]:
    """Returns a simple python dict with the information provided
    in the input (dummy).
    :type dummy: ``str``
    :param dummy: string to add in the dummy dict that is returned
    :return: dict as {"dummy": dummy}
    :rtype: ``str``
    """
    if remediation_action:
        port = 465
        smtp_server = 'smtp.gmail.com'
        sender_email = 'test.armorblox@gmail.com'
        password = 'Armorb123@'
        receiver_email = email
        subject = 'Remediation Action '
        body = f'The incident id: {incident_id} NEEDS REVIEW.'
        message = 'Subject: {}\n\n{}'.format(subject, body)
        with smtplib.SMTP_SSL(smtp_server, port) as server:
            # server.ehlo()  # Can be omitted
            # server.starttls(context=context)
            # server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)

        return f"Email Sent to {email}"
    else:
        return "Does not require to be reviewed"
# TODO: ADD HERE THE FUNCTIONS TO INTERACT WITH YOUR PRODUCT API


''' COMMAND FUNCTION '''


# TODO: REMOVE the following dummy command function
def send_email_command(args: Dict[str, Any]) -> CommandResults:

    email = args.get('user_email', None)
    incident_id = args.get('incident_id', None)
    if not incident_id:
        raise ValueError('Incident Id not specified')

    if not email:
        raise ValueError('Email not specified')

    # Call the standalone function and get the raw response
    result = send_email(email, incident_id)
    markdown = f'## {result}'
    outputs = {
        'Armorblox': {
            'send_report': result
        }
    }

    return CommandResults(
        readable_output=markdown,
        outputs_key_field=None,
        outputs=outputs,
    )
# TODO: ADD additional command functions that translate XSOAR inputs/outputs


''' MAIN FUNCTION '''


def main():
    try:
        # TODO: replace the invoked command function with yours
        return_results(send_email_command(demisto.args()))
    except Exception as ex:
        demisto.error(traceback.format_exc())  # print the traceback
        return_error(f'Failed to execute BaseScript. Error: {str(ex)}')


''' ENTRY POINT '''


if __name__ in ('__main__', '__builtin__', 'builtins'):
    main()
