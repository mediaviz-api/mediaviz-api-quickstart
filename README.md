# MediaViz-API-Photo-Uploader
Upload photos and request preliminary analysis from the MediaViz API.

Steps:
1. Clone into the repo using HTTPS: git clone https://github.com/imaige/MediaViz-API-Photo-Uploader
2. Navigate to the project root in your command line
3. Install project requirements: pip3 install -r requirements.txt
4. Add your folder of photos to the root of the project.
5. Create .env file using the window navigator, or using the command line: touch .env
6. Add the required items to your .env file:
    MEDIAVIZ_PHOTO_UPLOAD_URL=[upload_URL]
    MEDIAVIZ_BUCKET_NAME=[z-photos-X-XXXX-XXXXXXXX-XXXXXXXXX-XXX]
    MEDIAVIZ_API_REFRESH_TOKEN=[refresh_token]
    MEDIAVIZ_USER_ID=[user_id]
    MEDIAVIZ_COMPANY_ID=[company_id]
    FOLDER_NAME=[your_folder_name]
7. Select the subset of models you would like to use by commenting/uncommenting one of the string options in the bottom section of the file that look like: models = "image_comparison_model, face_recognition_model, blur_model, colors_model"
8. Run the script in your command line: python main.py
