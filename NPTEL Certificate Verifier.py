from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import cv2
from pyzbar.pyzbar import decode
import requests
import urllib
from bs4 import BeautifulSoup as bs
import glob
import os

root = Tk()
root.title('NPTEL Certificate Verifier by Saieed ')
root.geometry('750x250')
imageFolder = Label(root,text="/images_folder_location", borderwidth=1, relief="solid",padx=2, pady=3, width = 50).grid(row=1, column=1)

aburl="https://archive.nptel.ac.in/noc/Ecertificate/?q="
fake="FakeCertificates"
gen="GenuineCertificates"
unp="UnProcessed"
folder_selected=""

def createdir(dirName):
    try:
        # Create target Directory
        os.mkdir(dirName)
         
    except FileExistsError:
        print()        
    
    # Create target Directory if don't exist
    if not os.path.exists(dirName):
        os.mkdir(dirName)

def selectFolder():
    global folder_selected
    folder_selected = filedialog.askdirectory()
    global imageFolder
    imageFolder = Label(root,text=folder_selected, borderwidth=1, relief="solid",padx=2, pady=3,width = 50).grid(row=1, column=1)
    
def verify():
    i=0
    createdir(gen)
    createdir(fake)
    createdir(unp)
    genNo=0
    fakeNo=0
    globLocation=""
    globLocation=folder_selected + "/*.jpg"
    images = glob.glob(globLocation)
    for image in images:
        i=i+1
        global img
        img = cv2.imread(image) #read the image
        x=decode(img)
        if not x: #if qrcode is not read
            cv2.imwrite('UnProcessed/Certificate{j}.jpg'.format(j=i), img)
        else:
            for code in x:
                url=code.data.decode('utf-8') #url from qrcode of uploaded image
                url=aburl+url[38:]
                soup = bs(requests.get(url).content, "html.parser")  #get the page from url
                for img in soup.find_all("img"): 
                    img_src = img.attrs.get("src") #extracting dataURI from nptel site Certificate
                    response = urllib.request.urlopen(img_src)
                    with open('temp.jpg', 'wb') as f:
                        f.write(response.file.read()) #save jpg froom dataURI
                        imgOrig = cv2.imread(image)   #reading Uploaded Image
                        imageNPTEL = cv2.imread('temp.jpg') #reading Downloaded Image
                        difference = cv2.subtract(imgOrig, imageNPTEL) #comparing two images
                        b, g, r = cv2.split(difference)
                        if (cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0):
                            cv2.imwrite('GenuineCertificates/Certificate{j}.jpg'.format(j=i), imgOrig)
                            genNo=genNo+1
                        else:
                            cv2.imwrite('FakeCertificates/Certificate{j}.jpg'.format(j=i), imgOrig)
                            fakeNo=fakeNo+1
            lab=Label(root, text="Processed Image : {j}!".format(j=i)).grid(row=5,column=0)                
            os.remove("temp.jpg")
    messagebox.showinfo(title="Completed", message="Completed the Images in the folder. Check the newly created folders! \n Total Images Processed : {j} \n\n Number of Geniune Certificates : {k} \n Number of Fake Certificates : {l} \n Number of UnReadable Images : {m}".format(j=i, k=genNo, l=fakeNo, m=i-(genNo+fakeNo)))

labelMain=Label(root, text="! NPTEL Certificate Verifier by Saieed !").grid(row=0,column=0)
label1=Label(root,text="Choose the images folder!").grid(row=1, column=0)
#imageFolder = Label(root,text="folder location", width = 60).grid(row=1, column=1)
chooseFolderButton = Button(text="Select",padx=2, pady=3, command=selectFolder).grid(row=1, column=2)
labelempty=Label(root, text=" ").grid(row=2,column=0)
chooseFolderButton = Button(text="Start Verification",bd=5, command=verify).grid(row=3, column=0)
labelempty=Label(root, text=" Please wait after clicking Start Verification Button   ").grid(row=9,column=0)
labelempty=Label(root, text="till a complete message is shown.  ").grid(row=10,column=0)
labelempty=Label(root, text=" Please don't close the program ! ").grid(row=11,column=0)
root.mainloop()