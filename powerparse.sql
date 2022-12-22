CREATE USER 'agent'@'localhost' IDENTIFIED BY 'YOUR_PASSWORD';

CREATE DATABASE powerparse;

USE powerparse;

GRANT ALL PRIVILEGES ON powerparse TO 'agent'@'localhost';

CREATE TABLE alerts (
/*meta data*/
 	alert_id INT NOT NULL AUTO_INCREMENT, 
 	modified TIMESTAMP DEFAULT now() ON UPDATE now(),

/*data*/
    alert_create_date VARCHAR(80) NOT NULL,
 	alert_message VARCHAR(999) NOT NULL,
    outage_id INT NOT NULL,
    region_id INT NOT NULL,
    region_text VARCHAR(80) NOT NULL,
    planned SMALLINT NOT NULL,
    UNIQUE (outage_id, region_id, alert_create_date),

/*keys*/
PRIMARY KEY (alert_id)
);

GRANT ALL PRIVILEGES ON powerparse.alerts TO 'agent'@'localhost';