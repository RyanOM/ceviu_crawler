
# -*- coding: utf-8 -*-
import os, time, re
import urlparse, random, getpass

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


def getEmail():
    email_verrified = False
    while not email_verrified:
        email = raw_input('Ceviu Email:')
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            email_verrified = True
            return email
        else:
            print "Email not valid. Please try again"

            
def getPassword():
    pw_verrified = False
    while not pw_verrified:
        password = getpass.getpass('Password:')
        if len(password) >= 6:
            pw_verrified = True
            return password
        else:
            print "Password must have 6 or more characters"


def get_latest_job_id(homepagesoup):
    link_items = homepagesoup.find_all(class_='carousel')[0]
    job_url = link_items.contents[1].attrs['href']
    job_id = re.findall('[0-9]+', job_url)[0]
    return job_id


def check_job_page(job_id, page_html):

    if 'encontrada' in page_html.text:
        print '404: %s' % job_id
    elif 'pode ser visualizado por candidatos premium' in page_html.text:
        print 'premium: %s' % job_id
    elif 'VEJA OUTROS NA MESMA' in page_html.text:
        print 'Job no longer avaliable: %s' % job_id
    else:
        html = page_html.prettify("utf-8")
        file_name = "ceviu-%s.html" % job_id
        file_path = 'job_offers/ceviu/%s' % file_name
        if not os.path.isfile(file_path):
            with open(file_path, "wb") as htmlfile:
                htmlfile.write(html)
                print'Created file: %s' % file_name
        else:
            print'File already exists: %s' % file_name


def get_job_opportunity(browser, job_id):
    job_url = 'http://www.ceviu.com.br/vaga/%s' % job_id
    browser.get(job_url)
    time.sleep(random.uniform(0.5, 2.5))
    page_html = BeautifulSoup(browser.page_source)
    check_job_page(job_id, page_html)


def main():
    email = getEmail()
    password = getPassword()

    browser = webdriver.Firefox()
    browser.get('https://www.ceviu.com.br/login')

    emailElement = browser.find_element_by_id("p-login-usuario")
    emailElement.send_keys(email)
    passwordElement = browser.find_element_by_id("p-login-senha")
    passwordElement.send_keys(password)
    passwordElement.submit()

    os.system('clear')
    print("[+] Success! You are now logged in with %s." % email)
    print("[+] The bot is starting!")

    home_page = BeautifulSoup(browser.page_source)
    #latest_job_id = get_latest_job_id(home_page)
    latest_job_id = '466608'

    latest_id_int = int(latest_job_id) + 1
    for job_id in reversed(range(latest_id_int)):
        get_job_opportunity(browser, job_id)


if __name__ == '__main__':
    main()
