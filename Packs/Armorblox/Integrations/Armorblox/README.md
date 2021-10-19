This is the Armorblox integration for Cortex XSoar.
This integration was integrated and tested with version '' of Armorblox

## Configure Armorblox on Cortex XSOAR

1. Navigate to **Settings** > **Integrations** > **Servers & Services**.
2. Search for Armorblox.
3. Click **Add instance** to create and configure a new integration instance.

    | **Parameter** | **Required** |
    | --- | --- |
    | Armorblox tenant name | True |
    | API Key | True |
    | Fetch incidents | False |
    | Incidents Fetch Interval | False |
    | Incident type | False |
    | Maximum number of incidents per fetch | False |
    | First fetch time | False |
    | Trust any certificate (not secure) | False |
    | Use system proxy settings | False |

4. Click **Test** to validate the URLs, token, and connection.
## Commands
You can execute these commands from the Cortex XSOAR CLI, as part of an automation, or in a playbook.
After you successfully execute a command, a DBot message appears in the War Room with the command details.
### armorblox-fetch-incidents
***
Gets a list of armorblox incidents


#### Base Command

`armorblox-fetch-incidents`
#### Input

There are no input arguments for this command.

#### Context Output

There is no context output for this command.

#### Command Example
``` ```

#### Human Readable Output


