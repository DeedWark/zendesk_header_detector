# zendesk_header_detecter
Detect specific headers in attached EML/File in Zendesk ticket

## Launch
!!! Don't forget to replace elements in app/config.txt

- zendesk email, zendesk subdomain, zendesk view_id, zendesk author_id, email header 1,2,3 = app/config.txt
Example:
```
[ZENDESK]
email=user@email.com
subdomain=mycompany
view_id=1234567
author_id=9876543

[HEADERS]
header1=Content-Type
header2=From
header3=Return-Path
```
- zendesk token = environment variable -> ZENDESK_TOKEN
Example:
```bash
export ZENDESK_TOKEN="1234567abcdef"
```

```bash
python3 app/zendesk_header_detecter.py
```

## Build
```bash
docker build --build-arg ZENDESK_TOKEN='<yourtoken>' -t zendesk_header_detecter .
# OR
export ZENDESK_TOKEN='<yourtoken>'
```

## Run
```bash
docker run -d --name zendesk_header_detecter zendesk_header_detecter
```
