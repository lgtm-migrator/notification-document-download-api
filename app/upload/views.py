import pathlib

from flask import Blueprint, current_app, jsonify, request

from app import document_store
from app.utils import get_mime_type
from app.utils.mlwr import upload_to_mlwr
from app.utils.authentication import check_auth
from app.utils.urls import get_direct_file_url, get_api_download_url

upload_blueprint = Blueprint('upload', __name__, url_prefix='')
upload_blueprint.before_request(check_auth)


@upload_blueprint.route('/services/<uuid:service_id>/documents', methods=['POST'])
def upload_document(service_id):
    if 'document' not in request.files:
        return jsonify(error='No document upload'), 400

    mimetype = get_mime_type(request.files['document'])
    if not mime_type_is_allowed(mimetype, service_id):
        return jsonify(
            error="Unsupported document type '{}'. Supported types are: {}".format(
                mimetype,
                current_app.config['ALLOWED_MIME_TYPES']
            )
        ), 400
    file_content = request.files['document'].read()

    filename = request.form.get('filename')
    file_extension = None
    if filename and '.' in filename:
        file_extension = ''.join(pathlib.Path(filename.lower()).suffixes).lstrip('.')

    # Our MIME type auto-detection resolves CSV content as text/plain,
    # so we fix that if possible
    if (filename or '').lower().endswith('.csv') and mimetype == 'text/plain':
        mimetype = 'text/csv'

    sending_method = request.form.get('sending_method')

    if current_app.config["MLWR_HOST"]:
        sid = upload_to_mlwr(file_content)
    else:
        sid = False

    document = document_store.put(service_id, file_content, sending_method=sending_method, mimetype=mimetype)

    return jsonify(
        status='ok',
        document={
            'id': document['id'],
            'direct_file_url': get_direct_file_url(
                service_id=service_id,
                document_id=document['id'],
                key=document['encryption_key'],
                sending_method=sending_method,
            ),
            'url': get_api_download_url(
                service_id=service_id,
                document_id=document['id'],
                key=document['encryption_key'],
                filename=filename,
            ),
            'mlwr_sid': sid,
            'filename': filename,
            'sending_method': sending_method,
            'mime_type': mimetype,
            'file_size': len(file_content),
            'file_extension': file_extension,
        }
    ), 201


def mime_type_is_allowed(mimetype, service_id):
    if mimetype in current_app.config['ALLOWED_MIME_TYPES']:
        return True

    # Payload is formatted like "service_id1:mime1,service_id2:mime2"
    # Example:
    # "fccd5d86-afd6-491b-afa8-2ff592e1404f:application/octet-stream,95365643-8126-46f1-a222-e0c51fa918f2:application/json"
    return f"{service_id}:{mimetype}" in current_app.config['EXTRA_MIME_TYPES']
