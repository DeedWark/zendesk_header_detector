# zendesk_header_detecter
Detect specific headers in attached EML/File in Zendesk ticket

## Launch
!!! Don't forget to replace elements in app/config.txt
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
