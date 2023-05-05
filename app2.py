from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image
from pathlib import Path
import os



class App():

    def __init__(self):
        # Creating the main window
        self.root = Tk()
        self.root.title("WaterMarkingApp")
        self.root.geometry("1600x900")
        self.root.configure(
            bg="#F1EEE9", width=100, highlightthickness=0
        )

        # Creating the buttons frame
        frm1 = ttk.Frame(self.root, padding=10)
        frm1.grid(column=0, row=0, padx=0)
        frm1.grid()
        # frm1.configure(width=300, height=1500)

        # Creating the images Frame
        frm2 = ttk.Frame(self.root)
        frm2.grid(column=1, row=0, padx=10, pady=0)
        frm2.grid()

        # Creating the canvas that will hold the image

        self.canvas = Canvas(frm2, width=800, height=800, bg="#bdc3c7")
        self.canvas.grid(column=0, row=0, padx=30, pady=30, ipadx=30, ipady=30)
        self.none_image = self.canvas.create_image(460, 460, image=None)

        # Creating the buttons to upload the images

        self.main_image_upload_button = ttk.Button(frm1, text='Upload Image', command=self.get_main_image, width=30, padding=10)
        self.main_image_upload_button.grid(column=0, row=0)

        self.watermark_upload_button = ttk.Button(frm1, text="Upload Watermark", command=self.upload_water_mark, width=30, padding=10)
        self.watermark_upload_button.grid(column=0, row=1)

        self.merge_button = ttk.Button(frm1, text="merge",
                                       command=lambda: self.merge(self.main_image_object, self.watermark_object), width=30, padding=10)
        self.merge_button.grid(column=0, row=2)

        self.download_button = ttk.Button(frm1, text='Download', command=self.download, width=30, padding=10)
        self.download_button.grid(column=0, row=3)

        self.download_button = ttk.Button(frm1, text='Reset', command=self.reset, width=30, padding=10)
        self.download_button.grid(column=0, row=4)

        # Declaring the images variables
        p = Path("_")
        self.w = p
        self.watermark_tk = None
        self.watermark_object = None
        self.watermark_image = None
        self.main_image_object = None
        self.merged_image = None

        # Binding and images movement code
        # self.canvas.bind("<B1-Motion>", self.move)
        self.canvas.bind('<Motion>', self.position)
        self.flag = False
        self.root.mainloop()

        # ----------------------------------------------Defining Methods----------------------------------------------#

    def get_main_image(self):
        """ when pressed on the button, the function opens a file to upload the image """
        """ Image gets opened into an Image object"""
        """ Image gets resized into a 800*800"""
        """ Image gets converted into a TK image"""
        """ Canvas is asked to display the image """
        """ returns an image object"""

        image_file = filedialog.askopenfilename()
        with Image.open(image_file) as imgobj:
            resized_image = imgobj.resize((800, 800))
        image = ImageTk.PhotoImage(resized_image)
        label = Label(image=image)
        label.image = image  # keep a reference to prevent garbage collection!
        self.canvas.itemconfig(self.none_image, image=image)
        self.main_image_object = imgobj

    # def upload_water_mark(self):
    #     """ uploads a watermark image"""
    #
    #     watermark_file = filedialog.askopenfilename()
    #     with Image.open(watermark_file) as watermark_obj:
    #         resized_image = watermark_obj.resize((400, 400))
    #     watermark = ImageTk.PhotoImage(resized_image)
    #     label = Label(image=watermark)
    #     label.image = watermark
    #     self.watermark_tk = watermark
    #     self.watermark_image = self.canvas.create_image(400, 400, image=watermark, tags="watermark_tag")
    #     self.watermark_object = watermark_obj
    #     self.w = watermark_file


    def upload_water_mark(self):
        """ uploads a watermark image"""

        watermark_file = filedialog.askopenfilename()
        with Image.open(watermark_file) as watermark_obj:
            resized_image = watermark_obj.resize((400, 400))
        watermark = ImageTk.PhotoImage(resized_image)
        label = Label(image=watermark)
        label.image = watermark
        self.watermark_tk = watermark
        self.watermark_label = ttk.Label(self.root, image=self.watermark_tk)
        self.watermark_label.grid(column=1,row=0)
        self.watermark_object = watermark_obj
        self.w = watermark_file



    def merge(self, im1, im2):
        coords = self.canvas.coords('watermark_tag')
        resized_im1 = im1.resize((800, 800))
        im2_tk = ImageTk.PhotoImage(im2)
        top_corner = (int(coords[0] - im2_tk.width() / 2), int(coords[1] - im2_tk.height() / 2))
        self.canvas.unbind("<B1-Motion>")
        resized_im1.paste(im2, top_corner)
        merged_tk_image = ImageTk.PhotoImage(resized_im1)

        label = Label(image=merged_tk_image)
        label.image = merged_tk_image  # keep a reference to prevent garbage collection!

        self.canvas.delete("watermark_tag")
        self.canvas.itemconfig(self.none_image, image=merged_tk_image)
        self.main_image_object = resized_im1

    def download(self):
        """ Downloads the merged image"""
        file = filedialog.asksaveasfile(mode='w', defaultextension=".png",
                                        filetypes=(("PNG file", "*.png"), ("All Files", "*.*")))
        if file:
            abs_path = os.path.abspath(file.name)
            try:
                self.main_image_object.save(fp=abs_path)  # saves the image to the input file name.
            except AttributeError:
                print("upload image first")

    def move(self, e):
        """ binds the watermark image to the mouse movements"""

        try:
            self.canvas.coords("watermark_tag", e.x, e.y)
        except:
            self.watermark_image = ImageTk.PhotoImage(Image.open(self.w))
            self.canvas.delete(self.watermark_image)
            self.watermark_image = ImageTk.PhotoImage(Image.open(self.w))
            self.canvas.create_image(e.x, e.y, image=self.watermark_image, tags="watermark_tag")

    def position(self, event):
        self.dimentions = (self.watermark_tk.width(), self.watermark_tk.height())
        self.x, self.y = event.x, event.y

        # coords = self.canvas.coords('watermark_tag')

        x_edge = self.watermark_tk.width() / 2
        y_edge = self.watermark_tk.height() / 2
        print(f"dimensiton:{self.dimentions} \nself.x: {self.x}  \nself.y {self.y} \n\n x edge:{x_edge}\n  y edge: {y_edge} ")
        print(self.watermark_label.winfo_x(), self.watermark_label.winfo_y())

        if (
                self.x in range(int(x_edge) - 20, int(x_edge) + 20, 1) and
                self.x in range(int(y_edge) - 20, int(y_edge) + 20, 1)
        ):
            self.canvas.config(cursor='sizing')
            self.canvas.bind('<ButtonRelease-1>', self.end)
            self.canvas.bind('<Button-1>', self.start)

    def end(self, event):
        self.flag = True
        self.canvas.unbind('<ButtonRelease-1>')

    def start(self, event):
        self.flag = False
        self.resize()

    def resize(self):
        if not self.flag:
            self.canvas.config(cursor='sizing')
            try:
                resdized = ImageTk.PhotoImage(self.watermark_object.resize((self.x, self.y), Image.ANTIALIAS))
                self.watermark_tk = resdized
            except:
                pass
            self.watermark_object = self.watermark_object.resize((self.x, self.y), Image.ANTIALIAS)
            self.canvas.itemconfig(self.watermark_image, image=resdized)
            self.canvas.create_image(400, 400, resdized)
            self.canvas.update()
            self.canvas.after(1, self.resize)

    def reset(self):
        self.root.destroy()
        App()





if __name__ == "__main__":
    app = App()
