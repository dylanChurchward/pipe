import os
import functions_framework
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
from google.cloud import storage
import tempfile
import io

@functions_framework.http
def reformat_image(request):
    request_json = request.get_json()
    client = storage.Client()
    source_bucket = client.get_bucket("src-photo")
    source_blob = source_bucket.get_blob(request_json['name'])
    file_name = source_blob.name
    _, temp_local_filename = tempfile.mkstemp()
    source_blob.download_to_filename(temp_local_filename)
    print(f"Image {file_name} was downloaded to {temp_local_filename}.")

    Original_Image = Image.open(temp_local_filename).resize((700, 500))
    blured_image1 = Original_Image.filter(ImageFilter.GaussianBlur(radius=int(request_json['radius'])))
    contrasted_image1 = ImageEnhance.Contrast(blured_image1)
    contrasted_image1 = contrasted_image1.enhance(int(request_json['enhanced']))
    cropped_image1 = contrasted_image1.crop((int(request_json['width']) // 4, int(request_json['height']) // 4,
                                              (int(request_json['width']) // 4) * 3, (int(request_json['width']) // 4) * 3))
    Grayscaled_image1 = ImageOps.grayscale(cropped_image1)
    rotated_image1 = Grayscaled_image1.rotate(float(request_json['rotate']))

    b = io.BytesIO() # create a BytesIO object
    rotated_image1.save(b, 'jpeg') # save image to BytesIO object
    Original_Image.close()
    
    edited_bucket = client.bucket("edited-photo")
    new_blob = edited_bucket.blob(file_name)
    #new_blob.upload_from_filename(temp_local_filename)
    new_blob.upload_from_string(b.getvalue(), content_type='image/jpeg')
    print(f"Edited image uploaded to: gs://edited-photo/{file_name}")
    return 'OK,' + request_json['name']