from django.http import  FileResponse
from django.shortcuts import render
import qrcode
import os
from django.conf import settings
from datetime import datetime


def home(request):
    
    return render(request, 'generator/home.html')

def generate_qr(request):
        # Get the data from the form
    if request.method == 'POST':
        data = request.POST.get('qr_data', '')
        
        # Create QR code object
        qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            ) 

         # Add data to the QR code
        qr.add_data(data)
        qr.make(fit=True)
        # Create an image from the QR code
        img = qr.make_image(fill_color="black", back_color="white")

        # Save the image temporarily
         # Create media directory if it doesn't exist
        media_path = os.path.join(settings.MEDIA_ROOT, 'qrcodes')
        os.makedirs(media_path, exist_ok=True)

        # Generate a unique filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"qrcode_{timestamp}.png"
        file_path = os.path.join(media_path, filename)

        # Save the image
        img.save(file_path)

         # Create the URL for the image
        img_url = f'{settings.MEDIA_URL}qrcodes/{filename}'
        context = {"qr_code_url" : img_url,
                   "qr_data":data,
                   "filename":filename
                   }
        
        return render(request, "generator/result.html",context)
           

    # If not POST or no data, redirect to home
    return render(request, 'generator/home.html')


def download_qr(request):
   
   # check if GET request
    if request.method == 'GET':
        file_name = request.GET.get('filename', '')
        file_path = os.path.join(settings.MEDIA_ROOT, 'qrcodes', file_name)
   
     # Open the file and return it as a download
        if os.path.exists(file_path):
            response = FileResponse(open(file_path, 'rb'), content_type="image/png")
            response['Content-Disposition'] = f'attachment; filename="{file_name}"'
            return response
                

    # If something went wrong, redirect to home
    return render(request, 'generator/home.html')
