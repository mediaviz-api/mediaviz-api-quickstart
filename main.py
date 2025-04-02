from os import getenv, path, listdir
import logging
from dotenv import load_dotenv
from upload_photo import upload_photo

load_dotenv()

logger = logging.getLogger()
logger.setLevel(logging.INFO)


if __name__ == '__main__':
    directory = getenv('FOLDER_NAME')
    url = getenv('MEDIAVIZ_PHOTO_UPLOAD_URL')
    bucket_name = getenv('MEDIAVIZ_BUCKET_NAME')
    token = getenv('MEDIAVIZ_API_REFRESH_TOKEN')
    user_id = getenv('MEDIAVIZ_USER_ID')
    company_id = getenv('MEDIAVIZ_COMPANY_ID')

    # models = "image_comparison_model, face_recognition_model, blur_model, colors_model"
    # models = "image_comparison_model, blur_model, colors_model, feature_extraction_model"
    # models = "image_comparison_model, feature_extraction_model, blur_model"
    # models = "image_comparison_model, feature_extraction_model, colors_model"
    # models = "image_comparison_model, blur_model, colors_model, face_recognition_model, feature_extraction_model"
    # models = "colors_model, feature_extraction_model, image_classification_model"
    # models = "face_recognition_model, feature_extraction_model, image_classification_model"
    models = "blur_model"
    # all
    # models = "image_comparison_model, blur_model, colors_model, face_recognition_model, feature_extraction_model, image_classification_model"
    for file_name in listdir(directory):
        ext = path.splitext(file_name)[1]
        permitted_file_types = [
            '.jpg',
            '.jpeg',
            '.png'
        ]
        if ext.lower() in permitted_file_types:
            upload_photo(
                directory,
                file_name,
                url,
                bucket_name,
                models,
                company_id,
                user_id,
                bucket_name,
                None,
                token=token
            )
