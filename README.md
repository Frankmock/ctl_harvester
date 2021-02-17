# ctl_harvester
A bunch of scripts to easily harvest all the data from the Certificate Transparency Lists and put it into an sqlite database.

# How it works
It basically gets the stream from certstream.calidog.io and extracts all the domains and puts them in an SQLite database (`gather_ctl_data.py`). 
Another python script (`ctl_data_manager.py`) kills the process periodically and starts a new one. It then moves the SQLite database to a different folder so it can be picked up by another program to ingest it somewhere. It does this to make the harvesting as efficiently as possible. 

Live databases are written to: `/opt/ctl_harvesting/var/data`
Databases ready to be processed are in: `/opt/ctl_harvesting/var/data/ready_to_process`

# How to use it
Note: The steps below assume you are running this in root, if not, please make sure you configure the proper permissions on the folder and use sudo to install the dependencies.

1. Create a folder structure to store all the data and scripts. For example:
```
mkdir -p /opt/ctl_harvesting/bin
mkdir -p /opt/ctl_harvesting/var/data/ready_to_process
mkdir /opt/ctl_harvesting/var/log
```
2. Put all the python files in this repository into the `/opt/ctl_harvesting/bin` folder
3. Install the dependencies (don't forget to install pip3 if it isn't already):
    - `pip3 install websocket-client`
    - `apt update ; apt -y install postfix` 
      - So cron can send errors to a mailclient
4. Start the harvester:
`/bin/python3 /opt/ctl_harvesting/bin/gather_ctl_data.py dont_store_certs &`
5. Create a cronjob for the `ctl_data_manager.py`. For example:
`0 * * * * /bin/python3 /opt/ctl_harvesting/bin/ctl_data_manager.py > /opt/ctl_harvesting/log/ctl_cron.log`

# Disclaimer
This a bad script, but it works.

# Acknowledgements
The certstream.py file is a copy from the certstream-python library by CaliDog. I made a copy since I couldn't get it to install using pip3.
