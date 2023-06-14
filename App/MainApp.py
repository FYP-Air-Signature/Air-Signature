import subprocess
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from App.verification.Authentication import AuthAPI
from App.verification.PdfAPI import PdfAPI

authentication = None
pdfApi = PdfAPI()
AUTHENTICATE = False

signature = Tk()
signature.rowconfigure(0, weight=1)
signature.columnconfigure(0, weight=1)
height = 650
width = 1240
x = (signature.winfo_screenwidth() // 2) - (width // 2)
y = (signature.winfo_screenheight() // 4) - (height // 4)

signature.geometry('{}x{}+{}+{}'.format(width, height, x, y))

signature.title('Air Signature')

sign_in = Frame(signature)
sign_up = Frame(signature)
index_page = Frame(signature)
load_pdf = Frame(signature)
update_page = Frame(signature)

for frame in (index_page, sign_in, sign_up, load_pdf, update_page):
    frame.grid(row=0, column=0, sticky='nsew')


def show_frame(ui):
    ui.tkraise()


def show_password(entry):
    if entry.cget('show') == '*':
        entry.config(show='')
    else:
        entry.config(show='*')


show_frame(index_page)

# ====================================================================================
# =========================== INDEX PAGE START HERE ==================================
# ====================================================================================
index_page.configure(bg="#525561")

# ================Background Image ====================
index_page_bg_image = PhotoImage(file="assets\\image_1.png")
index_bg_image = Label(
    index_page,
    image=index_page_bg_image,
    bg="#525561"
)
index_bg_image.place(x=120, y=25)

# ================ Header Text Left ====================
index_headerText_image_left = PhotoImage(file="assets\\headerText_image.png")
index_headerText_image_label1 = Label(
    index_bg_image,
    image=index_headerText_image_left,
    bg="#272A37"
)
index_headerText_image_label1.place(x=60, y=45)

index_headerText1 = Label(
    index_bg_image,
    text="Air Signature",
    fg="#FFFFFF",
    font=("yu gothic ui bold", 20 * -1),
    bg="#272A37"
)
index_headerText1.place(x=110, y=45)

# ================ Header Text Down ====================
index_headerText_image_down = PhotoImage(file="assets\\headerText_image.png")
index_headerText_image_label3 = Label(
    index_bg_image,
    image=index_headerText_image_down,
    bg="#272A37"
)
index_headerText_image_label3.place(x=650, y=530)

index_headerText3 = Label(
    index_bg_image,
    text="Powered by Signature Group",
    fg="#FFFFFF",
    font=("yu gothic ui bold", 20 * -1),
    bg="#272A37"
)
index_headerText3.place(x=700, y=530)

# ============== Right Button ========================
signButton = Button(
    index_bg_image,
    text="Sign with \n Verification",
    fg="#206DB4",
    font=("yu gothic ui Bold", 40 * -1),
    bg="#272A60",
    bd=5,
    cursor="hand2",
    activebackground="#272A37",
    activeforeground="#ffffff",
    command=lambda: clickVerification(),
)
signButton.place(x=590, y=140, width=350, height=350)

# ================ Left Button ====================
signButton = Button(
    index_bg_image,
    text="Sign without \nVerification",
    fg="#206DB4",
    font=("yu gothic ui Bold", 40 * -1),
    bg="#272A60",
    bd=5,
    cursor="hand2",
    activebackground="#272A37",
    activeforeground="#ffffff",
    command=lambda: sign_without_verify()
)
signButton.place(x=75, y=140, width=350, height=350)

# ====================================================================================
# =========================== SIGN UP PAGE START HERE ================================
# ====================================================================================

# Sign Up Text Variables
FirstName = StringVar()
LastName = StringVar()
Email = StringVar()
Password = StringVar()
ConfirmPassword = StringVar()

sign_up.configure(bg="#525561")

# ================Background Image ====================
backgroundImage = PhotoImage(file="assets\\image_1.png")
bg_image = Label(
    sign_up,
    image=backgroundImage,
    bg="#525561"
)
bg_image.place(x=120, y=28)

# ================ Header Text Left ====================
headerText_image_left = PhotoImage(file="assets\\headerText_image.png")
headerText_image_label1 = Label(
    bg_image,
    image=headerText_image_left,
    bg="#272A37"
)
headerText_image_label1.place(x=60, y=45)

headerText1 = Label(
    bg_image,
    text="Air Signature",
    fg="#FFFFFF",
    font=("yu gothic ui bold", 20 * -1),
    bg="#272A37"
)
headerText1.place(x=110, y=45)

# ================ Header Text Right ====================
headerText_image_right = PhotoImage(file="assets\\headerText_image.png")
headerText_image_label2 = Label(
    bg_image,
    image=headerText_image_right,
    bg="#272A37"
)
headerText_image_label2.place(x=640, y=45)

headerText2 = Label(
    bg_image,
    anchor="nw",
    text="Signatures",
    fg="#FFFFFF",
    font=("yu gothic ui Bold", 20 * -1),
    bg="#272A37"
)
headerText2.place(x=690, y=45)

# ============== SHOW ALL SIGNATURES ========================
sign_image_right = Image.open("assets\\button_1.png")
sign_image_right = sign_image_right.resize((320, 80))
sign_image_right = ImageTk.PhotoImage(sign_image_right)
for i in range(5):
    sign_image_label = Label(
        bg_image,
        image=sign_image_right,
        bg="red"
    )
    sign_image_label.place(x=640, y=(85 + i * 90), width=320, height=80)

# ================ CREATE ACCOUNT HEADER ====================
createAccount_header = Label(
    bg_image,
    text="Create new account",
    fg="#FFFFFF",
    font=("yu gothic ui Bold", 28 * -1),
    bg="#272A37"
)
createAccount_header.place(x=75, y=121)

# ================ ALREADY HAVE AN ACCOUNT TEXT ====================
text = Label(
    bg_image,
    text="Already a member?",
    fg="#FFFFFF",
    font=("yu gothic ui Regular", 15 * -1),
    bg="#272A37"
)
text.place(x=75, y=187)

# ================ GO TO LOGIN ====================
switchLogin = Button(
    bg_image,
    text="Login",
    fg="#206DB4",
    font=("yu gothic ui Bold", 15 * -1),
    bg="#272A37",
    bd=0,
    cursor="hand2",
    activebackground="#272A37",
    activeforeground="#ffffff",
    command=lambda: show_frame(sign_in)
)
switchLogin.place(x=230, y=185, width=50, height=35)

# ================ First Name Section ====================
firstName_image = PhotoImage(file="assets\\input_img.png")
firstName_image_Label = Label(
    bg_image,
    image=firstName_image,
    bg="#272A37"
)
firstName_image_Label.place(x=80, y=242)

firstName_text = Label(
    firstName_image_Label,
    text="First name",
    fg="#FFFFFF",
    font=("yu gothic ui SemiBold", 13 * -1),
    bg="#3D404B"
)
firstName_text.place(x=25, y=0)

firstName_icon = PhotoImage(file="assets\\name_icon.png")
firstName_icon_Label = Label(
    firstName_image_Label,
    image=firstName_icon,
    bg="#3D404B"
)
firstName_icon_Label.place(x=159, y=15)

firstName_entry = Entry(
    firstName_image_Label,
    bd=0,
    bg="#3D404B",
    highlightthickness=0,
    font=("yu gothic ui SemiBold", 16 * -1),
    textvariable=FirstName
)
firstName_entry.place(x=8, y=17, width=140, height=27)

# ================ Last Name Section ====================
lastName_image = PhotoImage(file="assets\\input_img.png")
lastName_image_Label = Label(
    bg_image,
    image=lastName_image,
    bg="#272A37"
)
lastName_image_Label.place(x=293, y=242)

lastName_text = Label(
    lastName_image_Label,
    text="Last name",
    fg="#FFFFFF",
    font=("yu gothic ui SemiBold", 13 * -1),
    bg="#3D404B"
)
lastName_text.place(x=25, y=0)

lastName_icon = PhotoImage(file="assets\\name_icon.png")
lastName_icon_Label = Label(
    lastName_image_Label,
    image=lastName_icon,
    bg="#3D404B"
)
lastName_icon_Label.place(x=159, y=15)

lastName_entry = Entry(
    lastName_image_Label,
    bd=0,
    bg="#3D404B",
    highlightthickness=0,
    font=("yu gothic ui SemiBold", 16 * -1),
    textvariable=LastName
)
lastName_entry.place(x=8, y=17, width=140, height=27)

# ================ Email Name Section ====================
emailName_image = PhotoImage(file="assets\\email.png")
emailName_image_Label = Label(
    bg_image,
    image=emailName_image,
    bg="#272A37"
)
emailName_image_Label.place(x=80, y=311)

emailName_text = Label(
    emailName_image_Label,
    text="Email account",
    fg="#FFFFFF",
    font=("yu gothic ui SemiBold", 13 * -1),
    bg="#3D404B"
)
emailName_text.place(x=25, y=0)

emailName_icon = PhotoImage(file="assets\\email-icon.png")
emailName_icon_Label = Label(
    emailName_image_Label,
    image=emailName_icon,
    bg="#3D404B"
)
emailName_icon_Label.place(x=370, y=15)

emailName_entry = Entry(
    emailName_image_Label,
    bd=0,
    bg="#3D404B",
    highlightthickness=0,
    font=("yu gothic ui SemiBold", 16 * -1),
    textvariable=Email
)
emailName_entry.place(x=8, y=17, width=354, height=27)

# ================ Password Name Section ====================
passwordName_image = PhotoImage(file="assets\\input_img.png")
passwordName_image_Label = Label(
    bg_image,
    image=passwordName_image,
    bg="#272A37"
)
passwordName_image_Label.place(x=80, y=380)

passwordName_text = Label(
    passwordName_image_Label,
    text="Password",
    fg="#FFFFFF",
    font=("yu gothic ui SemiBold", 13 * -1),
    bg="#3D404B"
)
passwordName_text.place(x=25, y=0)

passwordName_icon = PhotoImage(file="assets\\pass-icon.png")
passwordName_icon_Label = Label(
    passwordName_image_Label,
    image=passwordName_icon,
    bg="#3D404B"
)
passwordName_icon_Label.place(x=159, y=15)

passwordName_entry = Entry(
    passwordName_image_Label,
    bd=0,
    bg="#3D404B",
    highlightthickness=0,
    font=("yu gothic ui SemiBold", 16 * -1),
    show="*",
    textvariable=Password
)
passwordName_entry.place(x=8, y=17, width=140, height=27)

password_check_btn = Checkbutton(bg_image, text='show password', fg="#FFFFFF", bg='#272A37', selectcolor='#272A37',
                                 activebackground='#272A37',
                                 bd=0,
                                 font=("yu gothic ui", 11, 'bold'), command=lambda: show_password(passwordName_entry))
password_check_btn.place(x=120, y=440)

# ================ Confirm Password Name Section ====================
confirm_passwordName_image = PhotoImage(file="assets\\input_img.png")
confirm_passwordName_image_Label = Label(
    bg_image,
    image=confirm_passwordName_image,
    bg="#272A37"
)
confirm_passwordName_image_Label.place(x=293, y=380)

confirm_passwordName_text = Label(
    confirm_passwordName_image_Label,
    text="Confirm Password",
    fg="#FFFFFF",
    font=("yu gothic ui SemiBold", 13 * -1),
    bg="#3D404B"
)
confirm_passwordName_text.place(x=25, y=0)

confirm_passwordName_icon = PhotoImage(file="assets\\pass-icon.png")
confirm_passwordName_icon_Label = Label(
    confirm_passwordName_image_Label,
    image=confirm_passwordName_icon,
    bg="#3D404B"
)
confirm_passwordName_icon_Label.place(x=159, y=15)

confirm_passwordName_entry = Entry(
    confirm_passwordName_image_Label,
    bd=0,
    bg="#3D404B",
    highlightthickness=0,
    font=("yu gothic ui SemiBold", 16 * -1),
    show="*",
    textvariable=ConfirmPassword
)
confirm_passwordName_entry.place(x=8, y=17, width=140, height=27)

confirm_check_btn = Checkbutton(bg_image, text='show password', fg="#FFFFFF", bg='#272A37', selectcolor='#272A37',
                                activebackground='#272A37',
                                bd=0,
                                font=("yu gothic ui", 11, 'bold'),
                                command=lambda: show_password(confirm_passwordName_entry))
confirm_check_btn.place(x=330, y=440)

# =============== Add Sign Button ====================
add_sign_buttonImage = PhotoImage(file="assets\\email.png")
add_sign_button = Button(
    bg_image,
    text="Add Signatures",
    fg="#206DB4",
    font=("yu gothic ui Bold", 25 * -1),
    bg="#2c3042",
    bd=0,
    cursor="hand2",
    activebackground="#272A37",
    activeforeground="#ffffff",
    command=lambda: add_signature()
)

add_sign_button.place(x=144, y=480, width=300, height=45)

# =============== Submit Button ====================
submit_buttonImage = PhotoImage(
    file="assets\\button_1.png")
submit_button = Button(
    bg_image,
    image=submit_buttonImage,
    borderwidth=0,
    highlightthickness=0,
    relief="flat",
    activebackground="#272A37",
    cursor="hand2",
    command=lambda: signup()
)
submit_button.place(x=130, y=530, width=333, height=65)

# ================ Header Text Down ====================
headerText_image_down = PhotoImage(file="assets\\headerText_image.png")
headerText_image_label3 = Label(
    bg_image,
    image=headerText_image_down,
    bg="#272A37"
)
headerText_image_label3.place(x=650, y=530)

headerText3 = Label(
    bg_image,
    text="Powered by Signature Group",
    fg="#FFFFFF",
    font=("yu gothic ui bold", 20 * -1),
    bg="#272A37"
)
headerText3.place(x=700, y=530)


def add_signature():
    win = Toplevel()
    window_width = 350
    window_height = 350
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    position_top = int(screen_height / 4 - window_height / 4)
    position_right = int(screen_width / 2 - window_width / 2)
    win.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

    win.title('Draw Signatures')
    # win.iconbitmap('images\\aa.ico')
    win.configure(background='#272A37')
    win.resizable(False, False)


def clear_signup():
    FirstName.set("")
    LastName.set("")
    Email.set("")
    Password.set("")
    ConfirmPassword.set("")

    password_check_btn.deselect()
    confirm_check_btn.deselect()


def signup():
    user = dict()

    if firstName_entry.get() == "" or lastName_entry.get() == "" or emailName_entry.get() == "" or passwordName_entry.get() == "" or confirm_passwordName_entry.get() == "":
        messagebox.showerror("Error", "All Fields are Required")
    elif passwordName_entry.get() != confirm_passwordName_entry.get():
        messagebox.showerror("Error", "Password and Confirmed Password Didn't Match")
    else:
        user['firstName'] = firstName_entry.get()
        user['lastName'] = lastName_entry.get()
        user['email'] = emailName_entry.get()
        user['password'] = passwordName_entry.get()

        clear_signup()
        show_frame(sign_in)


# ====================================================================================
# =========================== UPDATE PAGE START HERE =================================
# ====================================================================================

# Sign Up Text Variables
Update_FirstName = StringVar()
Update_LastName = StringVar()
Update_Password = StringVar()
Update_ConfirmPassword = StringVar()

update_page.configure(bg="#525561")

# ================Background Image ====================
update_backgroundImage = PhotoImage(file="assets\\image_1.png")
update_bg_image = Label(
    update_page,
    image=update_backgroundImage,
    bg="#525561"
)
update_bg_image.place(x=120, y=28)

# ================ Header Text Left ====================
update_headerText_image_left = PhotoImage(file="assets\\headerText_image.png")
update_headerText_image_label1 = Label(
    update_bg_image,
    image=update_headerText_image_left,
    bg="#272A37"
)
update_headerText_image_label1.place(x=60, y=45)

update_headerText1 = Label(
    update_bg_image,
    text="Air Signature",
    fg="#FFFFFF",
    font=("yu gothic ui bold", 20 * -1),
    bg="#272A37"
)
update_headerText1.place(x=110, y=45)

# ================ Header Text Right ====================
update_headerText_image_right = PhotoImage(file="assets\\headerText_image.png")
update_headerText_image_label2 = Label(
    update_bg_image,
    image=update_headerText_image_right,
    bg="#272A37"
)
update_headerText_image_label2.place(x=640, y=45)

update_headerText2 = Label(
    update_bg_image,
    anchor="nw",
    text="Signatures",
    fg="#FFFFFF",
    font=("yu gothic ui Bold", 20 * -1),
    bg="#272A37"
)
update_headerText2.place(x=690, y=45)

# ============== SHOW ALL SIGNATURES ========================
update_sign_image_right = PhotoImage(file="assets\\button_1.png").zoom(20).subsample(30)
for i in range(5):
    update_sign_image_label = Label(
        update_bg_image,
        image=update_sign_image_right,
        bg="red"
    )
    update_sign_image_label.place(x=640, y=(121 + i * 70))

# ================ UPDATE USER HEADER ====================
update_user_header = Label(
    update_bg_image,
    text="Update User",
    fg="#FFFFFF",
    font=("yu gothic ui Bold", 28 * -1),
    bg="#272A37"
)
update_user_header.place(x=75, y=121)

# ================ NOT NOW TEXT ====================
update_text = Label(
    update_bg_image,
    text="Not Now?",
    fg="#FFFFFF",
    font=("yu gothic ui Regular", 15 * -1),
    bg="#272A37"
)
update_text.place(x=80, y=187)

# ================ GO TO LOGIN ====================
update_back = Button(
    update_bg_image,
    text="Go Back",
    fg="#206DB4",
    font=("yu gothic ui Bold", 15 * -1),
    bg="#272A37",
    bd=0,
    cursor="hand2",
    activebackground="#272A37",
    activeforeground="#ffffff",
    command=lambda: show_frame(load_pdf)
)
update_back.place(x=230, y=185, width=60, height=35)

# ================ First Name Section ====================
update_firstName_image = PhotoImage(file="assets\\input_img.png")
update_firstName_image_Label = Label(
    update_bg_image,
    image=update_firstName_image,
    bg="#272A37"
)
update_firstName_image_Label.place(x=80, y=242)

update_firstName_text = Label(
    update_firstName_image_Label,
    text="First name",
    fg="#FFFFFF",
    font=("yu gothic ui SemiBold", 13 * -1),
    bg="#3D404B"
)
update_firstName_text.place(x=25, y=0)

update_firstName_icon = PhotoImage(file="assets\\name_icon.png")
update_firstName_icon_Label = Label(
    update_firstName_image_Label,
    image=update_firstName_icon,
    bg="#3D404B"
)
update_firstName_icon_Label.place(x=159, y=15)

update_firstName_entry = Entry(
    update_firstName_image_Label,
    bd=0,
    bg="#3D404B",
    highlightthickness=0,
    font=("yu gothic ui SemiBold", 16 * -1),
    textvariable=Update_FirstName
)
update_firstName_entry.place(x=8, y=17, width=140, height=27)

# ================ Last Name Section ====================
update_lastName_image = PhotoImage(file="assets\\input_img.png")
update_lastName_image_Label = Label(
    update_bg_image,
    image=update_lastName_image,
    bg="#272A37"
)
update_lastName_image_Label.place(x=293, y=242)

update_lastName_text = Label(
    update_lastName_image_Label,
    text="Last name",
    fg="#FFFFFF",
    font=("yu gothic ui SemiBold", 13 * -1),
    bg="#3D404B"
)
update_lastName_text.place(x=25, y=0)

update_lastName_icon = PhotoImage(file="assets\\name_icon.png")
update_lastName_icon_Label = Label(
    update_lastName_image_Label,
    image=update_lastName_icon,
    bg="#3D404B"
)
update_lastName_icon_Label.place(x=159, y=15)

update_lastName_entry = Entry(
    update_lastName_image_Label,
    bd=0,
    bg="#3D404B",
    highlightthickness=0,
    font=("yu gothic ui SemiBold", 16 * -1),
    textvariable=Update_LastName
)
update_lastName_entry.place(x=8, y=17, width=140, height=27)

# ================ Password Name Section ====================
update_passwordName_image = PhotoImage(file="assets\\input_img.png")
update_passwordName_image_Label = Label(
    update_bg_image,
    image=update_passwordName_image,
    bg="#272A37"
)
update_passwordName_image_Label.place(x=80, y=311)

update_passwordName_text = Label(
    update_passwordName_image_Label,
    text="Password",
    fg="#FFFFFF",
    font=("yu gothic ui SemiBold", 13 * -1),
    bg="#3D404B"
)
update_passwordName_text.place(x=25, y=0)

update_passwordName_icon = PhotoImage(file="assets\\pass-icon.png")
update_passwordName_icon_Label = Label(
    update_passwordName_image_Label,
    image=update_passwordName_icon,
    bg="#3D404B"
)
update_passwordName_icon_Label.place(x=159, y=15)

update_passwordName_entry = Entry(
    update_passwordName_image_Label,
    bd=0,
    bg="#3D404B",
    highlightthickness=0,
    font=("yu gothic ui SemiBold", 16 * -1),
    show="*",
    textvariable=Update_Password
)
update_passwordName_entry.place(x=8, y=17, width=140, height=27)

update_password_check_btn = Checkbutton(update_bg_image, text='show password', fg="#FFFFFF", bg='#272A37',
                                        selectcolor='#272A37', activebackground='#272A37', bd=0,
                                        font=("yu gothic ui", 11, 'bold'),
                                        command=lambda: show_password(update_passwordName_entry))
update_password_check_btn.place(x=120, y=370)

# ================ Confirm Password Name Section ====================
update_confirm_passwordName_image = PhotoImage(file="assets\\input_img.png")
update_confirm_passwordName_image_Label = Label(
    update_bg_image,
    image=update_confirm_passwordName_image,
    bg="#272A37"
)
update_confirm_passwordName_image_Label.place(x=293, y=311)

update_confirm_passwordName_text = Label(
    update_confirm_passwordName_image_Label,
    text="Confirm Password",
    fg="#FFFFFF",
    font=("yu gothic ui SemiBold", 13 * -1),
    bg="#3D404B"
)
update_confirm_passwordName_text.place(x=25, y=0)

update_confirm_passwordName_icon = PhotoImage(file="assets\\pass-icon.png")
update_confirm_passwordName_icon_Label = Label(
    update_confirm_passwordName_image_Label,
    image=update_confirm_passwordName_icon,
    bg="#3D404B"
)
update_confirm_passwordName_icon_Label.place(x=159, y=15)

update_confirm_passwordName_entry = Entry(
    update_confirm_passwordName_image_Label,
    bd=0,
    bg="#3D404B",
    highlightthickness=0,
    font=("yu gothic ui SemiBold", 16 * -1),
    show="*",
    textvariable=Update_ConfirmPassword
)
update_confirm_passwordName_entry.place(x=8, y=17, width=140, height=27)

update_confirm_check_btn = Checkbutton(update_bg_image, text='show password', fg="#FFFFFF", bg='#272A37',
                                       selectcolor='#272A37', activebackground='#272A37', bd=0,
                                       font=("yu gothic ui", 11, 'bold'),
                                       command=lambda: show_password(update_confirm_passwordName_entry))
update_confirm_check_btn.place(x=330, y=370)

# =============== Add Sign Button ====================
update_add_sign_button = Button(
    update_bg_image,
    text="Add Signatures",
    fg="#206DB4",
    font=("yu gothic ui Bold", 25 * -1),
    bg="#2c3042",
    bd=0,
    cursor="hand2",
    activebackground="#272A37",
    activeforeground="#ffffff",
    command=lambda: add_signature()
)

update_add_sign_button.place(x=144, y=405, width=300, height=45)

# =============== Submit Button ====================
update_submit_buttonImage = PhotoImage(
    file="assets\\button_1.png")
update_submit_button = Button(
    update_bg_image,
    image=update_submit_buttonImage,
    borderwidth=0,
    highlightthickness=0,
    relief="flat",
    activebackground="#272A37",
    cursor="hand2",
    command=lambda: update()
)
update_submit_button.place(x=130, y=460, width=333, height=65)

# ================ Header Text Down ====================
update_headerText_image_down = PhotoImage(file="assets\\headerText_image.png")
update_headerText_image_label3 = Label(
    update_bg_image,
    image=update_headerText_image_down,
    bg="#272A37"
)
update_headerText_image_label3.place(x=650, y=530)

update_headerText3 = Label(
    update_bg_image,
    text="Powered by Signature Group",
    fg="#FFFFFF",
    font=("yu gothic ui bold", 20 * -1),
    bg="#272A37"
)
update_headerText3.place(x=700, y=530)


def add_signature():
    win = Toplevel()
    window_width = 350
    window_height = 350
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    position_top = int(screen_height / 4 - window_height / 4)
    position_right = int(screen_width / 2 - window_width / 2)
    win.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

    win.title('Draw Signatures')
    # win.iconbitmap('images\\aa.ico')
    win.configure(background='#272A37')
    win.resizable(False, False)


def clear_update():
    Update_FirstName.set("")
    Update_LastName.set("")
    Update_Password.set("")
    Update_ConfirmPassword.set("")

    update_password_check_btn.deselect()
    update_confirm_check_btn.deselect()


def update():
    user = dict()

    if update_firstName_entry.get() == "" or update_lastName_entry.get() == "" or update_passwordName_entry.get() == "" or update_confirm_passwordName_entry.get() == "":
        messagebox.showerror("Error", "All Fields are Required")
    elif update_passwordName_entry.get() != update_confirm_passwordName_entry.get():
        messagebox.showerror("Error", "Password and Confirmed Password Didn't Match")
    else:
        user['firstName'] = update_firstName_entry.get()
        user['lastName'] = update_lastName_entry.get()
        user['password'] = update_passwordName_entry.get()

        clear_update()
        logout_event()
        show_frame(sign_in)

    print(user.values())


# ====================================================================================
# =========================== LOGIN PAGE START HERE ==================================
# ====================================================================================

# Login Text Variables
email = StringVar()
password = StringVar()

sign_in.configure(bg="#525561")

# ================Background Image ====================
Login_backgroundImage = PhotoImage(file="assets\\image_1.png")
bg_imageLogin = Label(
    sign_in,
    image=Login_backgroundImage,
    bg="#525561"
)
bg_imageLogin.place(x=120, y=28)

# ================ Header Text Left ====================
Login_headerText_image_left = PhotoImage(file="assets\\headerText_image.png")
Login_headerText_image_label1 = Label(
    bg_imageLogin,
    image=Login_headerText_image_left,
    bg="#272A37"
)
Login_headerText_image_label1.place(x=60, y=45)

Login_headerText1 = Label(
    bg_imageLogin,
    text="Air Signature",
    fg="#FFFFFF",
    font=("yu gothic ui bold", 20 * -1),
    bg="#272A37"
)
Login_headerText1.place(x=110, y=45)

# ================ LOGIN TO ACCOUNT HEADER ====================
loginAccount_header = Label(
    bg_imageLogin,
    text="Login to continue",
    fg="#FFFFFF",
    font=("yu gothic ui Bold", 28 * -1),
    bg="#272A37"
)
loginAccount_header.place(x=75, y=121)

# ================ NOT A MEMBER TEXT ====================
loginText = Label(
    bg_imageLogin,
    text="Not a member?",
    fg="#FFFFFF",
    font=("yu gothic ui Regular", 15 * -1),
    bg="#272A37"
)
loginText.place(x=75, y=187)

# ================ GO TO SIGN UP ====================
switchSignup = Button(
    bg_imageLogin,
    text="Sign Up",
    fg="#206DB4",
    font=("yu gothic ui Bold", 15 * -1),
    bg="#272A37",
    bd=0,
    cursor="hand2",
    activebackground="#272A37",
    activeforeground="#ffffff",
    command=lambda: show_frame(sign_up)
)
switchSignup.place(x=220, y=185, width=70, height=35)

# ================ Email Name Section ====================
Login_emailName_image = PhotoImage(file="assets\\email.png")
Login_emailName_image_Label = Label(
    bg_imageLogin,
    image=Login_emailName_image,
    bg="#272A37"
)
Login_emailName_image_Label.place(x=76, y=242)

Login_emailName_text = Label(
    Login_emailName_image_Label,
    text="Email account",
    fg="#FFFFFF",
    font=("yu gothic ui SemiBold", 13 * -1),
    bg="#3D404B"
)
Login_emailName_text.place(x=25, y=0)

Login_emailName_icon = PhotoImage(file="assets\\email-icon.png")
Login_emailName_icon_Label = Label(
    Login_emailName_image_Label,
    image=Login_emailName_icon,
    bg="#3D404B"
)
Login_emailName_icon_Label.place(x=370, y=15)

Login_emailName_entry = Entry(
    Login_emailName_image_Label,
    bd=0,
    bg="#3D404B",
    highlightthickness=0,
    font=("yu gothic ui SemiBold", 16 * -1),
    textvariable=email
)
Login_emailName_entry.place(x=8, y=17, width=354, height=27)

# ================ Password Name Section ====================
Login_passwordName_image = PhotoImage(file="assets\\email.png")
Login_passwordName_image_Label = Label(
    bg_imageLogin,
    image=Login_passwordName_image,
    bg="#272A37"
)
Login_passwordName_image_Label.place(x=80, y=330)

Login_passwordName_text = Label(
    Login_passwordName_image_Label,
    text="Password",
    fg="#FFFFFF",
    font=("yu gothic ui SemiBold", 13 * -1),
    bg="#3D404B"
)
Login_passwordName_text.place(x=25, y=0)

Login_passwordName_icon = PhotoImage(file="assets\\pass-icon.png")
Login_passwordName_icon_Label = Label(
    Login_passwordName_image_Label,
    image=Login_passwordName_icon,
    bg="#3D404B"
)
Login_passwordName_icon_Label.place(x=370, y=15)

Login_passwordName_entry = Entry(
    Login_passwordName_image_Label,
    bd=0,
    bg="#3D404B",
    highlightthickness=0,
    font=("yu gothic ui SemiBold", 16 * -1),
    show='*',
    textvariable=password
)
Login_passwordName_entry.place(x=8, y=17, width=354, height=27)

# =============== Submit Button ====================
Login_button_image_1 = PhotoImage(file="assets\\button_1.png")
Login_button_1 = Button(
    bg_imageLogin,
    image=Login_button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: signin(),
    relief="flat",
    activebackground="#272A37",
    cursor="hand2",
)
Login_button_1.place(x=120, y=445, width=333, height=65)

# ================ Home Button ====================
pdf_home_image_right = PhotoImage(file="assets\\home.png", palette='red')
home_button = Button(
    bg_imageLogin,
    image=pdf_home_image_right,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: show_frame(index_page),
    relief="flat",
    activebackground="#272A37",
    cursor="hand2",
    bg='#272A37'
)
home_button.place(x=860, y=45, width=105, height=50)

# ================ Header Text Down ====================
Login_headerText_image_down = PhotoImage(file="assets\\headerText_image.png")
Login_headerText_image_label3 = Label(
    bg_imageLogin,
    image=Login_headerText_image_down,
    bg="#272A37"
)
Login_headerText_image_label3.place(x=650, y=530)

Login_headerText3 = Label(
    bg_imageLogin,
    text="Powered by Signature Group",
    fg="#FFFFFF",
    font=("yu gothic ui bold", 20 * -1),
    bg="#272A37"
)
Login_headerText3.place(x=700, y=530)

login_check_btn = Checkbutton(bg_imageLogin, text='show password', fg="#FFFFFF", bg='#272A37', selectcolor='#272A37',
                              activebackground='#272A37',
                              font=("yu gothic ui", 11, 'bold'),
                              bd=0,
                              command=lambda: show_password(Login_passwordName_entry))
login_check_btn.place(x=210, y=390)


def clear_signin():
    email.set("")
    password.set("")

    login_check_btn.deselect()


def signin():
    global AUTHENTICATE
    if Login_emailName_entry.get() == "" or Login_passwordName_entry.get() == "":
        messagebox.showerror("Error", "All Fields are Required")
    else:
        userEmail = Login_emailName_entry.get()
        userPassword = Login_passwordName_entry.get()

        if authentication.sign_in(userEmail, userPassword):
            AUTHENTICATE = True
            clear_signin()
            show_frame(load_pdf)
        else:
            messagebox.showerror("Alert", "Email or Password is wrong.")


# ====================================================================================
# =========================== LOAD PDF PAGE START HERE ===============================
# ====================================================================================

# Load PDF Text Variables
pdfID = StringVar()

load_pdf.configure(bg="#525561")

# ================Background Image ====================
pdf_backgroundImage = PhotoImage(file="assets\\image_1.png")
bg_image_pdf = Label(
    load_pdf,
    image=pdf_backgroundImage,
    bg="#525561"
)
bg_image_pdf.place(x=120, y=28)

# ================ Header Text Left ====================
pdf_headerText_image_left = PhotoImage(file="assets\\headerText_image.png")
pdf_headerText_image_label1 = Label(
    bg_image_pdf,
    image=pdf_headerText_image_left,
    bg="#272A37"
)
pdf_headerText_image_label1.place(x=60, y=45)

pdf_headerText1 = Label(
    bg_image_pdf,
    text="Air Signature",
    fg="#FFFFFF",
    font=("yu gothic ui bold", 20 * -1),
    bg="#272A37"
)
pdf_headerText1.place(x=110, y=45)

# ================ LOAD PDF HEADER ====================
pdf_header = Label(
    bg_image_pdf,
    text="Load the PDF to Verify",
    fg="#FFFFFF",
    font=("yu gothic ui Bold", 28 * -1),
    bg="#272A37"
)
pdf_header.place(x=370, y=200)

# ================ PDF ID Section ====================
pdf_id_image = PhotoImage(file="assets\\email.png")
pdf_id_image_Label = Label(
    bg_image_pdf,
    image=pdf_id_image,
    bg="#272A37"
)
pdf_id_image_Label.place(x=320, y=280)

pdf_id_text = Label(
    pdf_id_image_Label,
    text="PDF ID",
    fg="#FFFFFF",
    font=("yu gothic ui SemiBold", 13 * -1),
    bg="#3D404B"
)
pdf_id_text.place(x=8, y=0)

pdf_id_entry = Entry(
    pdf_id_image_Label,
    bd=0,
    bg="#3D404B",
    highlightthickness=0,
    font=("yu gothic ui SemiBold", 16 * -1),
    textvariable=pdfID
)
pdf_id_entry.place(x=8, y=17, width=354, height=27)

# =============== Submit Button ====================
pdf_id_image_1 = PhotoImage(file="assets\\button_1.png")
pdf_button_1 = Button(
    bg_image_pdf,
    image=pdf_id_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: sign_with_verify(),
    relief="flat",
    activebackground="#272A37",
    cursor="hand2",
)
pdf_button_1.place(x=370, y=375, width=333, height=65)

# ================ Home Button ====================
home_image_right = PhotoImage(file="assets\\home.png")
home_button = Button(
    bg_image_pdf,
    image=home_image_right,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: show_frame(index_page),
    relief="flat",
    activebackground="#272A37",
    cursor="hand2",
    bg='#272A37'
)
home_button.place(x=860, y=45, width=105, height=50)

# ================ Logout Button ====================
logout_image_right = PhotoImage(file="assets\\exit.png")
logout_button = Button(
    bg_image_pdf,
    image=logout_image_right,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: logout_event(),
    relief="flat",
    activebackground="#272A37",
    cursor="hand2",
    bg='#272A37'
)
logout_button.place(x=860, y=100, width=105, height=50)

# ================ Update Button ====================
update_image_right = PhotoImage(file="assets\\edit.png")
update_button = Button(
    bg_image_pdf,
    image=update_image_right,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: show_frame(update_page),
    relief="flat",
    activebackground="#272A37",
    cursor="hand2",
    bg='#272A37'
)
update_button.place(x=860, y=155, width=105, height=50)

# ================ Header Text Down ====================
pdf_headerText_image_down = PhotoImage(file="assets\\headerText_image.png")
pdf_headerText_image_label3 = Label(
    bg_image_pdf,
    image=pdf_headerText_image_down,
    bg="#272A37"
)
pdf_headerText_image_label3.place(x=650, y=530)

pdf_headerText3 = Label(
    bg_image_pdf,
    text="Powered by Signature Group",
    fg="#FFFFFF",
    font=("yu gothic ui bold", 20 * -1),
    bg="#272A37"
)
pdf_headerText3.place(x=700, y=530)


def sign_without_verify():
    signature.withdraw()
    subprocess.run(['python', 'AirSigning//PDFAirSignerApp.py'])
    signature.deiconify()


def sign_with_verify():
    if pdf_id_entry.get() == "":
        messagebox.showerror("Error", "All Fields are Required")
    else:
        pdf_id = pdf_id_entry.get()
        pdfID.set("")

        if pdfApi.getPDF(pdf_id, authentication.getUserName(), authentication.gettoken()):
            signature.withdraw()
            subprocess.run(
                ['python', 'verification//PDFAirSignerApp.py', pdfApi.getDownloadedPdf(), authentication.getUserName()])
            signature.deiconify()
        else:
            messagebox.showerror("Id missed match", "No Pdf Found.")


def clickVerification():
    global authentication, AUTHENTICATE

    if authentication is None:
        authentication = AuthAPI()
    if AUTHENTICATE:
        show_frame(load_pdf)
    else:
        show_frame(sign_in)


def logout_event():
    global AUTHENTICATE
    if AUTHENTICATE:
        authentication.logout()
    show_frame(index_page)
    AUTHENTICATE = False


def close_app():
    global AUTHENTICATE
    if AUTHENTICATE:
        authentication.logout()
    signature.destroy()


signature.protocol("WM_DELETE_WINDOW", close_app)

signature.resizable(False, False)
signature.mainloop()
