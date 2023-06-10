import math
import os
import sys
from App.AirSigning.ShowPdf import ShowPdf
from App.Signing import Signing
from PyPDF2 import PdfReader
import subprocess
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
from App.verification.Verification import Verification


class PDFAirSignerApp(object):
    def __init__(self, master, **kwargs):
        self.master = master
        pad = 80
        self._geom = "850x{}+650+0".format(master.winfo_screenheight() - pad)
        master.geometry("{0}x{1}+0+0".format(master.winfo_screenwidth(), master.winfo_screenheight() - pad))
        master.bind('<Escape>', self.toggle_geom)

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
        self.file_label = Label(self.master, text="No File Chosen", bg='#525561', fg='#ffffff')
        self.file_label.pack()

        # Image Canvas  x, y  Coordinates
        self.X = 0
        self.Y = 0

        # creating object of ShowPdf from tkPDFViewer.
        self.v1 = ShowPdf()
        self.v2 = None

        # Create a button to close the PDF file
        self.close_button = Button(self.master, text='Save & Close PDF', command=self.close_pdf, width=20,
                                   font='arial 20', bd=4, cursor="hand2", state=DISABLED)
        self.close_button.pack(side=TOP, anchor='center')

        # Create a button to sign the PDF file
        self.sign_button = Button(self.master, text='Sign PDF', command=self.sign_pdf, width=20, font='arial 20',
                                  bd=4, cursor="hand2", state=DISABLED)
        self.sign_button.pack(side=TOP, anchor='center')

        # Add a button to select an image file
        self.img_button = Button(self.master, text="Select Signature", command=self.load_img,
                                 width=20, cursor="hand2", font='arial 20', bd=4, state=DISABLED)
        self.img_button.pack(side=TOP, anchor='center')

        self.filePath = None
        self.userName = sys.argv[2]

    def load_pdf(self, file_path):

        # If a file was selected, read the PDF file and display it in a Canvas widget
        if file_path:
            self.filePath = file_path
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
            prev_button = Button(self.canvas, text='Previous', width=7, font='arial 10', cursor="hand2",
                                 bd=2, command=lambda: self.v1.goto(self.update_current_page(False)))
            prev_button.pack(side=LEFT)

            # Create a button to Go Previous Page
            next_button = Button(self.canvas, text='Next', width=7, font='arial 10', cursor="hand2",
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
        os.remove(self.filePath)
        print('PDF Closed!')
        exit()

    def load_img(self):
        airSignComponent = Signing.AirSigning()
        img_path = airSignComponent.drawSign(f"verification//application_data//{self.userName}//new_sign")

        if img_path:
            self.verify()
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

        self.image_item.place_configure(x=event.x, y=event.y, anchor=CENTER)

        self.canvas.update()

        # print(event.x, event.y, "canvas", x_canvas, y_canvas, "pdf", x_pdf, y_pdf)

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

    def toggle_geom(self, event):
        geom = self.master.winfo_geometry()
        self.master.geometry(self._geom)
        self._geom = geom

    def verify(self):
        win = Toplevel(self.master, bg='#272A37')
        window_width = 350
        window_height = 350
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()
        position_top = int(screen_height / 4 - window_height / 4)
        position_right = int(screen_width / 2 - window_width / 2)
        win.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
        win.protocol("WM_DELETE_WINDOW", self.disable_event)

        win.title('Verify Signature')
        # win.iconbitmap('images\\aa.ico')

        win.grab_set()

        # sign = PhotoImage(file=f"verification//application_data//{self.userName}//new_sign//tempSign.png")
        # sign_image_label = Label(
        #     win,
        #     image=sign.zoom(15).subsample(25),
        #     bg="#272A37"
        # )
        # sign_image_label.place(x=120, y=50)

        message_label = Label(
            win,
            text="Verifying your Signature",
            fg="#FFFFFF",
            font=("yu gothic ui Bold", 15 * -1),
            bg="#272A37"
        )

        message_verified = Label(
            win,
            text="You are Successfully Verified",
            fg="#FFFFFF",
            font=("yu gothic ui Bold", 15 * -1),
            bg="#272A37"
        )

        message_label.place(x=85, y=120)

        verifying = ttk.Progressbar(win, orient=HORIZONTAL, length=300, mode='determinate')
        verifying.place(x=25, y=160, height=25, width=300)

        verifying.start(10)

        verifier = Verification()

        results, verified = verifier.verify_signature(self.userName)

        print(results)

        verifying.stop()
        verifying['value'] = 100

        win.resizable(False, False)

        if verified:
            message_verified.place(x=85, y=190)
            self.tksleep(2)

            win.grab_release()
            win.destroy()

            return True
        else:
            message_verified.config(text="Not Matched!", fg='red')
            message_verified.place(x=125, y=190)
            self.tksleep(2)

            res = messagebox.askyesno('Mismatched', 'Would You like to Re-Try Again?')
            print(res)

            win.destroy()
            win.grab_release()

            if not res:
                self.close_pdf()
            else:
                self.load_img()

        return False

    def disable_event(self):
        pass

    def tksleep(self, t):
        """emulating time.sleep(seconds)"""
        ms = int(t * 1000)
        var = IntVar(self.master)
        self.master.after(ms, lambda: var.set(1))
        self.master.wait_variable(var)


if __name__ == "__main__":
    root = Tk()
    root.title('PDF Opener')
    root.configure(bg="#525561")

    app = PDFAirSignerApp(root)
    app.load_pdf(sys.argv[1])
    root.mainloop()
