from tkinter import *
from PIL import Image, ImageTk
import cv2
import mysql.connector
from datetime import datetime

class Face_Recognition:

    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition Panel")

        # Define color scheme
        self.bg_color = "#2c3e50" 
        self.frame_color = "#34495e" 
        self.text_color = "white"
        self.title_font = ("tahoma", 24, "bold") 
        self.button_font = ("tahoma", 15, "bold")

        # === 1. MODERN TITLE BAR ===
        title_lbl = Label(self.root, text="FACE RECOGNITION PANEL", font=self.title_font, bg=self.frame_color,
                          fg=self.text_color)
        title_lbl.place(x=0, y=0, width=1530, height=45)

        # === 2. BACKGROUND (Solid Color) ===
        # Using a solid color background that matches the theme
        bg_img = Label(self.root, bg=self.bg_color)
        bg_img.place(x=0, y=45, width=1530, height=790-45)

        # === 3. MODERN, COMBINED BUTTON ===
        try:
            img_btn = Image.open("images/png-clipart-facial-recognition-system-face-detection-pattern-recognition-fingerprint-face-face-people-thumbnail.png")
            img_btn = img_btn.resize((180, 180), Image.BILINEAR)
            self.photo_btn = ImageTk.PhotoImage(img_btn)
            
            b1_1 = Button(bg_img, 
                          text="Face Detector", 
                          command=self.face_recog, 
                          image=self.photo_btn, 
                          compound=TOP, 
                          font=self.button_font, 
                          bg=self.frame_color, 
                          fg=self.text_color,
                          cursor="hand2",
                          relief=RIDGE,
                          borderwidth=2,
                          pady=15 # Add padding
                         )
            # Place the button in the center
            b1_1.place(relx=0.5, rely=0.4, anchor=CENTER, width=280, height=280)

        except Exception as e:
            print(f"Error loading button image: {e}")
            # Fallback button if image fails
            b1_1 = Button(bg_img, 
                          text="Face Detector", 
                          command=self.face_recog, 
                          font=self.button_font, 
                          bg=self.frame_color, 
                          fg=self.text_color,
                          cursor="hand2",
                          relief=RIDGE,
                          borderwidth=2
                         )
            b1_1.place(relx=0.5, rely=0.4, anchor=CENTER, width=280, height=100)


    # =====================Attendance===================
    # === MODIFIED to remove 'r' (roll number) from duplicate check ===
    def mark_attendance(self, i, r, n):
        already_marked = False
        with open("attendance.csv", "r+") as f:
            myDatalist = f.readlines()
            name_list = []
            for line in myDatalist:
                entry = line.split(",")
                name_list.append(entry[0])

            # Only check ID and Name for duplicates
            if i in name_list or n in name_list:
                already_marked = True

        if not already_marked:
            with open("attendance.csv", "a") as f:
                now = datetime.now()
                d1 = now.strftime("%d/%m/%Y")
                dtString = now.strftime("%H:%M:%S")
                # We still write 'r' (which is "N/A" now) to keep CSV columns consistent
                f.write(f"\n{i}, {r}, {n}, {dtString}, {d1}, Present")

               

    # =================face recognition==================
    def face_recog(self):
        def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, clf):
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            features = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbors, minSize=(100, 100))

            for (x, y, w, h) in features:
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 3)
                id, predict = clf.predict(gray_image[y:y+h, x:x+w])

                confidence = int((100 * (1 - predict / 300)))

                conn = mysql.connector.connect(user='root', password='vedant29@3', host='localhost', database='face_recognizer', port=3306)
                cursor = conn.cursor()

                # Get Name
                cursor.execute("select Name from student where Student_ID="+str(id))
                n = cursor.fetchone()
                n = str(n[0]) # Get first item from tuple

                # === GET ROLE (from 'course' column) ===
                cursor.execute("select course from student where Student_ID="+str(id))
                role = cursor.fetchone()
                role = str(role[0]) # Get first item from tuple

                # === GET ID ===
                cursor.execute("select Student_ID from student where Student_ID="+str(id))
                i = cursor.fetchone()
                i = str(i[0]) # Get first item from tuple
                
                conn.close() # Close connection

                if confidence > 77:
                    # === UPDATED TEXT OVERLAY ===
                    cv2.putText(img, f"ID: {i}", (x, y-80), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
                    cv2.putText(img, f"Name: {n}", (x, y-55), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
                    cv2.putText(img, f"Role: {role}", (x, y-30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
                    
                    # Pass "N/A" for the old roll number
                    self.mark_attendance(i, "N/A", n) 
                else:
                    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 3)
                    cv2.putText(img, "Unknown Face", (x, y-30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255), 2)

        def recognize(img, clf, face_cascade):
            draw_boundary(img, face_cascade, 1.1, 10, (255, 25, 255), "Face", clf)
            return img

        try:
            face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
            clf = cv2.face.LBPHFaceRecognizer_create()
            clf.read("classifier.xml")
        except cv2.error as e:
            from tkinter import messagebox
            messagebox.showerror("Error", f"Could not load cascade or classifier files.\nMake sure 'haarcascade_frontalface_default.xml' and 'classifier.xml' are in the correct folder.\n\nDetails: {e}", parent=self.root)
            return
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Error", f"An unexpected error occurred loading model: {e}", parent=self.root)
            return

        videoCap = cv2.VideoCapture(0)
        if not videoCap.isOpened():
             from tkinter import messagebox
             messagebox.showerror("Webcam Error", "Could not open webcam.", parent=self.root)
             return

        while True:
            ret, img = videoCap.read()
            if not ret:
                break
                
            img = recognize(img, clf, face_cascade)
            cv2.imshow("Face Detector (Press Enter to close)", img)

            if cv2.waitKey(1) == 13: # 13 is the Enter key
                break
                
        videoCap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition(root)
    root.mainloop()