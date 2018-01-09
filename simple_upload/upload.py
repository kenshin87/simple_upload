import time
import random
import json
import urlparse

from django.http import HttpResponse

from upload_settings import ALLOWED_UPLOAD_FILE_TYPE
from upload_settings import MAX_UPLOAD_FILE_SIZE

from upload_helper import store_uploaded_file
from log_helper import get_correct_logger

logger = get_correct_logger()

class UploadDownloadAPI(object):

    @staticmethod
    def status_helper(status_json):
        responseDict = json.loads(status_json._container[0])
        file_url = responseDict["result"]["file_url"]
        return file_url

    @staticmethod
    def get_abs_path(file_name_para):
        return os.path.join(MEDIA_ROOT, file_name_para)

    @staticmethod
    def upload(request):
        """
            view that handles file upload via Ajax
        """

        # check upload permission
        error = ''
        new_file_name = ''
        allowed_upload_file_types = ALLOWED_UPLOAD_FILE_TYPE
        max_upload_file_size = MAX_UPLOAD_FILE_SIZE
        try:
            base_file_name = str(time.time()).replace('.', str(random.randint(0, 100000)))
            file_storage, new_file_name = store_uploaded_file(
            request, 'file-upload', allowed_upload_file_types, base_file_name,
            max_file_size=max_upload_file_size
            )
            logger.info(
                "docreaderxblock FileStoreAPI.upload try uploaded {}: success".format(str(new_file_name))
            )
        except Exception as e:
            logger.warning(
                "docreaderxblock FileStoreAPI.upload try uploaded {}: fail -- {}".format(str(new_file_name), e)
            )
            file = request.POST["file-upload"].file
            request.FILES = {}
            request.FILES["file-upload"] = file
            try:
                file_storage, new_file_name = store_uploaded_file(
                    request, 'file-upload', allowed_upload_file_types, base_file_name,
                    max_file_size=max_upload_file_size
                )
                logger.info(
                    "docreaderxblock FileStoreAPI.upload try uploaded {}: success".format(str(new_file_name))
                )
            except Exception as e:
                error = str(type(e)) + " - " + str(e)
                logger.error(
                    "docreaderxblock FileStoreAPI.upload except uploaded {}: fail".format(str(new_file_name), e)
                )
                raise Exception
        if error == '':
            result = 'SUCCESS'
            file_url = file_storage.url(new_file_name)
            parsed_url = urlparse.urlparse(file_url)
            file_url = urlparse.urlunparse(
                urlparse.ParseResult(
                    parsed_url.scheme,
                    parsed_url.netloc,
                    parsed_url.path,
                    '', '', ''
                )
            )
        else:
            result = ''
            file_url = ''

        return HttpResponse(json.dumps({
            'result': "SUCCESS",
            'msg': result,
            'error': error,
            'file_url': file_url,
        }), content_type="application/json")

    @staticmethod
    def download(request, dict_obj):
        BLOCK_SIZE = 8 * 1024
        path = dict_obj["abs_path"]
        try:
            file_descriptor = default_storage.open(path)
            app_iter = iter(partial(file_descriptor.read, BLOCK_SIZE), '')
            return Response(app_iter=app_iter)
        except:
            pass
 
