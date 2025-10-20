# MediaViz-API-Photo-Uploader
Upload photos and request preliminary analysis from the MediaViz API.

Steps:
1. Clone into the repo using HTTPS: git clone https://github.com/mediaviz-api/Mediaviz-Api-Quickstart.git
2. Navigate to the project root in your command line
3. Set up and the project and install project requirements by running: sh setup3.sh
4. Add your folder of photos to the root of the project.
5. Create .env file using the window navigator, or using the command line: touch .env
6. Add the required items to your .env file: \
    MEDIAVIZ_PHOTO_UPLOAD_URL=[upload_URL] \
    MEDIAVIZ_BUCKET_NAME=[z-photos-X-XXXX-XXXXXXXX-XXXXXXXXX-XXX] \
    MEDIAVIZ_API_REFRESH_TOKEN=[refresh_token] \
    MEDIAVIZ_USER_ID=[user_id] \
    MEDIAVIZ_COMPANY_ID=[company_id] \
    FOLDER_NAME=[your_folder_name] 
7. Select the subset of models you would like to use by adjusting the model selection options to either 'True' or 'False' in main.py:

    blur = 'True'
   
    colors = 'True'
   
    face_recognition = 'True'
   
    feature_extraction = 'True'
   
    image_classification = 'True'
   
    image_comparison = 'True'
   
   Note that these should be in string form, as shown above.
8. Run the script in your command line: python main.py
