import cv2
from tkinter import *
from tkinter.filedialog import askopenfilename

class Demo:

    def __init__(self, root):
        self.menubar = Menu(root)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Photo", command=self.photo_selected)
        self.filemenu.add_command(label="Video", command=self.video_selected)
        self.filemenu.add_command(label="Web Cam", command=self.web_cam_selected)
        self.menubar.add_cascade(label="File", menu=self.filemenu)


        root.config(menu=self.menubar)
        self.tkvar = StringVar(root)

        obj_data = ["Eyes", "Face",]

        self.object = cv2.CascadeClassifier(obj_data[1])
        popupMenu = OptionMenu(root, self.tkvar, *obj_data, )
        self.tkvar.trace('w', self.value_changed)
        self.tkvar.set('Face')
        Label(root, text="Choose what to detect").grid(row=0, column=0)
        popupMenu.grid(row=1, column=0)

    def photo_selected(self):
        photo_path = askopenfilename(filetypes=[("Image File",'.jpg')])
        img = cv2.imread(photo_path)
        self.detect_face(img)


    def value_changed(self, *args):
        self.object = cv2.CascadeClassifier(self.tkvar.get()+".xml")

    def video_selected(self):
        video_path = askopenfilename(filetypes=[("Video File", '.mp4')])
        self.detect_from_video(video_path)


    def web_cam_selected(self):
        self.detect_from_video(0)


    def detect_from_video(self, path):
        webcam = cv2.VideoCapture(path)
        while True:
            succes_frame, frame = webcam.read()
            self.detect_face(frame)
            key = cv2.waitKey(1)
            if key == ord('q'):
                break
        webcam.release()
        cv2.destroyAllWindows()



    def detect_face(self, img):
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face = self.object.detectMultiScale(gray_img)
        for (x, y, w, h) in face:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.imshow("opencv demo", img)



r = Tk()
r.geometry("300x300")
demo = Demo(r)
r.mainloop()



