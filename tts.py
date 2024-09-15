from dotenv import load_dotenv
import os
import requests
import boto3
from botocore.exceptions import NoCredentialsError
from botocore.config import Config
import io
import wave

load_dotenv() 

# AWS S3 bucket details
S3_BUCKET_NAME = 'jhubuckethophacks'
S3_OBJECT_NAME = 'doctor1.mp3'  # Name of the file when uploaded to S3
S3_REGION = 'us-east-2'  # Ensure this matches your bucket's region

language_voice_map = {
    'en': 'mCQMfsqGDT6IDkEKR20a',
    'hi': 'IvLWq57RKibBrqZGpQrC',
    'ta': 'gCr8TeSJgJaeaIoV4RWH'
}

# Ensure correct signature version and region are used
my_config = Config(
    region_name='us-east-2',
    signature_version='s3v4'
)

# AWS credentials are assumed to be configured via environment or AWS CLI
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    config=my_config
)

def text_to_speech(text, language='en'):
    """
    text: str which is our model response
    returns: audio stream with elevenlabs
    """
    # Eleven Labs API setup
    CHUNK_SIZE = 1024
    voice_id = language_voice_map.get(language)
    url = "https://api.elevenlabs.io/v1/text-to-speech/" + voice_id

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": os.getenv('ELEVEN_API_KEY')
    }

    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.7,
            "similarity_boost": 0.8
        }
    }

    # Step 1: Get the audio data from Eleven Labs
    response = requests.post(url, json=data, headers=headers)

    # Check if the response is successful and contains audio data
    if response.status_code != 200 or response.headers.get("Content-Type") != "audio/mpeg":
        print("Failed to retrieve valid audio data.")
        print("response.text: ", response.text)
        return None

    # Step 2: Save the audio data as binary data in memory
    binary_audio_data = b''  # Start with an empty binary string
    for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
        if chunk:
            binary_audio_data += chunk  # Concatenate binary data chunks

    # Step 3: Upload the binary data to S3
    try:
        # Uploading to S3
        s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=S3_OBJECT_NAME,
            Body=binary_audio_data,
            ContentType='audio/mpeg'
        )
        print(f"File uploaded successfully to https://{S3_BUCKET_NAME}.s3.{S3_REGION}.amazonaws.com/{S3_OBJECT_NAME}")

        # Generate a pre-signed URL for the uploaded file
        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': S3_BUCKET_NAME, 'Key': S3_OBJECT_NAME},
            ExpiresIn=3600  # URL expires in 1 hour
        )
        return presigned_url
    except NoCredentialsError:
        print("Credentials not available. Please check your AWS credentials.")
    except Exception as e:
        print(f"Failed to upload file: {e}")
