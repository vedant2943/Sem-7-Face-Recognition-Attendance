import os
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from student import Student
from train import Train
from face_recognition import Face_Recognition
from developer import Developer

class Face_Recognition_System:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")
        
        # Define a modern color scheme
        self.bg_color = "#2c3e50" # Dark slate blue
        self.btn_color = "#34495e" # Slightly lighter slate blue
        self.text_color = "white"
        self.title_font = ("tahoma", 24, "bold") # Slightly smaller title font
        self.btn_font = ("tahoma", 14, "bold")
        self.icon_size = (130, 130) # Slightly larger icons
        self.btn_width = 240 # Standard button width
        self.btn_height = 200 # Standard button height

        # === 1. MODERN TITLE BAR (Moved to top) ===
        # Removed the image banner completely
        title_lbl = Label(self.root, text="FACE RECOGNITION ATTENDANCE SYSTEM", font=self.title_font, bg=self.btn_color,
                          fg=self.text_color)
        title_lbl.place(x=0, y=0, width=1530, height=45)


        # === 2. BACKGROUND IMAGE (Adjusted position) ===
        try:
            img3 = Image.open(r"images/futuristic-biometric-technology_1302-17807.png")
            # Adjusted height slightly to fit below new title bar position
            img3 = img3.resize((1530, 790-45), Image.BILINEAR) 
            self.photoimg3 = ImageTk.PhotoImage(img3)

            bg_img = Label(self.root, image=self.photoimg3)
            # Starts right below the title bar
            bg_img.place(x=0, y=45, width=1530, height=790-45) 
        except Exception as e:
            print(f"Error loading background image: {e}")
            # Fallback if image is missing
            bg_img = Label(self.root, bg="white")
            bg_img.place(x=0, y=45, width=1530, height=790-45)


        # === 3. COMBINED & STYLED BUTTONS (Resized & Realigned) ===
        # Buttons are now placed relative to bg_img
        
        # Define starting positions and padding for the grid
        start_x = 150 
        start_y = 60 # Start buttons lower down from title
        pad_x = 40
        pad_y = 40

        # --- Button 1: Employee Details ---
        try:
            img4 = Image.open(r"images/hand-drawn-flat-design-people-waving-illustration_23-2149217484.png")
            img4 = img4.resize(self.icon_size, Image.BILINEAR)
            self.photoimg4 = ImageTk.PhotoImage(img4)
        except Exception as e:
            print(f"Error loading img4: {e}")
            self.photoimg4 = None 

        b1_1 = Button(bg_img, text="Employee Details", command=self.student_details, cursor="hand2",
                      image=self.photoimg4, compound=TOP, font=self.btn_font, 
                      bg=self.btn_color, fg=self.text_color, relief=RIDGE, borderwidth=2,
                      pady=10) # Add padding inside button
        b1_1.place(x=start_x, y=start_y, width=self.btn_width, height=self.btn_height)

        # --- Button 2: Face Recognizer ---
        try:
            img5 = Image.open(r"images/55455d756425ac48168ea90d9dc3b883.png")
            img5 = img5.resize(self.icon_size, Image.BILINEAR)
            self.photoimg5 = ImageTk.PhotoImage(img5)
        except Exception as e:
            print(f"Error loading img5: {e}")
            self.photoimg5 = None

        b2_1 = Button(bg_img, text="Face Recognizer", cursor="hand2", command=self.face_data,
                      image=self.photoimg5, compound=TOP, font=self.btn_font, 
                      bg=self.btn_color, fg=self.text_color, relief=RIDGE, borderwidth=2,
                      pady=10)
        b2_1.place(x=start_x + self.btn_width + pad_x, y=start_y, width=self.btn_width, height=self.btn_height)

        # --- Button 3: Attendance ---
        try:
            img6 = Image.open(r"images/mobile-face-scan_24908-56399.png")
            img6 = img6.resize(self.icon_size, Image.BILINEAR)
            self.photoimg6 = ImageTk.PhotoImage(img6)
        except Exception as e:
            print(f"Error loading img6: {e}")
            self.photoimg6 = None

        b3_1 = Button(bg_img, text="Attendance", cursor="hand2", command=self.open_img23,
                      image=self.photoimg6, compound=TOP, font=self.btn_font, 
                      bg=self.btn_color, fg=self.text_color, relief=RIDGE, borderwidth=2,
                      pady=10)
        b3_1.place(x=start_x + 2*(self.btn_width + pad_x), y=start_y, width=self.btn_width, height=self.btn_height)

        # --- Button 4: Help Desk ---
        try:
            img7 = Image.open(r"images/call-center-background-flat-design_23-2147954923.png")
            img7 = img7.resize(self.icon_size, Image.BILINEAR)
            self.photoimg7 = ImageTk.PhotoImage(img7)
        except Exception as e:
            print(f"Error loading img7: {e}")
            self.photoimg7 = None

        b4_1 = Button(bg_img, text="Help Desk", cursor="hand2", # Add command later if needed
                      image=self.photoimg7, compound=TOP, font=self.btn_font, 
                      bg=self.btn_color, fg=self.text_color, relief=RIDGE, borderwidth=2,
                      pady=10) 
        b4_1.place(x=start_x + 3*(self.btn_width + pad_x), y=start_y, width=self.btn_width, height=self.btn_height)

        # --- Button 5: Train data ---
        try:
            img8 = Image.open(r"images/automatic-recognition-software-analyzing-city-collage_23-2150966933.png")
            img8 = img8.resize(self.icon_size, Image.BILINEAR)
            self.photoimg8 = ImageTk.PhotoImage(img8)
        except Exception as e:
            print(f"Error loading img8: {e}")
            self.photoimg8 = None

        b5_1 = Button(bg_img, text="Train data", cursor="hand2", command=self.train_data,
                      image=self.photoimg8, compound=TOP, font=self.btn_font, 
                      bg=self.btn_color, fg=self.text_color, relief=RIDGE, borderwidth=2,
                      pady=10)
        b5_1.place(x=start_x, y=start_y + self.btn_height + pad_y, width=self.btn_width, height=self.btn_height) 

        # --- Button 6: Photos ---
        try:
            img9 = Image.open(r"images/istockphoto-1306235479-612x612.jpg")
            img9 = img9.resize(self.icon_size, Image.BILINEAR)
            self.photoimg9 = ImageTk.PhotoImage(img9)
        except Exception as e:
            print(f"Error loading img9: {e}")
            self.photoimg9 = None

        b6_1 = Button(bg_img, text="Photos", cursor="hand2", command=self.open_img,
                      image=self.photoimg9, compound=TOP, font=self.btn_font, 
                      bg=self.btn_color, fg=self.text_color, relief=RIDGE, borderwidth=2,
                      pady=10)
        b6_1.place(x=start_x + self.btn_width + pad_x, y=start_y + self.btn_height + pad_y, width=self.btn_width, height=self.btn_height)

        # --- Button 7: Developer ---
        try:
            img10 = Image.open(r"images/view-3d-man-using-laptop_23-2150709796.png")
            img10 = img10.resize(self.icon_size, Image.BILINEAR)
            self.photoimg10 = ImageTk.PhotoImage(img10)
        except Exception as e:
            print(f"Error loading img10: {e}")
            self.photoimg10 = None

        b7_1 = Button(bg_img, text="Developer", cursor="hand2", command=self.developer_details,
                      image=self.photoimg10, compound=TOP, font=self.btn_font, 
                      bg=self.btn_color, fg=self.text_color, relief=RIDGE, borderwidth=2,
                      pady=10)
        b7_1.place(x=start_x + 2*(self.btn_width + pad_x), y=start_y + self.btn_height + pad_y, width=self.btn_width, height=self.btn_height)

        # --- Button 8: Exit ---
        try:
            img11 = Image.open(r"images/illustration-exit-door_53876-5844.png")
            img11 = img11.resize(self.icon_size, Image.BILINEAR)
            self.photoimg11 = ImageTk.PhotoImage(img11)
        except Exception as e:
            print(f"Error loading img11: {e}")
            self.photoimg11 = None

        b8_1 = Button(bg_img, text="Exit", cursor="hand2", command=self.root.quit,
                      image=self.photoimg11, compound=TOP, font=self.btn_font, 
                      bg=self.btn_color, fg=self.text_color, relief=RIDGE, borderwidth=2,
                      pady=10)
        b8_1.place(x=start_x + 3*(self.btn_width + pad_x), y=start_y + self.btn_height + pad_y, width=self.btn_width, height=self.btn_height)

    # ************Function Buttons (No changes here)****************

    def open_img(self):
        try:
            os.startfile("data")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open data folder: {e}", parent=self.root)


    def student_details(self):
        self.new_window=Toplevel(self.root)
        self.app=Student(self.new_window) # This is correct, it just opens the Student class

    def train_data(self):
        self.new_window=Toplevel(self.root)
        self.app=Train(self.new_window)


    def face_data(self):
        self.new_window=Toplevel(self.root)
        self.app=Face_Recognition(self.new_window)

    def developer_details(self):
        self.new_window=Toplevel(self.root)
        self.app=Developer(self.new_window)
    
    def open_img23(self):
        try:
            os.startfile("attendance.csv")
        except Exception as e:
             messagebox.showerror("Error", f"Could not open attendance.csv: {e}", parent=self.root)

    
if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition_System(root)
    root.mainloop()

