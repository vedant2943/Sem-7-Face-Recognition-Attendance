from tkinter import*
from tkinter import ttk
import os
from PIL import Image,ImageTk
# from face_recognition import Face_Recognition


# from attendance import Attendance


class Developer:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

# This part is image labels setting start 
        # first header image  
        img=Image.open(r"images/facial-recognition-software_52683-104208.png")
        img=img.resize((1566,130),Image.BILINEAR)
        self.photoimg=ImageTk.PhotoImage(img)

        # set image as lable
        f_lb1 = Label(self.root,image=self.photoimg)
        f_lb1.place(x=0,y=0,width=1566,height=130)

        # backgorund image 
        bg1=Image.open(r"images/istockphoto-1459063664-612x612.jpg")
        bg1=bg1.resize((1566,768),Image.BILINEAR)
        self.photobg1=ImageTk.PhotoImage(bg1)

        # set image as lable
        bg_img = Label(self.root,image=self.photobg1)
        bg_img.place(x=0,y=130,width=1566,height=768)


        #title section
        title_lb1 = Label(bg_img,text="Developer Pannel",font=("verdana",30,"bold"),bg="white",fg="navyblue")
        title_lb1.place(x=0,y=0,width=1566,height=45)

        # Create buttons below the section 
        # ------------------------------------------------------------------------------------------------------------------- 
        # student button 1
        std_img_btn=Image.open(r"images/view-3d-man-using-laptop_23-2150709796.png")
        std_img_btn=std_img_btn.resize((180,180),Image.BILINEAR)
        self.std_img1=ImageTk.PhotoImage(std_img_btn)

        std_b1 = Button(bg_img,image=self.std_img1,cursor="hand2")
        std_b1.place(x=310,y=200,width=180,height=180)

        std_b1_1 = Button(bg_img,text="Prathmesh Bhoir",cursor="hand2",font=("tahoma",15,"bold"),bg="white",fg="navyblue")
        std_b1_1.place(x=310,y=380,width=180,height=45)

        # Detect Face  button 2
        det_img_btn=Image.open(r"images/A determined individual.jpeg")
        det_img_btn=det_img_btn.resize((180,180),Image.BILINEAR)
        self.det_img1=ImageTk.PhotoImage(det_img_btn)

        det_b1 = Button(bg_img,image=self.det_img1,cursor="hand2",)
        det_b1.place(x=540,y=200,width=180,height=180)

        det_b1_1 = Button(bg_img,text="Abhishek Barote",cursor="hand2",font=("tahoma",15,"bold"),bg="white",fg="navyblue")
        det_b1_1.place(x=540,y=380,width=180,height=45)

         # Attendance System  button 3
        att_img_btn=Image.open(r"images/232f11d7a5ed6cf2061a0cd20ad2377c.jpg")
        att_img_btn=att_img_btn.resize((180,180),Image.BILINEAR)
        self.att_img1=ImageTk.PhotoImage(att_img_btn)

        att_b1 = Button(bg_img,image=self.att_img1,cursor="hand2",)
        att_b1.place(x=770,y=200,width=180,height=180)

        att_b1_1 = Button(bg_img,text="Paras Adkurkar",cursor="hand2",font=("tahoma",15,"bold"),bg="white",fg="navyblue")
        att_b1_1.place(x=770,y=380,width=180,height=45)

         # Help  Support  button 4
        hlp_img_btn=Image.open(r"images/view-3d-man-using-laptop_23-2150709796.png")
        hlp_img_btn=hlp_img_btn.resize((180,180),Image.BILINEAR)
        self.hlp_img1=ImageTk.PhotoImage(hlp_img_btn)

        hlp_b1 = Button(bg_img,image=self.hlp_img1,cursor="hand2",)
        hlp_b1.place(x=1000,y=200,width=180,height=180)

        hlp_b1_1 = Button(bg_img,text="Shreeyash Jadhav",cursor="hand2",font=("tahoma",15,"bold"),bg="white",fg="navyblue")
        hlp_b1_1.place(x=1000,y=380,width=180,height=45)




if __name__ == "__main__":
    root=Tk()
    obj=Developer(root)
    root.mainloop()