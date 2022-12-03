NPTEL Certificate Verifier is a Python based NPTEL Certificate verifier. It uses the QR Code of the uploaded image, and fetches the certificate from the official NPTEL archives. It then compares the two images and sorts them in three different folders - Genuine Certificates, Fake Certificates and UnProcessed Images., according to the comparision between uploaded image by student and downloaded image from NPTEL. 

Program by : Saieed Shafi
02-12-2022
_______________________________________________________________________________________________________________

Repository INFO:
1. The main python program is a single file named 'NPTEL Certificate Verifier.py'
2. The exe for windows is in a zip file in exe folder of repo. Same can b found in releases
_______________________________________________________________________________________________________________

Requirements:
1. Folder of images of certificates in jpg extension
2.  Copy all the images (which need verification) to the 'images' folder. Make sure the images are in .jpg extension and not jpeg or anything else. 
	Also make sure the images are in full resolution else the program may not work.
3. An Internet Connection
_______________________________________________________________________________________________________________

How to Use : 
1. After ensuring the requirements are fulfilled, open NPTEL Certificate Verifier
2. click on 'Select Button' and select the folder containing images of certificates uploaded by students
3. click Start Verifying
4. Wait for the program to show the completed message.
_______________________________________________________________________________________________________________

OUTPUT:

You will see output in the three newly created folders : Genuine Certificates, Fake Certificates and UnProcessed 


NOTE: The program may seem to be NOT RESPONDING, but if you see "temp.jpg" image in the same folder as the program, it means the program is working. it takes about 1-2 seconds/image to process. Please wait accordingly and do not close the program window. 