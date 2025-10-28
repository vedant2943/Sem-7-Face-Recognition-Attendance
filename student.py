from tkinter import *
from tkinter import ttk
from tkinter import messagebox  # Keep messagebox import
from PIL import Image, ImageTk
import mysql.connector
import cv2
import os

class Student:  # Keep class name as Student for consistency with main.py

    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Employee Management System") # Changed window title

        # Define color scheme (same as main.py)
        self.bg_color = "#2c3e50" 
        self.frame_color = "#34495e" 
        self.text_color = "white"
        self.title_font = ("tahoma", 24, "bold") 
        self.label_font = ("tahoma", 12, "bold")
        self.entry_font = ("tahoma", 11) 
        self.button_font = ("tahoma", 12, "bold")

        # ****************Variables**************
        self.var_dep = StringVar()
        self.var_course = StringVar() # Job Title
        self.var_year = StringVar()   # Hire Date
        self.var_semester = StringVar() # Unused
        self.var_std_id = StringVar()   # Employee ID
        self.var_std_name = StringVar() # Employee Name
        self.var_div = StringVar()      # Shift
        self.var_roll = StringVar()     # Unused
        self.var_gender = StringVar()
        self.var_dob = StringVar()
        self.var_email = StringVar()
        self.var_phone = StringVar()
        self.var_address = StringVar()
        self.var_teacher = StringVar() # Manager
        self.var_radio1 = StringVar(value="No") # Default photo sample to No


        # === 1. MODERN TITLE BAR (Moved to top) ===
        title_lbl = Label(self.root, text="EMPLOYEE MANAGEMENT SYSTEM", font=self.title_font, bg=self.frame_color,
                          fg=self.text_color)
        title_lbl.place(x=0, y=0, width=1530, height=45)

        # === 2. BACKGROUND IMAGE (Adjusted position) ===
        try:
            img3 = Image.open(r"images/view-3d-man-using-laptop_23-2150709796.png") # Using a different BG image
            img3 = img3.resize((1530, 790-45), Image.BILINEAR) 
            self.photoimg3 = ImageTk.PhotoImage(img3)
            bg_img = Label(self.root, image=self.photoimg3)
            bg_img.place(x=0, y=45, width=1530, height=790-45) 
        except Exception as e:
            print(f"Error loading background image: {e}")
            bg_img = Label(self.root, bg=self.bg_color) # Fallback to solid color
            bg_img.place(x=0, y=45, width=1530, height=790-45)

        # Main content frame on top of the background
        main_frame = Frame(bg_img, bd=2, relief=RIDGE, bg="white") # Slightly offset background
        main_frame.place(x=10, y=10, width=1510, height=700) # Adjusted size/position


        # --- Left Frame ---
        left_frame = LabelFrame(main_frame, bd=2, relief=RIDGE, text="Employee Details",
                                font=self.label_font, bg=self.frame_color, fg=self.text_color)
        left_frame.place(x=10, y=5, width=740, height=680) # Adjusted size/position


        # --- Job Information Frame ---
        current_course_frame = LabelFrame(left_frame, bd=2, relief=RIDGE, text="Job Information",
                                          font=self.label_font, bg=self.frame_color, fg=self.text_color)
        current_course_frame.place(x=5, y=5, width=730, height=130) # Adjusted size/position

        # Department
        dep_label = Label(current_course_frame, text="Department", font=self.label_font, bg=self.frame_color, fg=self.text_color)
        dep_label.grid(row=0, column=0, padx=5, pady=5, sticky=W)
        dep_combo = ttk.Combobox(current_course_frame, textvariable=self.var_dep, font=self.entry_font,
                                 width=20, state="readonly")
        dep_combo["values"] = ("Select Department", "Engineering", "Sales", "Marketing", "HR", "Finance")
        dep_combo.current(0)
        dep_combo.grid(row=0, column=1, padx=5, pady=5, sticky=W)

        # Job Title
        course_label = Label(current_course_frame, text="Job Title", font=self.label_font, bg=self.frame_color, fg=self.text_color)
        course_label.grid(row=0, column=2, padx=5, pady=5, sticky=W)
        course_combo = ttk.Combobox(current_course_frame, textvariable=self.var_course, font=self.entry_font, 
                                    width=20, state="readonly")
        course_combo["values"] = ("Select Title", "Manager", "Analyst", "Developer", "Associate", "Intern")
        course_combo.current(0)
        course_combo.grid(row=0, column=3, padx=5, pady=5, sticky=W)

        # Hire Date
        year_label = Label(current_course_frame, text="Hire Date", font=self.label_font, bg=self.frame_color, fg=self.text_color)
        year_label.grid(row=1, column=0, padx=5, pady=5, sticky=W)
        year_entry = ttk.Entry(current_course_frame, textvariable=self.var_year, width=22, # Adjusted width to match combobox
                               font=self.entry_font)
        year_entry.grid(row=1, column=1, padx=5, pady=5, sticky=W)

        # --- Employee Personal Info Frame ---
        class_Student_frame = LabelFrame(left_frame, bd=2, relief=RIDGE, text="Employee Personal Info",
                                         font=self.label_font, bg=self.frame_color, fg=self.text_color)
        class_Student_frame.place(x=5, y=140, width=730, height=530) # Adjusted size/position

        # Employee Id
        studentId_label = Label(class_Student_frame, text="Employee Id", font=self.label_font, bg=self.frame_color, fg=self.text_color)
        studentId_label.grid(row=0, column=0, padx=10, pady=5, sticky=W)
        studentId_entry = ttk.Entry(class_Student_frame, textvariable=self.var_std_id, width=20,
                                    font=self.entry_font)
        studentId_entry.grid(row=0, column=1, padx=10, pady=5, sticky=W)

        # Employee name
        studentName_label = Label(class_Student_frame, text="Employee Name", font=self.label_font, bg=self.frame_color, fg=self.text_color)
        studentName_label.grid(row=0, column=2, padx=10, pady=5, sticky=W)
        studentName_entry = ttk.Entry(class_Student_frame, textvariable=self.var_std_name, width=20,
                                      font=self.entry_font)
        studentName_entry.grid(row=0, column=3, padx=10, pady=5, sticky=W)

        # Shift
        class_div_label = Label(class_Student_frame, text="Shift", font=self.label_font, bg=self.frame_color, fg=self.text_color)
        class_div_label.grid(row=1, column=0, padx=10, pady=5, sticky=W)
        div_combo = ttk.Combobox(class_Student_frame, textvariable=self.var_div, font=self.entry_font, 
                                 width=18, state="readonly")
        div_combo["values"] = ("Select Shift", "Day", "Night", "General")
        div_combo.current(0)
        div_combo.grid(row=1, column=1, padx=10, pady=5, sticky=W)

        # Gender
        gender_label = Label(class_Student_frame, text="Gender", font=self.label_font, bg=self.frame_color, fg=self.text_color)
        gender_label.grid(row=1, column=2, padx=10, pady=5, sticky=W) # Moved Gender up
        gender_combo = ttk.Combobox(class_Student_frame, textvariable=self.var_gender, font=self.entry_font, 
                                    width=18, state="readonly")
        gender_combo["values"] = ("Male", "Female", "Other")
        gender_combo.current(0)
        gender_combo.grid(row=1, column=3, padx=10, pady=5, sticky=W) # Moved Gender up

        # DOB
        dob_label = Label(class_Student_frame, text="DOB", font=self.label_font, bg=self.frame_color, fg=self.text_color)
        dob_label.grid(row=2, column=0, padx=10, pady=5, sticky=W)
        dob_entry = ttk.Entry(class_Student_frame, textvariable=self.var_dob, width=20,
                              font=self.entry_font)
        dob_entry.grid(row=2, column=1, padx=10, pady=5, sticky=W)

        # Email
        email_label = Label(class_Student_frame, text="Email", font=self.label_font, bg=self.frame_color, fg=self.text_color)
        email_label.grid(row=2, column=2, padx=10, pady=5, sticky=W)
        email_entry = ttk.Entry(class_Student_frame, textvariable=self.var_email, width=20,
                                font=self.entry_font)
        email_entry.grid(row=2, column=3, padx=10, pady=5, sticky=W)   

        # Phone no
        phone_label = Label(class_Student_frame, text="Phone no", font=self.label_font, bg=self.frame_color, fg=self.text_color)
        phone_label.grid(row=3, column=0, padx=10, pady=5, sticky=W)
        phone_entry = ttk.Entry(class_Student_frame, textvariable=self.var_phone, width=20,
                                font=self.entry_font)
        phone_entry.grid(row=3, column=1, padx=10, pady=5, sticky=W)

        # Address
        address_label = Label(class_Student_frame, text="Address", font=self.label_font, bg=self.frame_color, fg=self.text_color)
        address_label.grid(row=3, column=2, padx=10, pady=5, sticky=W)
        address_entry = ttk.Entry(class_Student_frame, textvariable=self.var_address, width=20,
                                  font=self.entry_font)
        address_entry.grid(row=3, column=3, padx=10, pady=5, sticky=W)

        # Manager
        teacher_label = Label(class_Student_frame, text="Manager", font=self.label_font, bg=self.frame_color, fg=self.text_color)
        teacher_label.grid(row=4, column=0, padx=10, pady=5, sticky=W)
        teacher_entry = ttk.Entry(class_Student_frame, textvariable=self.var_teacher, width=20,
                                  font=self.entry_font)
        teacher_entry.grid(row=4, column=1, padx=10, pady=5, sticky=W)

        # --- Photo Sample Radio Buttons ---
        # Using a frame for better layout control
        radio_frame = Frame(class_Student_frame, bg=self.frame_color)
        radio_frame.grid(row=5, column=0, columnspan=4, pady=10, sticky=W, padx=10)

        photo_label = Label(radio_frame, text="Photo Sample:", font=self.label_font, bg=self.frame_color, fg=self.text_color)
        photo_label.pack(side=LEFT, padx=5)

        # Style for Radiobuttons
        style = ttk.Style()
        style.configure("TRadiobutton", background=self.frame_color, foreground="black", font=self.entry_font) # Basic style
        
        radiobtn1 = ttk.Radiobutton(radio_frame, variable=self.var_radio1, text="Take photo sample", value="Yes", style="TRadiobutton")
        radiobtn1.pack(side=LEFT, padx=10)

        radiobtn2 = ttk.Radiobutton(radio_frame, variable=self.var_radio1, text="No photo sample", value="No", style="TRadiobutton")
        radiobtn2.pack(side=LEFT, padx=10)


        # --- Button Frames (Combined and Styled) ---
        btn_frame_main = Frame(class_Student_frame, bd=2, relief=RIDGE, bg="white")
        btn_frame_main.place(x=5, y=350, width=720, height=130) # Adjusted position

        # Save Button
        save_btn = Button(btn_frame_main, text="Save", command=self.add_data, width=15, font=self.button_font,
                          bg=self.frame_color, fg=self.text_color, relief=RIDGE, borderwidth=2)
        save_btn.grid(row=0, column=0, padx=10, pady=10)

        # Update Button
        update_btn = Button(btn_frame_main, text="Update", command=self.update_data, width=15, font=self.button_font, 
                            bg=self.frame_color, fg=self.text_color, relief=RIDGE, borderwidth=2)
        update_btn.grid(row=0, column=1, padx=10, pady=10)

        # Delete Button
        delete_btn = Button(btn_frame_main, text="Delete", command=self.delete_data, width=15, font=self.button_font, 
                            bg=self.frame_color, fg=self.text_color, relief=RIDGE, borderwidth=2)
        delete_btn.grid(row=0, column=2, padx=10, pady=10)

        # Reset Button
        reset_btn = Button(btn_frame_main, text="Reset", command=self.reset_data, width=15, font=self.button_font, 
                           bg=self.frame_color, fg=self.text_color, relief=RIDGE, borderwidth=2)
        reset_btn.grid(row=0, column=3, padx=10, pady=10)

        # Take Photo Button (Full Width on next row)
        take_photo_btn = Button(btn_frame_main, command=self.generate_data, text="Take Photo Sample", width=32, 
                                font=self.button_font, bg=self.frame_color, fg=self.text_color, relief=RIDGE, borderwidth=2)
        take_photo_btn.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky=W)

        # Update Photo Button (Full Width on next row)
        update_photo_btn = Button(btn_frame_main, text="Update Photo Sample", width=32, 
                                  font=self.button_font, bg=self.frame_color, fg=self.text_color, relief=RIDGE, borderwidth=2)
        update_photo_btn.grid(row=1, column=2, columnspan=2, padx=10, pady=10, sticky=W)


        # --- Right Frame ---
        right_frame = LabelFrame(main_frame, bd=2, relief=RIDGE, text="Employee Records",
                                 font=self.label_font, bg=self.frame_color, fg=self.text_color)
        right_frame.place(x=755, y=5, width=745, height=680) # Adjusted size/position


        # Search System Frame
        Search_frame = LabelFrame(right_frame, bd=2, relief=RIDGE, text="Search System",
                                  font=self.label_font, bg=self.frame_color, fg=self.text_color)
        Search_frame.place(x=5, y=5, width=735, height=70)

        search_label = Label(Search_frame, text="Search By:", font=self.label_font, bg=self.frame_color, fg=self.text_color)
        search_label.grid(row=0, column=0, padx=5, pady=5, sticky=W)

        self.var_search_combo = StringVar()
        search_combo = ttk.Combobox(Search_frame, textvariable=self.var_search_combo, font=self.entry_font, width=15, state="readonly")
        search_combo["values"] = ("Select", "Employee_ID", "Phone_No") # Student_ID is db col
        search_combo.current(0)
        search_combo.grid(row=0, column=1, padx=5, pady=5, sticky=W)

        self.var_search_entry = StringVar()
        search_entry = ttk.Entry(Search_frame, textvariable=self.var_search_entry, width=18, font=self.entry_font)
        search_entry.grid(row=0, column=2, padx=5, pady=5, sticky=W)

        search_btn = Button(Search_frame, text="Search", command=self.search_data, width=12, font=self.button_font, 
                            bg=self.frame_color, fg=self.text_color, relief=RIDGE, borderwidth=2)
        search_btn.grid(row=0, column=3, padx=5, pady=5)

        showAll_btn = Button(Search_frame, text="Show All", command=self.fetch_data, width=12, font=self.button_font, 
                             bg=self.frame_color, fg=self.text_color, relief=RIDGE, borderwidth=2)
        showAll_btn.grid(row=0, column=4, padx=5, pady=5)


        # Table Frame
        table_frame = Frame(right_frame, bd=2, relief=RIDGE, bg="white")
        table_frame.place(x=5, y=80, width=735, height=590) # Adjusted size/position

        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        self.student_table = ttk.Treeview(table_frame, column=(
            "dep", "course", "year", "sem", "id", "name","roll", "div", "gender", "dob", "email", "phone", "address", # Removed duplicate gender
            "teacher", "photo"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set) # Removed photosample column display

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)

        # Configure Treeview Style
        style.configure("Treeview.Heading", font=self.label_font, background=self.frame_color, foreground=self.text_color, relief=FLAT)
        style.map("Treeview.Heading", background=[('active', self.bg_color)]) # Hover color
        style.configure("Treeview", font=self.entry_font, rowheight=25, fieldbackground="white")
        style.map("Treeview", background=[('selected', self.bg_color)], foreground=[('selected', self.text_color)])


        self.student_table.heading("dep", text="Department")
        self.student_table.heading("course", text="Job Title")
        self.student_table.heading("year", text="Hire Date")
        self.student_table.heading("sem", text="-") # Removed Semester
        self.student_table.heading("id", text="Emp. ID")
        self.student_table.heading("name", text="Name")
        self.student_table.heading("roll", text="-") # Removed Roll
        self.student_table.heading("div", text="Shift")
        self.student_table.heading("gender", text="Gender")
        self.student_table.heading("dob", text="DOB")
        self.student_table.heading("email", text="Email")
        self.student_table.heading("phone", text="Phone")
        self.student_table.heading("address", text="Address")
        self.student_table.heading("teacher", text="Manager")
        self.student_table.heading("photo", text="Photo Sample") # Simplified header
        self.student_table["show"] = "headings"

        # Adjust column widths (make Name wider)
        self.student_table.column("dep", width=100)
        self.student_table.column("course", width=100)
        self.student_table.column("year", width=80)
        self.student_table.column("sem", width=20, minwidth=10) # Minimal width
        self.student_table.column("id", width=70)
        self.student_table.column("name", width=120)
        self.student_table.column("roll", width=20, minwidth=10) # Minimal width
        self.student_table.column("div", width=60)
        self.student_table.column("gender", width=60)
        self.student_table.column("dob", width=80)
        self.student_table.column("email", width=120)
        self.student_table.column("phone", width=100)
        self.student_table.column("address", width=120)
        self.student_table.column("teacher", width=100)
        self.student_table.column("photo", width=100)

        self.student_table.pack(fill=BOTH, expand=1)
        self.student_table.bind("<ButtonRelease>", self.get_cursor)
        self.fetch_data() # Initial data load

    # *************Function Declaration*************

    def add_data(self):
        # Validate Hire Date and DOB format if needed here (simple validation)
        if not self.var_year.get(): # Example: Ensure Hire Date is not empty
            messagebox.showerror("Error", "Hire Date is required", parent=self.root)
            return
        if self.var_dep.get() == "Select Department" or self.var_std_name.get() == "" or self.var_std_id.get() == "":
            messagebox.showerror("Error", "Required fields are missing (Dept, ID, Name)", parent=self.root)
            return # Stop execution if validation fails
            
        try:
            conn = mysql.connector.connect(host="localhost", username="root", password="vedant29@3",
                                           database="face_recognizer")
            my_cursor = conn.cursor()
            
            my_cursor.execute(
                "INSERT INTO student (Dep, course, Year, Semester, Student_id, Name, Division, Roll, Gender, Dob, Email, Phone, Address, Teacher, PhotoSample) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (
                    self.var_dep.get(),
                    self.var_course.get(), # Job Title
                    self.var_year.get(), # Hire Date
                    "", # Semester - Pass empty string
                    self.var_std_id.get(), # Emp ID
                    self.var_std_name.get(), # Name
                    self.var_div.get(), # Shift
                    "", # Roll - Pass empty string
                    self.var_gender.get(),
                    self.var_dob.get(),
                    self.var_email.get(),
                    self.var_phone.get(),
                    self.var_address.get(),
                    self.var_teacher.get(), # Manager
                    self.var_radio1.get()
                )
            )

            conn.commit()
            self.fetch_data() # Refresh table
            conn.close()
            messagebox.showinfo("Success", "Employee details added successfully!", parent=self.root)
            self.reset_data() # Clear form after successful save

        except mysql.connector.Error as err:
             messagebox.showerror("Database Error", f"Error: {err}", parent=self.root)
        except Exception as es:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(es)}", parent=self.root)


    def fetch_data(self):
        try:
            conn = mysql.connector.connect(host="localhost", username="root", password="vedant29@3",
                                           database="face_recognizer")
            my_cursor = conn.cursor()
            my_cursor.execute("select * from student")
            data = my_cursor.fetchall()

            self.student_table.delete(*self.student_table.get_children()) # Clear existing data
            if data:
                for i in data:
                    # Ensure we insert the correct number of values, providing defaults for missing ones if necessary
                    # Assuming the table order matches the query `select *`
                     display_values = list(i[:15]) # Take first 15 columns as defined in INSERT
                     # Replace None with "" for display
                     display_values = ["" if v is None else v for v in display_values]
                     self.student_table.insert("", END, values=display_values)
            conn.commit() # Not strictly needed for SELECT, but good practice
            conn.close()
        except mysql.connector.Error as err:
             messagebox.showerror("Database Error", f"Error fetching data: {err}", parent=self.root)
        except Exception as es:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(es)}", parent=self.root)


    def get_cursor(self, event=""):
        try:
            cursor_focus = self.student_table.focus()
            if not cursor_focus: # If no item is selected
                return
            content = self.student_table.item(cursor_focus)
            data = content["values"]

            # Check if data has enough elements before accessing indices
            if len(data) >= 15:
                self.var_dep.set(data[0] if data[0] else "Select Department")
                self.var_course.set(data[1] if data[1] else "Select Title") 
                self.var_year.set(data[2] if data[2] else "")      
                # self.var_semester.set(data[3]) # Unused
                self.var_std_id.set(data[4] if data[4] else "")    
                self.var_std_name.set(data[5] if data[5] else "")  
                self.var_div.set(data[6] if data[6] else "Select Shift")     
                # self.var_roll.set(data[7]) # Unused
                self.var_gender.set(data[8] if data[8] else "Male")   
                self.var_dob.set(data[9] if data[9] else "")       
                self.var_email.set(data[10] if data[10] else "")   
                self.var_phone.set(data[11] if data[11] else "")   
                self.var_address.set(data[12] if data[12] else "") 
                self.var_teacher.set(data[13] if data[13] else "") 
                self.var_radio1.set(data[14] if data[14] else "No") 
            else:
                 print("Warning: Selected row has fewer than 15 data points.")
                 self.reset_data() # Clear form if data is incomplete

        except Exception as es:
             messagebox.showerror("Error", f"Could not process selected row: {es}", parent=self.root)
             self.reset_data() # Clear form on error


    def update_data(self):
        if self.var_dep.get() == "Select Department" or self.var_std_name.get() == "" or self.var_std_id.get() == "":
            messagebox.showerror("Error", "Required fields are missing (Dept, ID, Name)", parent=self.root)
            return

        try:
            Update = messagebox.askyesno("Confirm Update", "Do you want to update this employee's details?", parent=self.root)
            if Update:
                conn = mysql.connector.connect(host="localhost", username="root", password="vedant29@3",
                                               database="face_recognizer")
                my_cursor = conn.cursor()
                # Ensure Semester and Roll are handled (provide default/empty values)
                my_cursor.execute("UPDATE student SET Dep=%s, course=%s, Year=%s, Semester=%s, Name=%s, Division=%s, "
                                  "Roll=%s, Gender=%s, Dob=%s, Email=%s, Phone=%s, Address=%s, Teacher=%s, "
                                  "PhotoSample=%s WHERE Student_id=%s", (
                                      self.var_dep.get(),
                                      self.var_course.get(), # Job Title
                                      self.var_year.get(), # Hire Date
                                      "", # Semester - empty string
                                      self.var_std_name.get(),
                                      self.var_div.get(), # Shift
                                      "", # Roll - empty string
                                      self.var_gender.get(),
                                      self.var_dob.get(),
                                      self.var_email.get(),
                                      self.var_phone.get(),
                                      self.var_address.get(),
                                      self.var_teacher.get(), # Manager
                                      self.var_radio1.get(),
                                      self.var_std_id.get() # Emp ID
                                  ))
                conn.commit()
                self.fetch_data() # Refresh table
                conn.close()
                messagebox.showinfo("Success", "Employee details updated successfully!", parent=self.root)
                self.reset_data() # Clear form
            # else: Do nothing if user clicks No
        
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error updating data: {err}", parent=self.root)
        except Exception as es:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(es)}", parent=self.root)


    def delete_data(self):
        if not self.var_std_id.get():
            messagebox.showerror("Error", "Employee ID must be selected or entered", parent=self.root)
            return

        try:
            delete = messagebox.askyesno("Confirm Delete", f"Do you want to permanently delete Employee ID: {self.var_std_id.get()}?", parent=self.root)
            if delete:
                conn = mysql.connector.connect(host="localhost", username="root", password="vedant29@3",
                                               database="face_recognizer")
                my_cursor = conn.cursor()
                sql="DELETE FROM student WHERE Student_id=%s"
                val=(self.var_std_id.get(),)
                my_cursor.execute(sql,val)
                conn.commit()
                rows_affected = my_cursor.rowcount
                conn.close()

                if rows_affected > 0:
                    messagebox.showinfo("Deleted", f"Employee ID {self.var_std_id.get()} deleted successfully.", parent=self.root)
                    self.fetch_data() # Refresh table
                    self.reset_data() # Clear form
                else:
                     messagebox.showwarning("Not Found", f"Employee ID {self.var_std_id.get()} not found.", parent=self.root)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error deleting data: {err}", parent=self.root)
        except Exception as es:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(es)}", parent=self.root)


    def reset_data(self):
        self.var_dep.set("Select Department")
        self.var_course.set("Select Title")
        self.var_year.set("") 
        self.var_semester.set("") # Clear unused field
        self.var_std_id.set("")
        self.var_std_name.set("")
        self.var_div.set("Select Shift")
        self.var_roll.set("") # Clear unused field
        self.var_gender.set("Male")
        self.var_dob.set("")
        self.var_email.set("")
        self.var_phone.set("")
        self.var_address.set("")
        self.var_teacher.set("")
        self.var_radio1.set("No") # Default to No

    # --- Search Data Function ---
    def search_data(self):
        search_by = self.var_search_combo.get()
        search_term = self.var_search_entry.get()

        if search_by == "Select" or not search_term:
            messagebox.showwarning("Invalid Search", "Please select a search criteria and enter a search term.", parent=self.root)
            return

        # Map display name to actual DB column name
        search_column = ""
        if search_by == "Employee_ID":
            search_column = "Student_id" # Actual DB column name
        elif search_by == "Phone_No":
            search_column = "Phone"

        try:
            conn = mysql.connector.connect(host="localhost", username="root", password="vedant29@3",
                                           database="face_recognizer")
            my_cursor = conn.cursor()
            
            # Use parameterized query to prevent SQL injection
            query = f"SELECT * FROM student WHERE {search_column} LIKE %s"
            # Add wildcards for partial match
            search_value = f"%{search_term}%" 
            
            my_cursor.execute(query, (search_value,))
            data = my_cursor.fetchall()

            self.student_table.delete(*self.student_table.get_children()) # Clear existing data
            if data:
                for i in data:
                     display_values = list(i[:15])
                     display_values = ["" if v is None else v for v in display_values]
                     self.student_table.insert("", END, values=display_values)
            else:
                 messagebox.showinfo("No Results", "No employees found matching the search criteria.", parent=self.root)

            conn.close()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error searching data: {err}", parent=self.root)
        except Exception as es:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(es)}", parent=self.root)


    # --- Generate Data (Take Photos) ---
    def generate_data(self):
        if self.var_dep.get() == "Select Department" or self.var_std_name.get() == "" or self.var_std_id.get() == "":
            messagebox.showerror("Error", "Employee details (Dept, ID, Name) must be filled before taking photos.", parent=self.root)
            return
        
        # Check if the employee ID exists before taking photos. Update the PhotoSample status first.
        try:
            conn = mysql.connector.connect(host="localhost", username="root", password="vedant29@3", database="face_recognizer")
            my_cursor = conn.cursor()

            # Check if student exists
            my_cursor.execute("SELECT * FROM student WHERE Student_id=%s", (self.var_std_id.get(),))
            existing_employee = my_cursor.fetchone()

            if not existing_employee:
                 messagebox.showerror("Error", f"Employee ID {self.var_std_id.get()} not found. Please save the employee details first.", parent=self.root)
                 conn.close()
                 return

            # Update PhotoSample status to 'Yes' for this employee
            my_cursor.execute("UPDATE student SET PhotoSample='Yes' WHERE Student_id=%s", (self.var_std_id.get(),))
            conn.commit()
            self.fetch_data() # Refresh the table to show updated status
            
            # Determine the next sequential ID for saving photos (based on number of existing folders/files or a counter)
            # Original logic used count of rows, let's keep it simple for now, assuming ID matches user index
            # IMPORTANT: This photo ID logic might need refinement if Employee IDs are not sequential integers starting from 1
            my_cursor.execute("SELECT COUNT(*) FROM student")
            count_result = my_cursor.fetchone()
            photo_id_to_use = self.var_std_id.get() # Let's try using Employee ID directly
            
            conn.close() # Close connection before starting webcam

        except mysql.connector.Error as err:
             messagebox.showerror("Database Error", f"Error preparing for photo capture: {err}", parent=self.root)
             return
        except Exception as es:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(es)}", parent=self.root)
            return

        # --- Proceed with Photo Capture ---
        try:
            face_classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

            def face_cropped(img):
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_classifier.detectMultiScale(gray, 1.3, 5, minSize=(100,100)) # Added minSize
                if len(faces) == 0:
                    return None
                # Assume only one face, find the largest
                (x, y, w, h) = max(faces, key=lambda rect: rect[2] * rect[3]) 
                return img[y:y + h, x:x + w]

            cap = cv2.VideoCapture(0) 
            if not cap.isOpened():
                messagebox.showerror("Webcam Error", "Could not open webcam.", parent=self.root)
                return

            img_id = 0
            while True:
                ret, my_frame = cap.read()
                if not ret:
                    messagebox.showerror("Webcam Error", "Failed to capture frame.", parent=self.root)
                    break

                cropped_face = face_cropped(my_frame)
                
                display_frame = my_frame.copy() # Draw rectangle on copy

                if cropped_face is not None:
                    img_id += 1
                    face = cv2.resize(cropped_face, (450, 450))
                    face_gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                    
                    # Ensure data directory exists
                    if not os.path.exists("data"):
                        os.makedirs("data")
                        
                    file_name_path = f"data/user.{photo_id_to_use}.{img_id}.jpg"
                    cv2.imwrite(file_name_path, face_gray)
                    
                    # Draw rectangle and counter on the display frame
                    gray_disp = cv2.cvtColor(display_frame, cv2.COLOR_BGR2GRAY)
                    faces_disp = face_classifier.detectMultiScale(gray_disp, 1.3, 5, minSize=(100,100))
                    if len(faces_disp) > 0:
                       (x_disp, y_disp, w_disp, h_disp) = max(faces_disp, key=lambda r: r[2]*r[3])
                       cv2.rectangle(display_frame, (x_disp, y_disp), (x_disp+w_disp, y_disp+h_disp), (0, 255, 0), 2)
                    
                    cv2.putText(display_frame, f"Capturing: {img_id}/100", (30, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                    cv2.imshow("Capturing Face Sample", display_frame)

                else:
                    cv2.putText(display_frame, "No Face Detected", (30, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
                    cv2.imshow("Capturing Face Sample", display_frame)


                # Exit on Enter key or after 100 images
                key = cv2.waitKey(1)
                if key == 13 or img_id >= 100: 
                    break

            cap.release()
            cv2.destroyAllWindows()
            if img_id >= 100:
                messagebox.showinfo("Result", f"Photo samples generated successfully for Employee ID: {photo_id_to_use}", parent=self.root)
            else:
                 messagebox.showwarning("Incomplete", f"Photo sample generation stopped early ({img_id}/100 captured).", parent=self.root)
                 # Optionally update PhotoSample back to 'No' or keep 'Yes'
                 
        except cv2.error as cv_err:
             messagebox.showerror("OpenCV Error", f"Error during face capture: {cv_err}", parent=self.root)
             if 'cap' in locals() and cap.isOpened(): cap.release()
             cv2.destroyAllWindows()
        except Exception as es:
            messagebox.showerror("Error", f"An unexpected error occurred during photo capture: {str(es)}", parent=self.root)
            if 'cap' in locals() and cap.isOpened(): cap.release()
            cv2.destroyAllWindows()


if __name__ == "__main__":
    root = Tk()
    # Apply style to the root window if needed
    # root.configure(bg=self.bg_color) 
    obj = Student(root) # Keep class name Student
    root.mainloop()

