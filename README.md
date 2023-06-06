# Model driven telemetry cellular connectivity dashboard
This repository provides the code and instructions for deploying a container-based Cellular Connectivity Dashboard (CCD) that monitors the quality of cellular connections. The dashboard utilizes Cisco's model-driven telemetry and provides critical insights to crew members who depend on cellular connections in remote locations.

![image](https://wwwin-github.cisco.com/gve/gve_devnet_model_driven_telemetry_cellular_connectivity_dashboard/blob/master/IMAGES/ccd%20-%20overview.png)

**Dashboard Features**

The CCD dashboard offers the following data points for monitoring cellular connection quality:

  * Cellular strength (RSSI, RSRP, RSRQ)
  * Signal-to-noise ratio
  * Packet transmission
  * Packet receiving
  * Packet status
  * Cellular signal status
  * Cellular technology selection
  * Modem temperature

## Contacts
* Kirsi Kahikko (kkahikko@cisco.com)
* Justin Bor (jubor@cisco.com)

## Solution Components
  * Cisco Cellular Router (e.g. Cisco IR1101)
  * Docker (Compose)
    * Telegraf
    * InfluxDB
    * Grafana
  * Python
  * IOS XE

## Related Sandbox Environment
This sample code can be tested using a Cisco dCloud demo instance that contains the IR1101 industrial router.

## Prerequisites
Before proceeding, clone this repository with `git clone <this repo>`.

## Installation/Configuration

### Configuring Telemetry Subscriptions on an IOS-XE Device

To install the telemetry subscriptions correctly, follow these steps:

1. Edit the `adjust.env` file with the correct technical details, such as the IP address, port number, username, and password of the IOS XE industrial router. Adjust the following variables:

  * Related to the IOS-XE device:
    * TEL_IP_ADDRESS
    * TEL_PORT
    * TEL_USERNAME
    * TEL_PASSWORD
  * Related to your VM / device running the containers
    * TEL_IP_ADD_LIST
    * TEL_PORT_LIST

Rename the `adjust.env` file to `.env`.

2. Ensure that all the necessary modules defined in `telemetry_function.py` are installed before starting the subscription setup process.

3. Run the `telemetry_function.py` script and execute the `start_subscriptions()` function to initiate the process of setting up the necessary subscriptions for monitoring and visualizing cellular connectivity data using the TIG Stack.

### Setting up Docker Compose Container Environment

1. Edit the `adjust.telegraf.conf` file with the IP address of the InfluxDB container. Rename the file to `telegraf.conf`.

2. Edit the `adjust.docker-compose.yml` file with the necessary environmental variable changes. Make sure to change the default variables as this increases the level of safety with which the containers are exectued. Rename the file to `docker-compose.yml`.

3. Start the container using Docker Compose by navigating to the repository's containers folder and using the `docker-compose up` command.

4. Verify that the containers are properly booted by reading through the debug info of the containers

### Adjusting the InfluxDB container

To prevent the use of the FLUX data language, which has a steep learning curve, a few manual adjustments must be made to the InfluxDB container in order to connect with Grafana container. Documentation on this manual step can be found [here (InfluxData.com)](https://docs.influxdata.com/influxdb/v1.8/tools/grafana/)

1. First identify the right InfluxDB bucket ID using the `docker exec influxdb influx bucket list` command. Look for the bucket name that matches the predefined name in the `adjust.docker-compose.yml` file.

2. Run the `docker exec influxdb influx v1 dbrp create   --db [DATABASE]   --rp retention_rws    --bucket-id [bucket-ID]   --default` command. Change the **[DATABASE]** and **[bucket-ID]** out for the right chosen database name and bucket ID.

3. Store the database that is created. Optionally use `docker exec influxdb influx v1 dbrp list` to identify the database ID

4. Create a user account by first running the `docker exec influxdb influx v1 auth create   --read-bucket [bucket-name]   --write-bucket [bucket-ID]   --username [USERNAME] --no-password` command. Change the **[bucket-ID]** and **[USERNAME]** out for the right bucket ID and chosen username.

5. Store the user ID that is created. Optionally use `docker exec influxdb influx v1 auth list` to identify the user ID

6. Create a password for the user account by running the `docker exec influxdb influx v1 auth set-password   --id [user ID] --password [PASSWORD]` command. Change the **[user ID]** and **[PASSWORD]** out for the right user ID and chosen password.

Your InfluxDB container is now ready to communicate with your Grafana container. D

### Grafana

1. Open the GUI of your Grafana container by navigating to `http://container-location:3000/`. The container-location can be `localhost`, but also an IP-address. 

2. Login using the default username (admin) and password (admin). Change this password immediately.

3. Setup the InfluxDB - Grafana connection by navigating to the settings icon in the left bar and select 'Data sources'. Click on 'Add new data source'. Select 'InfluxDB' in the list of data sources.

4. Fill in the following elements on the page that follows:
  * URL: `http://container-location:8086/`
  * Custom HTTP Headers, click on 'Add header'. 
    * Under 'Header' fill in 'Authorization'. 
    * Under 'Value' fill in 'Token ' (include a space after token). Paste the `DOCKER_INFLUXDB_INIT_ADMIN_TOKEN` value from the `docker-compose.yml` after. The total string in the 'Value' field should be: `Token ADMIN_TOKEN`.
  * Under 'InfluxDB Details' fill in:
    * Under 'Database' fill in the **[DATABASE]** value as configured in InfluxDB.
    * Under 'User' fill in the **[USERNAME]** value as configured in InfluxDB.
    * Under 'Password' fill in the **[PASSWORD]** value as configured in InfluxDB.
    * Under 'HTTP Method' choose 'GET'.

5. Click on 'Save & Test'

You should receive a green alert bar on your screen. If succesful, you are ready to configure your dashboard.

1. Click on the 4 square icon ('Dashboards') in the left menu bar. Select '+ Import'. 

2. Drag and drop the `dashboard-template.json` into 'Upload' area of the GUI. 

3. Click on load.

You have now setup the Cellular Connectivity Dashboard (CCD) Dashboard.

![image](https://wwwin-github.cisco.com/gve/gve_devnet_model_driven_telemetry_cellular_connectivity_dashboard/blob/master/IMAGES/dashboard-screenshot.png)

### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.
