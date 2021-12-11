import requests
from bs4 import BeautifulSoup
from datetime import date
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import configparser


# Init file global variable.
CONFIG = configparser.ConfigParser(inline_comment_prefixes="#")


def read_ini():
    # Read INI file into a global variable.
    ini_file = __file__.replace('.py', '.ini')
    CONFIG.read(ini_file)


def send_msg(subject, body):
    # Create message container - the correct MIME type is multipart/alternative.
    port = CONFIG.get('MAIL', "PORT")
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
    except:
        print('ERROR al enviar el correo. Comprueba los valores del fichero .INI')


def scrapping_boe(url):
    response = requests.get(url)
    if response.status_code != 200:
        return '!!! ERROR en el acceso al BOE'

    soup = BeautifulSoup(response.text, "html.parser")
    liTag = soup.find_all("li", {"class": "dispo"})
    result = "<ol>"
    for dispo in liTag:
        title = dispo.find('p').get_text()
        link = dispo.find('a').get('href')
        result += ('<li>' + title + '\n<br><a href=\"https://www.boe.es' + link + '\">Descargar</a></li><br>')
    result += '</ol>'
    return result


def scrapping_boam(url):
    # Get the URL for today's BOAM.
    # It is embedded in the body and cannot be built directly from today's date
    response = requests.get(url)
    if response.status_code != 200:
        return '!!! ERROR en el acceso al BOAM'
    soup = BeautifulSoup(response.text, "html.parser")
    divTag = soup.find_all("div", {"class": "col-sm-8 visited-color"})
    todaysBOAM = 'https://sede.madrid.es' + divTag[0].find_all('a')[0].get('href')

    # Get today's BOAM and extract the "Personal -> Convocatorias" links
    response = requests.get(todaysBOAM)
    if response.status_code != 200:
        return '!!! ERROR en el acceso al BOAM'
    soup = BeautifulSoup(response.text, "html.parser")
    liTag = soup.find_all("li", {"id": "61_S"})
    result = "<ol>"
    for dispo in liTag[0].find_all('a'):
        title = dispo.get_text()
        link = dispo.get('href')
        result += ('<li>' + title + '\n<br><a href=\"https://sede.madrid.es' + link + '\">Descargar</a></li><br>')
    result += '</ol>'
    return result


def scrapping_bocm(url):
    # Get the URL for today's summary.
    # It is embedded in the body and cannot be built directly from today's date
    response = requests.get(url)
    if response.status_code != 200:
        return '!!! ERROR en el acceso al BOCM'
    soup = BeautifulSoup(response.text, "html.parser")
    divTag = soup.find("div", {"class": "field field-name-field-content-name field-type-text field-label-hidden "
                                        "field-name-node-link"})
    todaysBOCM = 'https://www.bocm.es' + divTag.find('a').get('href')

    # Get today's BOCM and extract the "Autoridades y Personal" links
    response = requests.get(todaysBOCM)
    if response.status_code != 200:
        return '!!! ERROR en el acceso al BOCM'
    soup = BeautifulSoup(response.text, "html.parser")

    # Get date of BOCM. It will be needed later on to make up links to the PDF files
    divTag = soup.find("span", {"class": "date-display-single"})
    (y, m, d) = divTag.attrs['content'][0:10].split("-")

    divTag = soup.find("div", {"class": "view-display-id-seccion_1"})  # Section #1 is Autoridades y Personal
    divTag = divTag.find("div", {"class": "view-grouping"})
    divTag = divTag.find_all("div", {"class": "field-item even"})
    i = 0
    result = "<ol>"
    for dispo in divTag:
        i += 1
        if (i % 6) != 2:  # This is very, very specific. It will break easily but I found no other way
            continue
        result += (f'<li>{dispo.get_text()}<br><a href=\"https://www.bocm.es/boletin/CM_Orden_BOCM/'
                   f'{y}/{m}/{d}/BOCM-{y}{m}{d}-{i // 6 + 1}.PDF\">Descargar</a></li><br>\n\n')
    result += '</ol>'
    return result


def main():
    if date.today().strftime('%A') == "Sunday":
        return
    today = date.today().strftime("%d/%m/%Y")
    (d, m, y) = today.split('/')

    read_ini()

    URLBOE = 'https://www.boe.es/boe/dias/' + y + '/' + m + '/' + d + '/index.php?s=2B'
    responseBOE = scrapping_boe(URLBOE)
    send_msg(f'Ofertas de empleo en el BOE ({today})', responseBOE)

    URLBOAM = "https://sede.madrid.es/portal/site/tramites/menuitem.c5ae73b3eef2caf7cf32e4e5a8a409a0/?" \
              "vgnextoid=3ddc814231ede410VgnVCM1000000b205a0aRCRD&vgnextchannel=3ddc814231ede410VgnVCM" \
              "1000000b205a0aRCRD&vgnextfmt=default"
    responseBOAM = scrapping_boam(URLBOAM)
    send_msg(f'Ofertas de empleo en el Ayuntamiento de Madrid ({today})', responseBOAM)

    URLBOCM = "https://www.bocm.es/ultimo-bocm"
    responseBOCAM = scrapping_bocm(URLBOCM)
    send_msg(f'Ofertas de empleo en la Comunidad de Madrid ({today})', responseBOCAM)

    return


if __name__ == '__main__':
    main()
