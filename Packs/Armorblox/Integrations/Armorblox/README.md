Armorblox is an API-based platform that stops targeted email attacks,
  protects sensitive data, and automates incident response.
This integration was integrated and tested with version xx of 67c81960-d3b3-4d0b-8189-6fd8ca78e8be

## Configure Armorblox on Cortex XSOAR

1. Navigate to **Settings** > **Integrations** > **Servers & Services**.
2. Search for Armorblox.
3. Click **Add instance** to create and configure a new integration instance.

    | **Parameter** | **Required** |
    | --- | --- |
    | Armorblox tenant name | True |
    | Incident type | False |
    | Trust any certificate (not secure) | False |
    | Use system proxy settings | False |
    | API Key | True |
    | Incidents Fetch Interval | False |
    | Fetch incidents | False |
    | First fetch timestamp (&lt;number&gt; &lt;time unit&gt;, e.g., 12 hours, 7 days) | False |
    | None | False |

4. Click **Test** to validate the URLs, token, and connection.
5. Select **Fetches incidents** to pull incidents from Armorblox to Cortex
6. Select Classifier as Armorblox-Classifier
7. Select Mapper as Armorblox-Mapper