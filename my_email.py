import imaplib
import email
from email.header import decode_header
import json
import imaplib
import email
from email.header import decode_header
import json
from datetime import datetime, timedelta

def get_email(username, password, imap_server, search_date):
    con = imaplib.IMAP4_SSL(imap_server)
    con.login(username, password)

    thu_muc = "INBOX"
    con.select(thu_muc)

    search_date_str = search_date.strftime("%d-%b-%Y")
    trangthai, email_list = con.search(None, f'(SINCE "{search_date_str}")')
    email_id_list = email_list[0].split()

    result = {}
    for email_id in email_id_list:

        trang_thai, msg_data = con.fetch(email_id, "(RFC822)")

        if trang_thai == "OK":
            email_raw = msg_data[0][1]
            msg = email.message_from_bytes(email_raw)
            ngay_gui = "0" + msg.get("Date")[5:24] if msg.get("Date")[6] == " " else msg.get("Date")[5:25]
            ngay_gui = datetime.strptime(ngay_gui, "%d %b %Y %H:%M:%S")

            chu_de, encoding = decode_header(msg["Subject"])[0]
            chu_de = chu_de.decode(encoding) if encoding else chu_de

            nguoi_gui, encoding = decode_header(msg.get("From"))[0]
            nguoi_gui = nguoi_gui.decode(encoding) if encoding else nguoi_gui

            body = ''
            if msg.is_multipart():
                for part in msg.walk():
                    content_disposition = str(part.get("Content-Disposition"))
                    if "attachment" not in content_disposition:
                        if part.get_content_type() == "text/plain":
                            mss = part.get_payload(decode=True)
                            if mss:
                                body += mss.decode(errors='ignore')
            else:
                body = msg.get_payload(decode=True).decode(errors='ignore')

            if isinstance(body, bytes):
                body = body.decode('utf-8')

            if isinstance(chu_de, bytes):
                chu_de = chu_de.decode('utf-8')

            if isinstance(nguoi_gui, bytes):
                nguoi_gui = nguoi_gui.decode('utf-8')

            email_info = {
                "From": nguoi_gui,
                "Subject": chu_de,
                "Message": body,
                "Date":ngay_gui.strftime("%Y-%m-%d %H:%M:%S")
            }

            result[f"email{email_id}"] = email_info
    return json.dumps(result, ensure_ascii=False, indent=4)

