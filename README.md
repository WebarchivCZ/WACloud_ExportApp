# WACloud_ExportApp

WARC Export application 

## Funding - dedication

The work of this project - Centralised interface for Webarchive big data extraction and analysis (projcet identification code: DG18P02OVV016), was supported via programme of the Ministry of culture of the Czech Republic - Applied research and developement of national and culture identity programme (NAKI).

## Requirements

- python 3 (tested with 3.8)
- python venv (`apt install python3.8-venv`)

## Production

### Linux (bash)

- create a virtual environment (venv): `python3 -m venv venv`
- activate the venv: `. ./venv/bin/activate`
- install requirements: `pip install -r requirements.txt`
- deactivate venv `deactive`
- create a systemd service `/etc/systemd/system/multi-user.target.wants/warc-exporter.service`
  with content from the file `systemd.service` (replace `<OS_USER>` and `<PATH_TO_APP>` to your values)
- if your HBase Thrift Server  does not run on `localhost:9090`, you have to modify `Environment` lines
- reload systemd daemon `sudo systemctl daemon-reload`
- start app as a systemd service `sudo systemctl start warc-exporter`

## Development

### Linux (bash)

- create a virtual environment (venv): `python3 -m venv venv`
- activate the venv: `. ./venv/bin/activate`
- install requirements: `pip install -r requirements.txt`
- run the server: `export FLASK_APP=app && flask run`
- if you want to exit, terminate server app (Ctrl+C) and exit the venv: `deactivate`

### Windows (CMD)

- create a virtual environment (venv): `py -3 -m venv venv`
- activate the venv: `venv\Scripts\activate`
- install requirements: `pip install -r requirements.txt`
- run the server: 
```
set FLASK_APP=app
flask run
```
- if you want to exit, terminate server app (Ctrl+C) and exit the venv: `deactivate`

## Test the endpoints

Get WARC archive with documents by its identifications (Ids are saved in a sample json file)

`curl -X POST -H "Content-Type: application/json" -d @examples/documents.json --output test.warc.gz http://127.0.0.1:5000/`
