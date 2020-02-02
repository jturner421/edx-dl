import logging
from dataclasses import dataclass
import pywebcopy
from pywebcopy import save_webpage
from bs4 import BeautifulSoup
import lxml
import argparse


def pyweb_login(url, headers, username, password, session):
    """
    Log in user into the openedx website for pywebcopy.
    """
    payload = {'email': username,
               'password': password
               }

    response = session.post(url, data=payload, headers=headers)
    return response

def pywebcopy_get_headers(session, username, password, login_url):
    """
    Build the Open edX headers to create future requests.

    """
    logging.info('Building Pywebcopy headers for future requests.')

    headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
               'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko)'
                             'Chrome/79.0.3945.88 Safari/537.36'}
    session.get(login_url, headers=headers)

    csrftoken = session.cookies._cookies['courses.edx.org']['/']['csrftoken']
    headers['cookie'] = '; '.join([x.name + '=' + x.value for x in session.cookies])

    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/79.0.3945.88 Safari/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-CSRFToken': csrftoken.value,
        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
        'cookie': headers['cookie'],
        'Referer':login_url,
        'X-Requested-With': 'XMLHttpRequest'
    }
    logging.debug('PywebCopy Headers built: %s', headers)
    return headers

def save_web_page(unit_url, args, target_dir, filename_prefix, pyweb_session):
    kwargs = {'zip_project_folder': False,
              'url': unit_url.unit_page_url,
              'project_folder': target_dir,
              'over_write': True
              }
    save_webpage(**kwargs)

def extract_course_hierachy(sub_sec,section_list):
    for child in sub_sec:
        sub_sec_list = []
        # section = child.find(class_='section_title')
        if child is not None:
            # for i in child.parents:
            #     name = soup.find("h3")
            section_name = child.parent.parent.h3.text.strip()
            subsection_heading = child.h4.text.strip()
            print(subsection_heading)
            links = child.find_all('a')
            link_list = []
            for link in links:
                link_name = link.text.strip()
                try:
                    link_url = link.attrs['href']
                except TypeError:
                    continue
                l = {link_name: link_url}
                link_list.append(l)
            sub_section_links = {subsection_heading: link_list}
            sub_sec_list.append(sub_section_links)
        else:
            pass
        section_dict = {section_name: sub_sec_list}
        section_list.append(section_dict)
    return section_list

def main():
    username = 'jturner421@gmail.com'
    password =  'durin7456'
    LOGIN_API = 'https://courses.edx.org/login_ajax'
    course_url = 'https://courses.edx.org/courses/course-v1:Harvardx+HLS2X+1T2020/course/'
    # Prepare PyWebCopy Headers
    pyweb_session = pywebcopy.SESSION
    pyweb_session_headers = pywebcopy_get_headers(pyweb_session, username, password, LOGIN_API)

    # establish PyWebCopy Session
    pyweb_session = pyweb_login(LOGIN_API, pyweb_session_headers, username, password, pyweb_session)
    # Login
    section_names_list = []
    page = pywebcopy.SESSION.get(course_url)
    soup = BeautifulSoup (page.text, 'lxml')

    sub_sec = soup.find_all(class_="subsection accordion")
    section_list = []
    course_urls = extract_course_hierachy(sub_sec, section_list)
    print(section_list)

if __name__ == '__main__':
    main()