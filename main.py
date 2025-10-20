from os import getenv, path, listdir
import logging
from dotenv import load_dotenv
from upload_photo import upload_photo

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    directory = getenv('FOLDER_NAME')
    url = getenv('MEDIAVIZ_PHOTO_UPLOAD_URL')
    bucket_name = getenv('MEDIAVIZ_BUCKET_NAME')
    token = getenv('MEDIAVIZ_API_REFRESH_TOKEN')
    user_id = getenv('MEDIAVIZ_USER_ID')
    company_id = getenv('MEDIAVIZ_COMPANY_ID')

    blur = 'True'
    colors = 'True'
    face_recognition = 'True'
    feature_extraction = 'True'
    image_classification = 'True'
    image_comparison = 'True'
    permitted_file_types = [
        '.jpg',
        '.jpeg',
        '.png'
    ]
    for index, file_name in enumerate(listdir(directory), start=25):
        ext = path.splitext(file_name)[1]
        if ext.lower() in permitted_file_types:
            logger.info(f"Uploading photo {index}: {file_name}")
            upload_photo(
                directory,
                file_name,
                str(index),
                url,
                bucket_name,
                company_id,
                user_id,
                bucket_name,
                blur,
                colors,
                face_recognition,
                feature_extraction,
                image_classification,
                image_comparison,
                None,
                token=token
            )
        else:
            logger.error(f"Failed to upload photo {index} due to incorrect extension: {ext}")
