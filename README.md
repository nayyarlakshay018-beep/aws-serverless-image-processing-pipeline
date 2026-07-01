# aws-serverless-image-processing-pipeline
Built a serverless image processing pipeline using AWS Lambda, Amazon S3, Amazon SNS, CloudWatch, IAM, and Python (Pillow). Images uploaded to an S3 bucket automatically trigger a Lambda function that processes the image, stores the output in another S3 bucket, logs execution in CloudWatch, and sends an email notification via Amazon SNS.
