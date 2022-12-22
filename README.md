# powerparse
This utility will execute an API call to a power company API to return a JSON object and parse it into a mariadb database table.

## VM Requirements:
Ubuntu Linux 20.04.4 LTS

libmariadb3

libmariadb-dev

mariadb-server

python3

### Python 3 Packages:
pandas

mariadb

## Installation:

### Install required packages:
sudo apt install libmariadb3 libmariadb-dev git python3-pip python3 mariadb-server

### If using WSL locally
sudo /etc/init.d/mysql start

### Run mysql secure installation
sudo mysql_secure_installation

### Copy repository files
git clone https://github.com/kierankyllo/powerparse.git

### Edit following line in the powerparse.sql file to add your custom password for the database
CREATE USER 'agent'@'localhost' IDENTIFIED BY 'YOUR_PASSWORD_HERE';

### Login to the database and run the setup query file
sudo mysql

source powerparse.sql;

exit;

### Edit config.json file to add your custom password for the database 

    "user": "agent",
    "password": "YOUR_PASSWORD_HERE",
    "host": "localhost",
    "port": 3306,
    "database": "powerparse",


## Operation

Run the script as a standalone or add it as a systemd service unit to run on startup.

## Files
ppscript.py - parses API call into alert table

powerparse.sql - creates database user and empty tables

config.json - configuration file for database connection

ppscript.sh - shell script for startup service

powerparse.service - systemd unit file to run as a startup service
