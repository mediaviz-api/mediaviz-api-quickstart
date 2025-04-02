from os import getenv, path, listdir
from typing import List, Union, Dict, Any
import json
import requests
from requests import JSONDecodeError
import logging
import mimetypes
import base64
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import exifread
from io import BytesIO
import datetime
from dotenv import load_dotenv


load_dotenv()

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def upload_photo(
        directory: str,
        url: str,
        bucket_name: str,
        models: str,
        company_id: str,
        user_id: str,
        project_table_name: str,
        client_side_id: str = None,
        token: str = None
):
    # TODO: figure out how to pass client_side_id
    file_path = path.join(directory, file_name)
    print(f"file path is: {file_path}")
    headers_initial = {
        'Content-Type': "application/json",  # new
        'Authorization': token,
        'x-bucket-name': bucket_name,
        'x-file-name': file_name,
        'x-models': models,
        'x-company-id': company_id,
        'x-user-id': user_id,
        'x-project-table-name': project_table_name,
        'x-client-side-id': client_side_id,
        'x-title': file_name,
        'x-file-path': file_path,
        'x-description': None,
    }
    img_json, headers = preprocess_image(headers_initial, file_path, file_name)
    print(f"headers: {headers}")
    request_with_headers_and_photo(url, "post", headers, img_json)


# Helpers
def request_with_headers_and_photo(url: str, request_type: str, heads: Union[Dict, None], json: Any):
    response = ''

    if request_type == 'get':
        response = requests.get(url, headers=heads)
    elif request_type == 'post':
        response = requests.post(url, json=json, headers=heads)

    try:
        response_json = response.json()
        print(f"Request with body {response.status_code}: {response_json}")
        return response_json
    except JSONDecodeError as e:
        print(f"Caught error: {e}")


def preprocess_image(headers, file_path, file_name, max_size=400 * 1024, max_dimension=512):
    """
    Extract metadata from an image and resize it in a single operation
    Limits both dimensions to max_dimension while maintaining aspect ratio
    Returns both the metadata and the resized image data
    """
    try:
        mime_type, _ = mimetypes.guess_type(file_name)
        # Create a copy of headers to avoid modifying the original
        headers_copy = headers.copy()

        # Open the image file once
        with Image.open(file_path) as img:
            # Store the original format and dimensions
            img_format = img.format
            original_width, original_height = img.size

            # Get all EXIF data
            exif_data = {}
            if hasattr(img, '_getexif') and img._getexif():
                exif_info = img._getexif()
                if exif_info:
                    for tag, value in exif_info.items():
                        decoded = TAGS.get(tag, tag)
                        exif_data[decoded] = value

            # Extract GPS info if available
            gps_info = {}
            if 'GPSInfo' in exif_data:
                for key, value in exif_data['GPSInfo'].items():
                    decoded = GPSTAGS.get(key, key)
                    gps_info[decoded] = value

            # Format GPS coordinates if available
            latitude = None
            longitude = None
            if gps_info:
                if 'GPSLatitude' in gps_info and 'GPSLatitudeRef' in gps_info:
                    lat = gps_info['GPSLatitude']
                    lat_ref = gps_info['GPSLatitudeRef']
                    latitude = convert_to_degrees(lat)
                    if lat_ref != 'N':
                        latitude = -latitude

                if 'GPSLongitude' in gps_info and 'GPSLongitudeRef' in gps_info:
                    lon = gps_info['GPSLongitude']
                    lon_ref = gps_info['GPSLongitudeRef']
                    longitude = convert_to_degrees(lon)
                    if lon_ref != 'E':
                        longitude = -longitude

            # Format date taken if available
            date_taken = None
            if 'DateTimeOriginal' in exif_data:
                date_str = exif_data['DateTimeOriginal']
                try:
                    date_taken = datetime.datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
                except ValueError:
                    date_taken = date_str

            # Resolution information
            x_resolution = None
            y_resolution = None
            if 'XResolution' in exif_data:
                x_resolution = exif_data['XResolution']
            if 'YResolution' in exif_data:
                y_resolution = exif_data['YResolution']

            # Add metadata to headers
            headers_copy['x-size'] = f"{original_width}x{original_height}"
            headers_copy['x-source-resolution-x'] = str(x_resolution) if x_resolution else None
            headers_copy['x-source-resolution-y'] = str(y_resolution) if y_resolution else None
            headers_copy['x-date-taken'] = str(date_taken) if date_taken else None
            headers_copy['x-latitude'] = str(latitude) if latitude is not None else None
            headers_copy['x-longitude'] = str(longitude) if longitude is not None else None

            # Resize image to max dimensions if necessary
            if original_width > max_dimension or original_height > max_dimension:
                # Calculate the scaling factor to maintain aspect ratio
                scale = min(max_dimension / original_width, max_dimension / original_height)
                new_width = int(original_width * scale)
                new_height = int(original_height * scale)

                # Resize the image using high-quality LANCZOS resampling
                img_resized = img.resize((new_width, new_height), Image.LANCZOS)

                # Update metadata with new dimensions
                headers_copy['x-resized-dimensions'] = f"{new_width}x{new_height}"
            with BytesIO() as buffer:
                img_resized.save(buffer, format=img_format)
                buffer.seek(0)
                resized_image_bytes = buffer.getvalue()

                # Create the JSON object for API submission
                base64_content = base64.b64encode(resized_image_bytes).decode('utf-8')
                result_json = {
                    "file_content": base64_content,
                    "file_name": file_name,
                    "mimetype": mime_type
                }

            return result_json, headers_copy

    except Exception as e:
        return {'error': str(e)}, None


def convert_to_degrees(value):
    """Helper function to convert the GPS coordinates stored in the EXIF to degrees"""
    degrees = float(value[0])
    minutes = float(value[1]) / 60.0
    seconds = float(value[2]) / 3600.0
    return degrees + minutes + seconds


if __name__ == '__main__':
    directory = './test_photos'
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
                url,
                bucket_name,
                models,
                company_id,
                user_id,
                bucket_name,
                None,
                token=token
            )
