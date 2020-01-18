import pytest

from edx_dl import edx_dl


def test_check_for_duplicate_url_to_save(class_startup, url=None):
    result = edx_dl.common.UnitUrl.check_for_duplicate_url_to_save(url)
    assert result


@pytest.mark.skip
def test_check_for_base_url(class_setup):
    assert BASE_URL == 'https://courses.edx.org'