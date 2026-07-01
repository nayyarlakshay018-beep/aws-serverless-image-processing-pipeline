import os
import boto3
from PIL import Image
from io import BytesIO
from urllib.parse import unquote_plus
import traceback

s3 = boto3.client("s3")
sns = boto3.client("sns")

# Environment Variables
OUTPUT_BUCKET = os.environ["OUTPUT_BUCKET"]
TOPIC_ARN = os.environ["TOPIC_ARN"]


def lambda_handler(event, context):
    try:
        print("===== Lambda Started =====")
        print("Event:", event)

        bucket = event["Records"][0]["s3"]["bucket"]["name"]
        key = unquote_plus(event["Records"][0]["s3"]["object"]["key"])

        print(f"Reading image from: {bucket}/{key}")

        response = s3.get_object(Bucket=bucket, Key=key)

        print("Reading image bytes...")
        image_bytes = response["Body"].read()

        print("Opening image...")
        image = Image.open(BytesIO(image_bytes))
        print("Image opened successfully")

        print("Starting resize...")
        image = image.resize((800, 800))
        print("Resize complete")

        print("Creating buffer...")
        buffer = BytesIO()

        print("Starting RGB conversion...")
        image = image.convert("RGB")
        print("RGB conversion complete")

        print("Saving image...")
        image.save(buffer, format="JPEG")
        print("Image saved successfully")

        buffer.seek(0)

        output_key = "resized-" + key

        print(f"Uploading to bucket: {OUTPUT_BUCKET}")

        s3.put_object(
            Bucket=OUTPUT_BUCKET,
            Key=output_key,
            Body=buffer.getvalue(),
            ContentType="image/jpeg"
        )

        print("Upload complete")

        print("Sending SNS notification...")

        sns.publish(
            TopicArn=TOPIC_ARN,
            Subject="Image Processed Successfully",
            Message=f"{key} has been resized successfully."
        )

        print("SNS notification sent")

        print("===== Lambda Finished Successfully =====")

        return {
            "statusCode": 200,
            "body": "Success"
        }

    except Exception as e:
        print("===== ERROR =====")
        print(str(e))
        traceback.print_exc()
        raise