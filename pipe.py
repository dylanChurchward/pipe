import os
import boto3
from PIL import Image, ImageFilter, ImageEnhance, ImageOps


def lambda_handler(event, context):
    session = boto3.Session(
        aws_access_key_id=os.environ['AWS_KEY'],
        aws_secret_access_key=os.environ['AWS_SECRET'],
        region_name=os.environ['AWS_REGIONS'])
    s3 = session.resource('s3')
    my_bucket = s3.Bucket(event.get('bucketname'))
    s3 = session.client('s3')
    for my_bucket_object in my_bucket.objects.all():
        print(my_bucket_object)
        s3.download_file(my_bucket_object.bucket_name, my_bucket_object.key,
                         '/tmp/' + 'finished_' + my_bucket_object.key)
        Original_Image = Image.open('/tmp/' + 'finished_' + my_bucket_object.key).resize((700, 500))
        blured_image1 = Original_Image.filter(ImageFilter.GaussianBlur(radius=int(event.get('radius'))))
        contrasted_image1 = ImageEnhance.Contrast(blured_image1)
        contrasted_image1 = contrasted_image1.enhance(int(event.get('enhanced')))
        cropped_image1 = contrasted_image1.crop((int(event.get("width")) // 4, int(event.get("height")) // 4,
                                              (int(event.get("width")) // 4) * 3, (int(event.get("width")) // 4) * 3))
        Grayscaled_image1 = ImageOps.grayscale(cropped_image1)
        rotated_image1 = Grayscaled_image1.rotate(float(event.get('rotate')))
        rotated_image1.save('/tmp/' + 'finished_' + my_bucket_object.key)
        s3.upload_file('/tmp/' + 'finished_' + my_bucket_object.key, 'image.save.bucket.tcss462562-2', 'finished_' + my_bucket_object.key)
        
    response = {"status": "success"}
    return response 