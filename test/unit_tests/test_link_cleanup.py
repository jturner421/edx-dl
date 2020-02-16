from pathlib import Path

import pytest
import os

from edx_dl import web_page_save

@pytest.mark.skip
def testlink_cleanup():
    text = "\nPre Course Survey\n Completes"
    result = web_page_save._strip_characters_from_link_text(text)

    assert result == 'Pre Course Survey'


def test_create_save_web_page_path():
    output_path = '/Volumes/home/CloudStation/Contract_Law_From_Trust_to_Promise_to_Contract'
    url_key = 'What is a Contract?'
    section_name = 'Introduction'
    result = web_page_save.set_page_save_path(['01-Welcome_Materials_and_Office_Hours',
                                              '02-Introduction',
                                               '03-Unit_1-_Four_Principles'],section_name,output_path,url_key)

    assert os.fspath(result) == '/Volumes/home/CloudStation/Contract_Law_From_Trust_to_Promise_to_Contract/02-Introduction' \
                     '/What is a Contract?'

def test_create_symlink():
     p = Path('/Volumes/home/CloudStation/Contract_Law_From_Trust_to_Promise_to_Contract/'
              '01-Welcome_Materials_and_Office_Hours/What is a Contract?')

