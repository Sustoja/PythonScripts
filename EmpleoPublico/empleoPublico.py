import configparser
import requests
import smtplib
from bs4 import BeautifulSoup
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fake_useragent import UserAgent


# Init file global variable.
CONFIG = configparser.ConfigParser(inline_comment_prefixes="#")


def read_ini_file():
    # Read INI file into a global variable.
    ini_file = __file__.replace('.py', '.ini')
    CONFIG.read(ini_file)


def send_mail_msg(subject, body):
    # Create message container - the correct MIME type is multipart/alternative.
    port = int(CONFIG.get('MAIL', "PORT"))
    smtp_server = CONFIG.get('MAIL', "SMTP_SERVER")
    sender_email = CONFIG.get('MAIL', "SENDER_EMAIL")
    receiver_email = CONFIG.get('MAIL', "RECEIVER_EMAIL")
    password = CONFIG.get('MAIL', "PASSWORD")

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    # msg['From'] = "Casa"
    # msg['To'] = "J.A."

    # Create the body of the message (a plain-text and an HTML version).
    # text = body
    html = "<html><head></head><body>"
    html += body
    html += "</body></html>"

    # Record the MIME types of both parts - text/plain and text/html.
    # part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    # msg.attach(part1)
    msg.attach(part2)

    # Send the message via local SMTP server.
    try:
        mail = smtplib.SMTP(smtp_server, port)
        mail.ehlo()
        mail.starttls()
        mail.login(sender_email, password)
        mail.sendmail(sender_email, receiver_email, msg.as_string())
        mail.quit()
    except BaseException as error:
        raise SystemExit(f"Unable to send alert email via {smtp_server}") from error


def read_html(url) -> BeautifulSoup:
    ua = UserAgent()
    hdr = {'User-Agent': ua.random,
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}
    response = requests.get(url, headers=hdr)
    if response.status_code != 200:
        raise requests.exceptions.RequestException
    return BeautifulSoup(response.text, "html.parser")


def boe_webscrapper():
    today = date.today().strftime("%d/%m/%Y")
    (d, m, y) = today.split('/')
    url_boe = 'https://www.boe.es/boe/dias/' + y + '/' + m + '/' + d + '/index.php?s=2B'
    # https://www.boe.es/boe/dias/2022/11/11/index.php?s=2B
    try:
        soup = read_html(url_boe)
    except requests.exceptions.RequestException:
        return 'ERROR en el acceso al BOE'

    li_tag = soup.find_all("li", {"class": "dispo"})
    result = "<ol>"
    for dispo in li_tag:
        title = dispo.find('p').get_text()
        link = dispo.find('a').get('href')
        result += ('<li>' + title + '\n<br><a href=\"https://www.boe.es' + link + '\">Descargar</a></li><br>')
    result += '</ol>'
    return result


def boam_webscrapper():
    # Get the website main page. Today's BOAM is not directly here, just a link to it
    url_boam = "https://sede.madrid.es/portal/site/tramites/menuitem.c5ae73b3eef2caf7cf32e4e5a8a409a0/?" \
               "vgnextoid=3ddc814231ede410VgnVCM1000000b205a0aRCRD&vgnextchannel=3ddc814231ede410VgnVCM" \
               "1000000b205a0aRCRD&vgnextfmt=default"

    try:
        soup = read_html(url_boam)
    except requests.exceptions.RequestException:
        return 'ERROR en el acceso al BOAM'

    # Find today's BOAM link and get the contents
    div_tag = soup.find_all("div", {"class": "col-sm-8 visited-color"})
    todays_boam = 'https://sede.madrid.es' + div_tag[0].find_all('a')[0].get('href')
    try:
        soup = read_html(todays_boam)
    except requests.exceptions.RequestException:
        return 'ERROR en el acceso al BOAM'

    # Extract the "Personal -> Convocatorias" links
    li_tag = soup.find_all("li", {"id": "61_S"})
    result = "<ol>"
    for dispo in li_tag[0].find_all('a'):
        title = dispo.get_text()
        link = dispo.get('href')
        result += ('<li>' + title + '\n<br><a href=\"https://sede.madrid.es' + link + '\">Descargar</a></li><br>')
    result += '</ol>'
    return result


def bocm_webscrapper():
    # Get the URL for today's summary.
    # It is embedded in the page and cannot be made up from today's date
    url_bocm = "https://www.bocm.es/ultimo-bocm"
    try:
        soup = read_html(url_bocm)
    except requests.exceptions.RequestException:
        return

    # Get today's BOCM and extract the "Autoridades y Personal" links
    div_tag = soup.find("div", {"class": "field field-name-field-content-name field-type-text field-label-hidden "
                                         "field-name-node-link"})
    todays_bocm = 'https://www.bocm.es' + div_tag.find('a').get('href')
    try:
        soup = read_html(todays_bocm)
    except requests.exceptions.RequestException:
        return 'ERROR en el acceso al BOCM'

    # Get date of BOCM. It will be needed later on to make up links to the PDF files
    div_tag = soup.find("span", {"class": "date-display-single"})
    (y, m, d) = div_tag.attrs['content'][0:10].split("-")

    div_tag = soup.find("div", {"class": "view-display-id-seccion_1"})  # Section #1 is Autoridades y Personal
    div_tag = div_tag.find("div", {"class": "view-grouping"})
    div_tag = div_tag.find_all("div", {"class": "field-item even"})
    i = 0
    result = "<ol>"
    for dispo in div_tag:
        i += 1
        if (i % 6) != 2:  # This is very, very specific. It will break easily but I found no other way
            continue
        result += (f'<li>{dispo.get_text()}<br><a href=\"https://www.bocm.es/boletin/CM_Orden_BOCM/'
                   f'{y}/{m}/{d}/BOCM-{y}{m}{d}-{i // 6 + 1}.PDF\">Descargar</a></li><br>\n\n')
    result += '</ol>'
    return result


def main():
    # Nothing gets published on Sunday
    if date.today().strftime('%A') == "Sunday":
        return

    read_ini_file()
    today = date.today().strftime("%d/%m/%Y")

    send_mail_msg(f'Ofertas de empleo en el BOE ({today})', boe_webscrapper())
    send_mail_msg(f'Ofertas de empleo en el Ayuntamiento de Madrid ({today})', boam_webscrapper())
    send_mail_msg(f'Ofertas de empleo en la Comunidad de Madrid ({today})', bocm_webscrapper())


if __name__ == '__main__':
    main()
