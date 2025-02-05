import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk, ImageOps, ImageDraw, ImageFont, ImageEnhance


class ImageEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Image Editor")
        self.root.geometry("900x700")
        self.image = None
        self.edited_image = None

        # UI Layout
        self.create_ui()

    def create_ui(self):
        # Toolbar Frame
        toolbar = tk.Frame(self.root, bg="#ececec", relief=tk.RAISED, bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Buttons in Toolbar
        tk.Button(toolbar, text="Open", command=self.open_image, bg="#d9d9d9", padx=10).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(toolbar, text="Save", command=self.save_image, bg="#d9d9d9", padx=10).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(toolbar, text="Rotate 90°", command=self.rotate_image, bg="#d9d9d9", padx=10).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(toolbar, text="Flip Horizontal", command=self.flip_horizontal, bg="#d9d9d9", padx=10).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(toolbar, text="Flip Vertical", command=self.flip_vertical, bg="#d9d9d9", padx=10).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(toolbar, text="Grayscale", command=self.to_grayscale, bg="#d9d9d9", padx=10).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(toolbar, text="Add Text", command=self.add_text, bg="#d9d9d9", padx=10).pack(side=tk.LEFT, padx=5, pady=5)
        
        # Frame for canvas and control panel
        content_frame = tk.Frame(self.root)
        content_frame.pack(fill=tk.BOTH, expand=True)

        import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk, ImageEnhance

class ImageEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Image Editor")
        self.root.geometry("900x700")
        self.image = None
        self.edited_image = None

        # Main layout frames
        self.create_ui()

    def create_ui(self):
        # Toolbar Frame
        toolbar = tk.Frame(self.root, bg="#ececec", relief=tk.RAISED, bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Buttons in Toolbar
        tk.Button(toolbar, text="Open", command=self.open_image, fg="white",bg="orange", padx=10,font=("Arial",20,"bold")).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(toolbar, text="Save", command=self.save_image, bg="light gray", padx=10).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(toolbar, text="Rotate 90°", command=self.rotate_image, bg="#d9d9d9", padx=10).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(toolbar, text="Flip Horizontally", command=self.flip_horizontal, bg="#d9d9d9", padx=10).pack(side=tk.LEFT,padx=5,pady=5)
        tk.Button(toolbar, text="Flip Vertically", command=self.flip_vertical, bg="#d9d9d9", padx=10).pack(side=tk.LEFT,padx=5,pady=5)
        tk.Button(toolbar, text="GrayScale", command=self.to_grayscale, bg="#d9d9d9", padx=10).pack(side=tk.LEFT,padx=5,pady=5)
        
        # Frame for canvas and control panel
        content_frame = tk.Frame(self.root)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Canvas for displaying the image
        self.canvas = tk.Canvas(content_frame, bg="light blue")
        self.canvas.pack(fill=tk.BOTH, expand=True, side=tk.TOP)

        # Control Panel for Brightness & Contrast
        control_panel = tk.Frame(content_frame, bg="light green", relief=tk.RAISED, bd=2)
        control_panel.pack(side=tk.BOTTOM, fill=tk.X)

        tk.Label(control_panel, text="Brightness:", bg="#ececec").pack(side=tk.LEFT, padx=5)
        self.brightness_scale = ttk.Scale(
            control_panel, from_=0.5, to=2.0, orient=tk.HORIZONTAL, value=1.0, command=self.adjust_brightness
        )
        self.brightness_scale.pack(side=tk.LEFT, padx=5)

        tk.Label(control_panel, text="Contrast:", bg="#ececec").pack(side=tk.LEFT, padx=5)
        self.contrast_scale = ttk.Scale(
            control_panel, from_=0.5, to=2.0, orient=tk.HORIZONTAL, value=1.0, command=self.adjust_contrast
        )
        self.contrast_scale.pack(side=tk.LEFT, padx=5)


    def open_image(self):
        filetypes = [("Image Files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        filepath = filedialog.askopenfilename(filetypes=filetypes)
        if filepath:
            self.image = Image.open(filepath)
            self.edited_image = self.image.copy()
            self.display_image(self.image)


    def save_image(self):
        if self.edited_image:
            filepath = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg *.jpeg"), ("All Files", "*.*")]
            )
            if filepath:
                self.edited_image.save(filepath)
                messagebox.showinfo("Success", "Image saved successfully!")
        else:
            messagebox.showerror("Error", "No image to save!")

    def adjust_brightness(self, value):
        if self.image:
            enhancer = ImageEnhance.Brightness(self.image)
            self.edited_image = enhancer.enhance(float(value))
            self.display_image(self.edited_image)

    def adjust_contrast(self, value):
        if self.image:
            enhancer = ImageEnhance.Contrast(self.image)
            self.edited_image = enhancer.enhance(float(value))
            self.display_image(self.edited_image)

    def rotate_image(self):
        if self.image:
            self.edited_image = self.edited_image.rotate(90, expand=True)
            self.display_image(self.edited_image)
        else:
            messagebox.showerror("Error", "Open an image first!")

    def flip_horizontal(self):
        if self.image:
            self.edited_image = ImageOps.mirror(self.edited_image)
            self.display_image(self.edited_image)
        else:
            messagebox.showerror("Error", "Open an image first!")

    def flip_vertical(self):
        if self.image:
            self.edited_image = ImageOps.flip(self.edited_image)
            self.display_image(self.edited_image)
        else:
            messagebox.showerror("Error", "Open an image first!")

    def to_grayscale(self):
        if self.image:
            self.edited_image = ImageOps.grayscale(self.edited_image)
            self.display_image(self.edited_image)
        else:
            messagebox.showerror("Error", "Open an image first!")

    def add_text(self):
        if self.image:
            text = tk.simpledialog.askstring("Input", "Enter the text to add:")
            if text:
                draw = ImageDraw.Draw(self.edited_image)
                font = ImageFont.load_default()
                draw.text((50, 50), text, fill="red", font=font)
                self.display_image(self.edited_image)
        else:
            messagebox.showerror("Error", "Open an image first!")

    

    def display_image(self, image):
        self.canvas.delete("all")
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # Resize image to fit within the canvas
        image_ratio = image.width / image.height
        canvas_ratio = canvas_width / canvas_height

        if image_ratio > canvas_ratio:
            # Fit to canvas width
            new_width = canvas_width
            new_height = int(canvas_width / image_ratio)
        else:
            # Fit to canvas height
            new_height = canvas_height
            new_width = int(canvas_height * image_ratio)

        resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)
        self.tk_image = ImageTk.PhotoImage(resized_image)
        self.canvas.create_image(canvas_width // 2, canvas_height // 2, image=self.tk_image)


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    editor = ImageEditor(root)
    root.mainloop()
