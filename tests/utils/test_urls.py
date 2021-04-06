from uuid import UUID

from app.utils.urls import get_frontend_download_url, get_direct_file_url


SAMPLE_KEY = bytes(range(32))
# the b64 has one trailing =, that we strip.
SAMPLE_B64 = 'AAECAwQFBgcICQoLDA0ODxAREhMUFRYXGBkaGxwdHh8'


def test_get_frontend_download_url_returns_frontend_url_without_filename(app):
    assert get_frontend_download_url(
        service_id=UUID(int=0), document_id=UUID(int=1), key=SAMPLE_KEY,
        filename=None
    ) == 'http://localhost:7001/d/{}/{}?key={}'.format(
        'AAAAAAAAAAAAAAAAAAAAAA',
        'AAAAAAAAAAAAAAAAAAAAAQ',
        SAMPLE_B64
    )


def test_get_frontend_download_url_returns_frontend_url_with_filename(app):
    assert get_frontend_download_url(
        service_id=UUID(int=0), document_id=UUID(int=1), key=SAMPLE_KEY,
        filename='file.pdf'
    ) == 'http://localhost:7001/d/{}/{}?key={}&filename=file.pdf'.format(
        'AAAAAAAAAAAAAAAAAAAAAA',
        'AAAAAAAAAAAAAAAAAAAAAQ',
        SAMPLE_B64
    )


def test_get_direct_file_url_gets_local_url_without_compressing_uuids(app):
    assert get_direct_file_url(
        service_id=UUID(int=0), document_id=UUID(int=1), key=SAMPLE_KEY,
        sending_method='link'
    ) == 'http://document-download.test/services/{}/documents/{}?key={}&sending_method={}'.format(
        '00000000-0000-0000-0000-000000000000',
        '00000000-0000-0000-0000-000000000001',
        SAMPLE_B64,
        'link'
    )
