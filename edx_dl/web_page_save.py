import logging
from dataclasses import dataclass

from bs4 import BeautifulSoup

from edx_dl.edx_dl import EDX_HOMEPAGE


def pyweb_login(url, headers, username, password, session):
    """
    Log in user into the openedx website for pywebcopy.
    """
    payload = {'email': username,
               'password': password
               }

    response = session.post(url, data=payload, headers=headers)
    return response

def pywebcopy_get_headers(session, username, password):
    """
    Build the Open edX headers to create future requests.

    """
    logging.info('Building Pywebcopy headers for future requests.')

    headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
               'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko)'
                             'Chrome/79.0.3945.88 Safari/537.36'}
    session.get(EDX_HOMEPAGE, headers=headers)

    csrftoken = session.cookies._cookies['courses.edx.org']['/']['csrftoken']
    headers['cookie'] = '; '.join([x.name + '=' + x.value for x in session.cookies])

    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/79.0.3945.88 Safari/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-CSRFToken': csrftoken.value,
        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
        'cookie': headers['cookie'],
        'Referer': EDX_HOMEPAGE,
        'X-Requested-With': 'XMLHttpRequest'
    }
    logging.debug('PywebCopy Headers built: %s', headers)
    return headers


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
    section_names_list = []
    soup = BeautifulSoup(open('/Users/jwt/PycharmProjects/edx-dl/Downloaded/Course | CSS.0x | edX.html'), 'html.parser')
    #sections = soup.find_all(class_='outline-item section')
    #section_names_list = [value.h3.text for value in sections]
    sub_sec = soup.find_all(class_="subsection accordion")
    section_list = []
    course_urls = extract_course_hierachy(sub_sec, section_list)
    print(section_list)

if __name__ == '__main__':
    main()