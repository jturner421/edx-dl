from dataclasses import dataclass

from bs4 import BeautifulSoup
import string

# soup = BeautifulSoup(open('/Downloaded/Course | CSS.0x | edX.html'), 'html.parser')
# section_names_list = []
# sections = soup.find_all(class_='outline-item section')

# find 1st section name soup. section = soup.find(class_='outline-item section')
# get next sub-section nav = r.find_next(class_="subsection-title")
# get 1st page of subsection nav = r.find_next(nav = r.find_next(class_="outline-item focusable"))

class Module:
    def __init__(self, module_name):
        self.module_name = module_name
        self.soup = None


    def get_html(self):
        self.soup = BeautifulSoup(open('/Users/jwt/PycharmProjects/edx-dl/Downloaded/Course | CSS.0x | edX.html'), 'html.parser')


class SubSection(Module):
    def __init__(self, module_name, sub_section_name):
        super().__init__(module_name)
        self.contents = []


# for count, section in enumerate(sections):
#     for value in section.descendants:
#         try:
#             if value.attrs['class'][0]== 'section-name':
#                 section_name = value.text.strip()
#                 section_url = value.attrs['id']
#                 section_url = section_url.partition(':')[2]
#                 print(f'Count - {count}, Section name = {section_name}')
#
#             elif value.attrs['class'][0] == 'subsection-title':
#                 while True:
#                     if sub_section_name == value.text.strip():
#                         break
#                     else:
#                         sub_section_name = value.text.strip()
#                         print(f'Count - {count}, Sub section name = {sub_section_name}')
#
#             elif value.attrs['class'][0]== "outline-item" and value.attrs['id'] is not None:
#                 content_url = value.attrs['id']
#                 content_url = content_url.partition(':')[2]
#                 content_name = value.contents[1].text.strip()
#                 print(f'Count - {count}, Content name = {content_name}')
#         except AttributeError:
#             continue
#
#
