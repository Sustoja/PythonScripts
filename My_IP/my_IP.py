"""
Checks public IP and sends an email if it has changed
"""
import urllib.request
import urllib.error
import smtplib
import ssl
import configparser
import os

# Init file global variable.
CONFIG = configparser.ConfigParser(inline_comment_prefixes="#")


def read_ini():
    # Read INI file into a global variable.
    ini_file = __file__.replace('.py', '.ini')
    CONFIG.read(ini_file)


def get_ip_file():
    # The file where the IP is stored.
    # Same name as the script but with .txt extension
    return __file__.replace('.py', '.txt')


def save_current_ip(current_ip):
    """Write the current IP into a file for later use"""
    ip_file = get_ip_file()
    try:
        with open(ip_file, "w", encoding='utf-8') as file:
            file.write(current_ip)
    except IOError as error:
        raise SystemExit(f'Unable to write current IP in {ip_file}: {error.strerror}') from error


def get_old_ip():
    """Read the last IP that was stored in IP.txt file"""
    ip_file = get_ip_file()
    try:
        with open(ip_file, "r", encoding='utf-8') as file:
            return file.readline()
    except IOError as error:
        return '0.0.0.0'


def get_current_ip():
    """Get the current IP from an Internet service"""
    ip_service = CONFIG.get('APP', "IP_SERVICE")
    try:
        return urllib.request.urlopen(ip_service).read().decode('utf8')
    except urllib.error.URLError as error:
        raise SystemExit(f'Unable to get current IP from {ip_service}: {error.reason}') from error


def send_alert(body):
    """Sends an email via GMail. The body parameter is used as the email contents"""
    try:
        port = CONFIG.get('MAIL', "PORT")
        smtp_server = CONFIG.get('MAIL', "SMTP_SERVER")
        sender_email = CONFIG.get('MAIL', "SENDER_EMAIL")
        receiver_email = CONFIG.get('MAIL', "RECEIVER_EMAIL")
        password = CONFIG.get('MAIL', "PASSWORD")
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, body)
    except BaseException as error:
        raise SystemExit(f"Unable to send alert email via {smtp_server}") from error


def main():
    read_ini()

    """Checks if the IP has changed and alerts via email if so"""
    old_ip = get_old_ip()
    new_ip = get_current_ip()

    if old_ip != new_ip:
        send_alert(f"""Subject: La IP de casa ha cambiado\n
                    Nueva IP: {new_ip}
                    Antigua IP: {old_ip}""")
        save_current_ip(new_ip)


if __name__ == '__main__':
    main()
