import math
import os
from tkinter import filedialog

from App.AirSigning.ShowPdf import ShowPdf
from App.Signing import Signing
from PyPDF2 import PdfReader
import subprocess
import shutil
import tempfile
from tkinter import *
from PIL import Image, ImageTk

class PDFAirSignerApp(Canvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Create the root window
        self.master = master

        self.canvas = None

        # get currently opened fileName
        self.fileName = ''
        self.imageName = ''
        self.current_page = 0
        self.numberPages = 0

        # signature image
        self.photo = None
        self.image_item = None
        self.page_dim = None
        self.img_dim = None

        # create a label to display the name of the loaded PDF file
        self.file_label = Label(self.master, text="No File Chosen")
        self.file_label.pack()

        # Image Canvas  x, y  Coordinates
        self.X = 0
        self.Y = 0

        # creating object of ShowPdf from tkPDFViewer.
        self.v1 = ShowPdf()
        self.v2 = None

        # Create a button to open a PDF file
        self.open_button = Button(self.master, text='Open PDF', command=self.load_pdf, width=20, font='arial 20',
                                  bd=4)
        self.open_button.pack(side=TOP, anchor='center')

        # Create a button to close the PDF file
        self.close_button = Button(self.master, text='Close PDF', command=self.close_pdf, width=20, font='arial 20',
                                   bd=4, state=DISABLED)
        self.close_button.pack(side=TOP, anchor='center')

        # Create a button to sign the PDF file
        self.sign_button = Button(self.master, text='Sign PDF', command=self.sign_pdf, width=20, font='arial 20',
                                  bd=4, state=DISABLED)
        self.sign_button.pack(side=TOP, anchor='center')

        # Add a button to select an image file
        self.img_button = Button(self.master, text="Draw Signature", command=self.load_img, width=20,
                                 font='arial 20', bd=4, state=DISABLED)
        self.img_button.pack(side=TOP, anchor='center')

        # Temporary directory
        self.tempDir = None
        self.currentTempPath = None

    def load_pdf(self):
        # Open a file dialog to select a PDF file
        file_path = filedialog.askopenfilename(filetypes=[('PDF Files', '*.pdf')], initialdir=os.getcwd(),
                                               title='Select pdf File')

        # If a file was selected, read the PDF file and display it in a Canvas widget
        if file_path:
            # create a temporary directory in the current project directory
            temp_dir = tempfile.TemporaryDirectory(dir=os.getcwd() + "\\AirSigning\\temp")
            newFilePath = temp_dir.name + "\\" + file_path.split("/")[-1]
            shutil.copy(file_path, newFilePath)

            # Wait until the file has been completely copied
            while True:
                try:
                    shutil.copystat(file_path, newFilePath)
                    break
                except OSError:
                    pass
            file_path = newFilePath
            # Load PDF page and get its dimensions
            doc = PdfReader(file_path)
            page = doc.getPage(0)
            self.numberPages = len(doc.pages)
            self.page_dim = page.cropBox

            # Create PDF Canvas
            self.canvas = Canvas(master=self.master, relief=SUNKEN, borderwidth=1, bg='grey',
                                 width=math.ceil(self.page_dim.width), height=math.ceil(self.page_dim.height))

            self.canvas.pack(fill='none', expand=True, pady=10, padx=10, side=BOTTOM)

            # Create a button to Go Next Page
            prev_button = Button(self.canvas, text='Previous', width=7, font='arial 10',
                                 bd=2, command=lambda: self.v1.goto(self.update_current_page(False)))
            prev_button.pack(side=LEFT)

            # Create a button to Go Previous Page
            next_button = Button(self.canvas, text='Next', width=7, font='arial 10',
                                 bd=2, command=lambda: self.v1.goto(self.update_current_page(True)))
            next_button.pack(side=RIGHT)

            self.v2 = self.v1.pdf_view(master=self.canvas, pdf_location=open(file_path), width=77,
                                       height=math.ceil(self.page_dim.height))
            self.v1.text.bindtags([f"pdf_page_{i}" for i in range(self.numberPages)])
            self.v2.pack(pady=10, padx=10)

            # update the label to display the name of the loaded PDF file
            self.fileName = file_path  # extract the fileName from the file path
            self.file_label.config(text=f"Loaded PDF file: {self.fileName}")
            self.img_button.config(state=ACTIVE if len(self.fileName) > 0 else DISABLED)
            self.close_button.config(state=ACTIVE if len(self.fileName) > 0 else DISABLED)
            self.tempDir = temp_dir
            print('PDF Opened.')

        else:
            print('No File Chosen')

    def update_current_page(self, isNext):
        if self.current_page == self.numberPages - 1 or self.current_page < 0:
            self.current_page = 0
        else:
            if isNext:
                self.current_page += 1
            else:
                self.current_page -= 1

        return self.current_page

    def close_pdf(self):
        self.v1.frame.destroy()
        self.v1.img_object_li.clear()
        self.canvas.destroy()
        self.file_label.config(text='No File Chosen')
        self.sign_button.config(state=DISABLED)
        self.img_button.config(state=DISABLED)
        self.close_button.config(state=DISABLED)
        self.tempDir.cleanup()
        print('PDF Closed!')

    def load_img(self):
        # img_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        airSignComponent = Signing.AirSigning()
        img_path = airSignComponent.drawSign(self.tempDir.name)

        if img_path:
            # Open the image file and display it on the PDF canvas
            image = Image.open(img_path).convert('RGBA')
            image.thumbnail((150, 40), Image.ANTIALIAS)
            self.photo = ImageTk.PhotoImage(image)
            self.image_item = Label(master=self.v2, image=self.photo, takefocus=True, bd=0)
            self.image_item.pack(side=LEFT)
            self.image_item.place(relx=0, rely=0)

            self.imageName = img_path
            self.img_dim = (image.width, image.height)
            self.sign_button.config(state=ACTIVE if len(self.fileName) & len(self.imageName) > 0 else DISABLED)

            self.image_item.bind("<B1-Motion>", self.on_move)

    def on_move(self, event):
        self.X, self.Y = event.x, event.y

        x_canvas, y_canvas = self.canvas.winfo_x(), self.canvas.winfo_y()
        x_pdf, y_pdf = self.v2.winfo_x(), self.v2.winfo_y()

        # self.v1.find(event.x - x_pdf, event.y - y_pdf)
        self.image_item.place_configure(x=event.x, y=event.y, anchor=CENTER)

        # self.canvas.coords(self.image_item, self.X, self.Y)
        self.canvas.update()

        #print(event.x, event.y, "canvas", x_canvas, y_canvas, "pdf", x_pdf, y_pdf)

    def sign_pdf(self):
        # List of Python scripts to run
        scripts = ["python", "signPdfProcess/signpdf.py", self.fileName, self.imageName, "--coords",
                   "{}x{}x{}x{}x{}".format(self.current_page + 1, (self.X - (self.img_dim[0] // 2)),
                                           (math.ceil(self.page_dim.height) - (self.Y + self.img_dim[1] // 2) + 10),
                                           self.photo.width(), self.photo.height())]

        try:
            # Run the python cmd script
            try:
                subprocess.run(scripts, shell=True)

                # Reset view:
                self.v1.frame.destroy()
                self.v1.img_object_li.clear()

                # Display Signed pdf
                snd_pdf = self.v1.pdf_view(master=self.canvas,
                                           pdf_location=open("{}_signed{}".format(*os.path.splitext(self.fileName))),
                                           width=77, height=math.ceil(self.page_dim.height))
                snd_pdf.pack(pady=10, padx=10)

            except subprocess.CalledProcessError as e:
                print(f"An error occurred while running: {e}")
                exit(1)
        except KeyboardInterrupt:
            print("Script execution interrupted by user.")

