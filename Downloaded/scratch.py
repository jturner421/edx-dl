from bs4 import BeautifulSoup
import string

soup = BeautifulSoup(open('/Users/jwt/PycharmProjects/edx-dl/Course | CSS.0x | edX.html'),'html.parser')
section_names_list = []
section = soup.find_all(class_='outline-item section')
# get the Module name
for index, child in enumerate(section):
    result = child.text.split('\n')
    module_name = ""
    found = False
    for string in result:
        if string != "":
            if 'Module' in string:
                module_name = string
                break

    for i, value in enumerate(child.contents):
        pass
        if value.attrs['class'][0]== 'section-name':
            url = value.attrs['id']
            url = url.partition(':')[2]
        if 'Module' in value.text:
            module_name = value.text
        # if len(value)> 0:
        #     if value[i].attrs['class'][0]=='section-name':
        #         module_name = value[i].text





