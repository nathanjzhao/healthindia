import requests
import boto3
from botocore.exceptions import NoCredentialsError
from botocore.config import Config

# AWS S3 bucket details
S3_BUCKET_NAME = 'jhubuckethophacks'
S3_OBJECT_NAME = 'doctor1.mp3'  # Name of the file when uploaded to S3
S3_REGION = 'us-east-2'  # Ensure this matches your bucket's region

# Ensure correct signature version and region are used
my_config = Config(
    region_name='us-east-2',
    signature_version='s3v4'
)

# AWS credentials are assumed to be configured via environment or AWS CLI
s3_client = boto3.client('s3', config=my_config)

text = "Hello, thank you for calling telemedicine, how can I help you?"

def text_to_speech(text):
    """
    text: str which is our model response
    returns: audio stream with elevenlabs
    """
    # Eleven Labs API setup
    CHUNK_SIZE = 1024
    url = "https://api.elevenlabs.io/v1/text-to-speech/fKe9ZDqkOtN9VMLdbWJ5"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": "sk_b459dc20d700919e6ccbaefd2f5297498f8f653669ee7f7e"
    }

    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }

    # Step 1: Get the audio data from Eleven Labs
    response = requests.post(url, json=data, headers=headers)

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
    except NoCredentialsError:
        print("Credentials not available. Please check your AWS credentials.")
    except Exception as e:
        print(f"Failed to upload file: {e}")
pass
