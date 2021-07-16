import os
import time
import email
import requests
import configparser
from email.parser import Parser
from zenpy import Zenpy
from zenpy.lib.api_objects import Comment, Ticket

# CONFIG PARSER
config = configparser.ConfigParser()
config.read('config.txt')
email = config.get('ZENDESK', 'email')
subdomain = config.get('ZENDESK', 'subdomain')
view_id = config.get('ZENDESK', 'view_id')
view_id = int(view_id)
author_id = config.get('ZENDESK', 'author_id')
author_id = int(author_id)
# ENV VAR
token = os.environ.get('ZENDESK_TOKEN')

creds = {
    'email': f"{email}",
    'token': f"{token}",
    'subdomain': f"{subdomain}"
}
zenpy = Zenpy(**creds)

def HeaderDetecter(view_id):
    """ EXECUTE VIEW IN ORDER TO GET TICKET """
    ticket_list = zenpy.views.tickets(view=view_id)
    for ticket in ticket_list:
        ticket_id = ticket.id

        """ GET ALL COMMENT, ALL ATTACHMENTS, CONTENT_TYPE, CONTENT, FILENAME """
        comment_list = zenpy.tickets.comments(ticket_id)
        for comment in comment_list:
            for attachment in comment.attachments:
                file_name = attachment.file_name
                file_type = attachment.content_type
                file_url = attachment.content_url

                """ IF FILE TYPE IS NOT MSG """
                if file_type is not "application/vns.ms-outlook" and not file_name.lower().endswith(".msg"):
                    r = requests.get(file_url)
                    email = r.content
                    if type(email) is not "str":
                        try:
                            email = email.decode("utf-8")
                        except (RuntimeError, Exception, UnicodeDecodeError) as err:
                            print("Error when decoding email in utf-8 - Error: {err}")

                    # Parse EML content
                    headers = Parser().parsestr(email)

                    # Configparser
                    header1 = config.get('HEADERS', 'header1')
                    header2 = config.get('HEADERS', 'header2')
                    header3 = config.get('HEADERS', 'header3')

                    specific_header1 = headers[str(header1)]
                    specific_header2 = headers[str(header2)]
                    specific_header3 = headers[str(header3)]

                    comment = f"""Filename: {file_name}
                    Header1: {specific_header1}
                    Header2: {specific_header2}
                    Header3: {specific_header3}"""

                    """ REDACT PRIVATE COMMENT TO THE RIGHT TICKET AND ADD THE TAG header_detected """
                    ticket = zenpy.tickets(id=ticket_id)
                    ticket.comment = Comment(
                        body=comment,
                        public=False,
                        author_id=author_id
                    )
                    ticket.tags.extend(['header_detected'])
                    zenpy.tickets.update(ticket)
                    print("Comment added in ticket: #{ticket_id}")

    return True

def main():
    while True:
        HeaderDetecter()
        time.sleep(60)

if __name__ == '__main__':
    main()
