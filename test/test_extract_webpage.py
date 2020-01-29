import pytest
from bs4 import BeautifulSoup

from edx_dl.scratch import Module, SubSection


@pytest.fixture()
def soup_object():
    soup = BeautifulSoup(open('/Users/jwt/PycharmProjects/edx-dl/test/Course | CSS.0x | edX.html'), 'html.parser')
    return soup

@pytest.fixture()
def subsection():
    module_0 = Module('Module 0')
    sub_section = SubSection(module_0, 'css_basics')
    return sub_section

def test_get_soup():
    module_0 = Module('Module 0')
    result = module_0.get_html()
    assert module_0.soup


def test_create_sub_section_instance():
    module_0 = Module('Module 0')
    sub_section = SubSection(module_0, 'css_basics')
    assert sub_section
    assert subsection.sub_section_name == 'css basics'


@pytest.mark.skip
def test_get_subsections_from_class_page():
    pass