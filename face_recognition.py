from tkinter import *
from PIL import Image, ImageTk
import cv2
import mysql.connector
from datetime import datetime
import os # Import os for file existence check
from tkinter import messagebox # Import messagebox explicitly

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
        bg_img = Label(self.root, bg=self.bg_color)
        bg_img.place(x=0, y=45, width=1530, height=790-45)

        # === 3. MODERN, COMBINED BUTTON ===
        try:
            # Ensure the image path is correct relative to where the script is run
            img_path = os.path.join("images", "png-clipart-facial-recognition-system-face-detection-pattern-recognition-fingerprint-face-face-people-thumbnail.png")
            if os.path.exists(img_path):
                 img_btn = Image.open(img_path)
                 img_btn = img_btn.resize((180, 180), Image.BILINEAR)
                 self.photo_btn = ImageTk.PhotoImage(img_btn)
            else:
                 print(f"Warning: Button image not found at {img_path}")
                 self.photo_btn = None # Set to None if image not found

            b1_1 = Button(bg_img,
                          text="Face Detector",
                          command=self.face_recog,
                          image=self.photo_btn if self.photo_btn else None, # Use image only if loaded
                          compound=TOP if self.photo_btn else None, # Compound only if image exists
                          font=self.button_font,
                          bg=self.frame_color,
                          fg=self.text_color,
                          cursor="hand2",
                          relief=RIDGE,
                          borderwidth=2,
                          pady=15 # Add padding
                         )
            # Place the button in the center
            b1_1.place(relx=0.5, rely=0.4, anchor=CENTER, width=280, height=280 if self.photo_btn else 100) # Adjust height based on image

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
    # === MODIFIED to check ID, Date, AND Minute for duplicates + Add Headers ===
    def mark_attendance(self, i, r, n):
        already_marked_this_minute = False
        now = datetime.now()
        d1 = now.strftime("%d/%m/%Y")
        dtMinute = now.strftime("%H:%M") # Get time down to the minute

        try:
            # === FIX: Check if file exists. If not, create it with headers ===
            if not os.path.exists("attendance.csv"):
                 with open("attendance.csv", "w", encoding='utf-8') as f:
                     # === FIX: Added column headers ===
                     f.write("ID,Role_Placeholder,Name,Time,Date,Status\n") # Add newline for header

            with open("attendance.csv", "r+", encoding='utf-8') as f:
                myDataList = f.readlines() # Read all lines
                for line in myDataList[1:]: # Skip header row
                    try:
                        entry = line.strip().split(",")
                        if len(entry) >= 5: # Make sure line has enough columns
                            existing_id = entry[0].strip()
                            existing_time_full = entry[3].strip()
                            existing_date = entry[4].strip()

                            # Extract HH:MM from the full timestamp
                            try:
                                existing_dt = datetime.strptime(existing_time_full, "%H:%M:%S")
                                existing_minute = existing_dt.strftime("%H:%M")
                            except ValueError:
                                existing_minute = ""

                            # Check if ID, Date, and Minute match
                            if existing_id == str(i) and existing_date == d1 and existing_minute == dtMinute:
                                already_marked_this_minute = True
                                break
                    except IndexError:
                        print(f"Skipping malformed line in attendance.csv: {line.strip()}")
                        continue 

            if not already_marked_this_minute:
                with open("attendance.csv", "a", encoding='utf-8') as f:
                    dtString = now.strftime("%H:%M:%S") # Full time for writing
                    f.write(f"{i},{r},{n},{dtString},{d1},Present\n") # Use \n for newline

        except Exception as es:
            print(f"Error in mark_attendance: {es}")


    # =================face recognition==================
    def face_recog(self):
        marked_this_minute_session = set()
        last_check_minute = ""
        window_name = "Face Detector (Press Enter or Close Window)" # Define window name

        videoCap = None # Initialize videoCap to None

        try: # Main try block for resource loading
            face_cascade_path = "haarcascade_frontalface_default.xml"
            classifier_path = "classifier.xml"
            if not os.path.exists(face_cascade_path) or not os.path.exists(classifier_path):
                 messagebox.showerror("File Not Found", f"Could not find required model files:\n{face_cascade_path}\n{classifier_path}\nPlease ensure they are in the project folder.", parent=self.root)
                 return

            face_cascade = cv2.CascadeClassifier(face_cascade_path)
            clf = cv2.face.LBPHFaceRecognizer_create()
            clf.read(classifier_path)

        except cv2.error as e:
            messagebox.showerror("OpenCV Error", f"Could not load cascade or classifier files.\nError: {e}", parent=self.root)
            return
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred loading model: {e}", parent=self.root)
            return

        try: # Try block for camera and main loop
            videoCap = cv2.VideoCapture(0)
            if not videoCap.isOpened():
                 messagebox.showerror("Webcam Error", "Could not open webcam.", parent=self.root)
                 return

            while True:
                ret, img = videoCap.read()
                if not ret:
                    print("Error: Failed to read frame from webcam.")
                    break

                # --- Recognition Logic ---
                gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                features = face_cascade.detectMultiScale(gray_image, 1.1, 10, minSize=(100, 100))

                current_minute = datetime.now().strftime("%H:%M")
                if current_minute != last_check_minute:
                    marked_this_minute_session.clear()
                    last_check_minute = current_minute

                for (x, y, w, h) in features:
                    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    face_roi_gray = gray_image[y:y+h, x:x+w]

                    # --- Prediction ---
                    id_, predict = clf.predict(face_roi_gray)
                    confidence = int((100 * (1 - predict / 300)))

                    n, role, i = "Unknown", "Unknown", str(id_) # Default values

                    if confidence > 77:
                        # --- Database Lookup ---
                        try:
                            conn = mysql.connector.connect(user='root', password='vedant29@3', host='localhost', database='face_recognizer', port=3306, connect_timeout=1)
                            cursor = conn.cursor()
                            cursor.execute("SELECT Name, course, Student_ID FROM student WHERE Student_ID=%s", (str(id_),))
                            result = cursor.fetchone()
                            conn.close()

                            if result:
                                # === FIX: Extract clean string from tuple ===
                                n = str(result[0])
                                role = str(result[1]) if result[1] else "N/A"
                                i = str(result[2])
                            else:
                                n = "Not Found" # ID recognized but not in DB

                        except mysql.connector.Error as err:
                            print(f"Database Error: {err}")
                            n, role = "DB Error", "DB Error"
                        except Exception as e:
                            print(f"Error fetching DB data: {e}")
                            n, role = "Error", "Error"

                        # --- Display Info & Mark Attendance ---
                        cv2.putText(img, f"ID: {i}", (x, y-55), cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 255, 255), 1)
                        cv2.putText(img, f"Name: {n}", (x, y-35), cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 255, 255), 1)
                        cv2.putText(img, f"Role: {role}", (x, y-15), cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 255, 255), 1)

                        # === FIX: Check session cache to stop race condition ===
                        if i not in marked_this_minute_session and n != "DB Error" and n != "Error" and n != "Not Found":
                            self.mark_attendance(i, "N/A", n)
                            marked_this_minute_session.add(i)
                    else:
                        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
                        cv2.putText(img, "Unknown Face", (x, y-15), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 1)

                # --- Show Frame ---
                cv2.imshow(window_name, img)

                # --- Check for Exit Keys/Events ---
                key = cv2.waitKey(1) & 0xFF
                if key == 13: # Enter key
                    break

                # === FIX: Check if window was closed ===
                try:
                    if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
                        break
                except cv2.error:
                     break
                # === END FIX ===

        except Exception as e:
            print(f"Error during face recognition loop: {e}")
            messagebox.showerror("Runtime Error", f"An error occurred during face recognition:\n{e}", parent=self.root)
        
        finally: # === FIX: Ensure cleanup happens ===
            if videoCap is not None and videoCap.isOpened():
                videoCap.release()
            cv2.destroyAllWindows()
            print("Webcam released and windows closed.")
            self.root.focus_force()
            # === END FIX ===


if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition(root)
    root.mainloop()

