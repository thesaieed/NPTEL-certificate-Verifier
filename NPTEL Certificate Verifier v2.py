
import customtkinter
from tkinter import filedialog
from tkinter import messagebox
import tkinter 
import cv2
from pyzbar.pyzbar import decode
import requests
import urllib
from bs4 import BeautifulSoup as bs
import glob
import os


customtkinter.set_appearance_mode("light")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

root_tk = customtkinter.CTk()  # create CTk window like you do with the Tk window
root_tk.geometry("800x270")
root_tk.resizable(0, 0)
root_tk.title("NPTEL Certificate Verifier by Saieed")
root_tk.wm_iconbitmap('icon.ico')


aburl="https://archive.nptel.ac.in/noc/Ecertificate/?q="
fake="FakeCertificates"
gen="GenuineCertificates"
unp="UnProcessed"
folder_selected=""
gif='Loading.gif'

    
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
        global verifying
        verifying.configure(text="Verifying Image : {j}".format(j=i))
        root_tk.update()
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
            os.remove("temp.jpg")
    messagebox.showinfo(title="Completed", message="Completed the Images in the folder. Check the newly created folders! \n Total Images Processed : {j} \n\n Number of Geniune Certificates : {k} \n Number of Fake Certificates : {l} \n Number of UnReadable Images : {m}".format(j=i, k=genNo, l=fakeNo, m=i-(genNo+fakeNo)))


def selectFolder():
    global folder_selected
    folder_selected = filedialog.askdirectory()
    global imageFolder
    imageFolder.configure(text=folder_selected)
    
    
def createdir(dirName):
    try:
        # Create target Directory
        os.mkdir(dirName)
         
    except FileExistsError:
        print()        
    
    # Create target Directory if don't exist
    if not os.path.exists(dirName):
        os.mkdir(dirName)


aburl="https://archive.nptel.ac.in/noc/Ecertificate/?q="
fake="FakeCertificates"
gen="GenuineCertificates"
unp="UnProcessed"


labelHeading = customtkinter.CTkLabel(master=root_tk, text="NPTEL Certificate Verifier by Saieed")
labelHeading.pack()

frame = customtkinter.CTkFrame(master=root_tk,
                               width=750,
                               height=50,
                               corner_radius=10)
frame.pack(padx=20, pady=20)

labelfolder = customtkinter.CTkLabel(master=frame, text="Images Folder : ")
labelfolder.place(relx=0.2, rely=0.5, anchor='e')

imageFolder = customtkinter.CTkLabel(master=frame, text="/folder_location")
imageFolder.place(relx=0.5, rely=0.5, anchor='center')

button = customtkinter.CTkButton(master=frame, text="Select", command=selectFolder)
button.place(relx=0.9, rely=0.5, anchor=tkinter.CENTER)


button = customtkinter.CTkButton(master=root_tk, text="Start Verification", command=verify)
button.place(relx=0.1, rely=0.5)

verifying = customtkinter.CTkLabel(root_tk, text="")
verifying.pack()


root_tk.mainloop()