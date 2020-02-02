from dataclasses import dataclass

from bs4 import BeautifulSoup



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