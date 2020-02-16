import logging
import os
import pathlib

import pywebcopy
from bs4 import BeautifulSoup
from pywebcopy import save_webpage


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
        'Referer': login_url,
        'X-Requested-With': 'XMLHttpRequest'
    }
    logging.debug('PywebCopy Headers built: %s', headers)
    return headers


def save_web_page(url, target_dir, pyweb_session):
    kwargs = {'zip_project_folder': False,
              'url': url,
              'project_folder': target_dir,
              'over_write': True
              }
    save_webpage(**kwargs)


def extract_course_hierachy(sub_sec, section_list):
    sub_sec_list = []
    for child in sub_sec:
        if child is not None:

            section_name = child.parent.parent.h3.text.strip()
            section_name = section_name.replace(":", "").replace("-", "").replace(" ", "_")
            subsection_heading = child.h4.text.strip()
            links = child.find_all('a')
            link_list = []
            for link in links:
                link_name = link.text.strip()
                if link_name.find("\n"):
                    link_name = _strip_characters_from_link_text(link_name)
                try:
                    link_url = link.attrs['href']
                except TypeError:
                    continue
                l = {link_name: link_url}
                link_list.append(l)
            sub_section_links = {'subsection': subsection_heading, 'links': link_list}
            sub_sec_list.append(sub_section_links)
        else:
            pass
        section_dict = {'section_name': section_name, 'subsection': subsection_heading}
        section_list.append(section_dict)
    return section_list, sub_sec_list


def _strip_characters_from_link_text(link_name):
    if "\n" in link_name:
        link_name = link_name[:link_name.find("\n")]

    #link_name = link_name.strip('\n')

    return link_name


def set_page_save_path(file_list, substring, output_path, url_key):
    # save_path = next(section_name for section_name in file_list if section_name in section_name)
    save_path = next(i for i in file_list if substring in i)
    page_save_path = pathlib.Path(output_path).joinpath(save_path, url_key)
    return page_save_path


def create_directory_based_on_downloaded_videos(output_path):
    file_list = []
    for entry in os.scandir(output_path):
        if entry.is_dir():
            file_list.append(entry.name)
    return file_list


def create_url_dictionary(course_urls):
    url_dict = dict((i['subsection'], i['links']) for i in course_urls[1])
    return url_dict


def find_subsections(soup):
    sub_sec = soup.find_all(True, {"class": ["subsection accordion", "subsection accordion graded scored"]})
    return sub_sec

def create_symlink(page_save_path):
    source = list(page_save_path.rglob('*.html'))
    dest = page_save_path / 'index.html'
    os.symlink(source[0], dest)


def main():

    username = 'jturner421@gmail.com'
    password = 'durin7456'
    LOGIN_API = 'https://courses.edx.org/login_ajax'
    course_url = 'https://courses.edx.org/courses/course-v1:Harvardx+HLS2X+1T2020/course/'
    # Prepare PyWebCopy Headers
    pyweb_session = pywebcopy.SESSION
    pyweb_session_headers = pywebcopy_get_headers(pyweb_session, username, password, LOGIN_API)
    base_output_path = ('/Volumes/home/CloudStation')
    # establish PyWebCopy Session
    pyweb_session = pyweb_login(LOGIN_API, pyweb_session_headers, username, password, pyweb_session)
    # Login
    section_names_list = []
    page = pywebcopy.SESSION.get(course_url)
    soup = BeautifulSoup(page.text, 'lxml')
    course_name = soup.find(class_='page-header-main').h2.text.strip()
    course_name = course_name.replace(":", "").replace("-", "").replace(" ", "_")
    output_path = pathlib.Path(base_output_path).joinpath(course_name)

    sub_sec = find_subsections(soup)
    section_list = []
    course_urls = extract_course_hierachy(sub_sec, section_list)
    # create master dictionary of urls for loookup
    # url_dict = dict((i['subsection'], i['links']) for i in course_urls[1])
    url_dict = create_url_dictionary(course_urls)
    # section_list_dict = dict((i['section_name'], i['subsections']) for i in course_urls[0])
    # get output directories for course
    file_list = create_directory_based_on_downloaded_videos(output_path)
    # get key
    for sub_section in course_urls[0]:
        section_name = sub_section['section_name']
        url_key = sub_section['subsection']
        # get course list
        urls = url_dict[url_key]
        page_save_path = set_page_save_path(file_list, section_name, output_path, url_key)
        url = urls[0][url_key]
        save_web_page(url, os.fspath(page_save_path), pyweb_session)
        # TODO Create symbolic link back to saved page
        create_symlink(page_save_path)
        print(section_name)




if __name__ == '__main__':
    main()
