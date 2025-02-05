import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, colorchooser 
from tkinter.colorchooser import askcolor
from tkinter import ttk
from PIL import Image, ImageTk, ImageOps, ImageDraw, ImageFont, ImageEnhance
import ttkbootstrap as tb


class ImageEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("EditPro")
        self.root.geometry("900x700")
        self.image = None
        self.edited_image = None
        self.history = []  # Stack for undo functionality
        self.text_color = "red"

        self.zoom_factor = 1.0  # Zoom level

        # Cropping variables
        self.crop_start_x = None
        self.crop_start_y = None
        self.crop_end_x = None
        self.crop_end_y = None
        self.cropping = False


        # Main layout frames
        self.create_ui()

    def create_ui(self):
        # Toolbar Frame
        toolbar = tk.Frame(self.root, bg="#ececec", relief=tk.RAISED, bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Buttons in Toolbar
        ttk.Button(toolbar, text="Open", command=self.open_image).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(toolbar, text="Save", command=self.save_image).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(toolbar, text="Rotate 90°", command=self.rotate_image).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(toolbar, text="Flip Horizontally", command=self.flip_horizontal).grid(row=0, column=3, padx=5, pady=5)
        ttk.Button(toolbar, text="Flip Vertically", command=self.flip_vertical).grid(row=0, column=4, padx=5, pady=5)
        ttk.Button(toolbar, text="GrayScale", command=self.to_grayscale).grid(row=0, column=5, padx=5, pady=5)
        ttk.Button(toolbar, text="Add Text", command=self.add_text).grid(row=0, column=6, padx=5, pady=5)
        ttk.Button(toolbar, text="Choose Text Color", command=self.choose_text_color).grid(row=0, column=7, padx=5, pady=5)
        ttk.Button(toolbar, text="Undo", command=self.undo).grid(row=0, column=8, padx=5, pady=5)
        ttk.Button(toolbar, text="Reset", command=self.reset_image).grid(row=0, column=9, padx=5, pady=5)
        ttk.Button(toolbar, text="Crop", command=self.activate_crop).grid(row=0, column=10, padx=5, pady=5)
       # ttk.Button(toolbar, text="Zoom In", command=self.zoom_in, bg="#d9d9d9", padx=10, font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=5, pady=5)
       # ttk.Button(toolbar, text="Zoom Out", command=self.zoom_out, bg="#d9d9d9", padx=10, font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=5, pady=5)
        # Frame for canvas and control panel
        content_frame = tk.Frame(self.root)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Canvas for displaying the image
        self.canvas = tk.Canvas(content_frame, bg="#f0f0f0", relief=tk.SUNKEN, bd=2)
        self.canvas.pack(fill=tk.BOTH, expand=True, side=tk.TOP)

        self.canvas.bind("<ButtonPress-1>", self.start_crop)
        self.canvas.bind("<B1-Motion>", self.show_crop_rectangle)
        self.canvas.bind("<ButtonRelease-1>", self.end_crop)
        

        # Control Panel for Brightness & Contrast
        control_panel = tk.Frame(content_frame, background="black", relief=tk.RAISED, bd=3,height= 40)
        control_panel.pack(side=tk.BOTTOM, fill=tk.X)
        
        style = ttk.Style()
        style.configure(
            "Custom.Horizontal.TScale",  # Custom style name
            troughcolor="red",       # Track background color
            sliderrelief="raised",       # Add a 3D effect to the slider button
            sliderthickness=30,   
            type="FLAT"       # Adjust the thickness of the slider button
        )
        tk.Label(control_panel, text="Brightness:", bg="#87CEEB",font=("bold")).pack(side=tk.LEFT, padx=5)
        self.brightness_scale = ttk.Scale(
            control_panel, from_=0.5, to=2.0, orient=tk.HORIZONTAL, value=1.0, command=self.adjust_brightness,
            length=  200, style="Custom.Horizontal.TScale"
            )
        
        
        self.brightness_scale.pack(side=tk.LEFT, padx=5)

        tk.Label(control_panel, text="Contrast:", bg="light grey", font=("bold")).pack(side=tk.LEFT, padx=5)
        self.contrast_scale = ttk.Scale(
            control_panel, from_=0.5, to=2.0, orient=tk.HORIZONTAL, value=1.0, command=self.adjust_contrast,
        length = 200
        )
        self.contrast_scale.pack(side=tk.LEFT, padx=5)

        
        zoom_in_button = ttk.Button(control_panel,
        text="+",
        bootstyle="success-outline",  # Green outline style
        command=self.zoom_in
        )
        zoom_in_button.pack(side=tk.RIGHT, padx=10)


        zoom_out_button = tb.Button(
            control_panel,
            text="-",
            bootstyle="danger-outline",  # Red outline style
            command=self.zoom_out
        )
        zoom_out_button.pack(side=tk.RIGHT, padx=5)

    def open_image(self):
        filetypes = [("Image Files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        filepath = filedialog.askopenfilename(filetypes=filetypes)
        if filepath:
            self.image = Image.open(filepath)
            self.edited_image = self.image.copy()
            self.history = [self.edited_image.copy()]  # Reset history
            self.display_image(self.image)

    def save_image(self):
        if self.edited_image:
            filepath = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg *.jpeg"), ("All Files", "*.*")],
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
            self.history.append(self.edited_image.copy())
            self.display_image(self.edited_image)


    def rotate_image(self):
        if self.image:
            self.edited_image = self.edited_image.rotate(90, expand=True)
            self.history.append(self.edited_image.copy())
            self.display_image(self.edited_image)
        else:
            messagebox.showerror("Error", "Open an image first!")

    def flip_horizontal(self):
        if self.image:
            self.edited_image = ImageOps.mirror(self.edited_image)
            self.history.append(self.edited_image.copy())
            self.display_image(self.edited_image)
        else:
            messagebox.showerror("Error", "Open an image first!")

    def flip_vertical(self):
        if self.image:
            self.edited_image = ImageOps.flip(self.edited_image)
            self.history.append(self.edited_image.copy())
            self.display_image(self.edited_image)
        else:
            messagebox.showerror("Error", "Open an image first!")

    def to_grayscale(self):
        if self.image:
            self.edited_image = ImageOps.grayscale(self.edited_image)
            self.history.append(self.edited_image.copy())
            self.display_image(self.edited_image)
        else:
            messagebox.showerror("Error", "Open an image first!")

    def add_text(self):

        if self.image:
            # Prompt the user for text
            text = simpledialog.askstring("Input", "Enter the text to add:")
            if text:
                font_size = int(self.edited_image.height * 0.05)  # 5% of image height
                if font_size < 10:
                    font_size = 20  # Minimum font size

                # Prompt the user to choose a color
                color = askcolor(title="Choose Text Color")[1]  # Get color in hex format
                if not color:
                    color = "red"  # Default to red if no color is selected

                # Load a font
                try:
                    font = ImageFont.truetype("arial.ttf", font_size)  # System font
                except IOError:
                    font = ImageFont.load_default()  # Default font fallback

                # Add text dynamically at the center of the image
                draw = ImageDraw.Draw(self.edited_image)
                text_width, text_height = draw.textsize(text, font=font)
                image_width, image_height = self.edited_image.size

                # Calculate centered position
                x = (image_width - text_width) // 2
                y = (image_height - text_height) // 2

                self.history.append(self.edited_image.copy())

                # Add text to the image
                draw.text((x, y), text, fill=color, font=font)

                # Display the updated image
                self.display_image(self.edited_image)
        else:
            messagebox.showerror("Error", "Open an image first!")

    def choose_text_color(self):
        color = colorchooser.askcolor(title="Choose Text Color")
        if color[1]:
            self.text_color = color[1]

    def undo(self):
        if len(self.history) > 1:  # Ensure there's a previous state
            self.history.pop()  # Remove the current state
            self.edited_image = self.history[-1].copy()  # Restore the previous state
            self.display_image(self.edited_image)
        else:
            messagebox.showinfo("Info", "No more actions to undo.")

    def reset_image(self):
        if self.image:
            self.edited_image = self.image.copy()
            self.history = [self.edited_image.copy()]  # Reset history to the default state
            self.display_image(self.edited_image)
        else:
            messagebox.showerror("Error", "Open an image first!")

    def zoom_in(self):

        if self.edited_image:
            width, height = self.edited_image.size
            new_width, new_height = int(width * 1.2), int(height * 1.2)  # Increase by 20%
            self.edited_image = self.edited_image.resize((new_width, new_height), Image.ANTIALIAS)
            self.history.append(self.edited_image.copy())  # Save state
            self.display_image(self.edited_image)
        else:
            messagebox.showerror("Error", "Open an image first!")

    def zoom_out(self):

        if self.edited_image:
            width, height = self.edited_image.size
            new_width, new_height = int(width * 0.8), int(height * 0.8)  # Decrease by 20%
            self.edited_image = self.edited_image.resize((new_width, new_height), Image.ANTIALIAS)
            self.history.append(self.edited_image.copy())  # Save state
            self.display_image(self.edited_image)
        else:
            messagebox.showerror("Error", "Open an image first!")

    def activate_crop(self):
        if self.edited_image:
            self.cropping = True
            messagebox.showinfo("Info", "Click and drag to select the area to crop.")
        else:
            messagebox.showerror("Error", "Open an image first!")

    def start_crop(self, event):
        if self.cropping:
            self.crop_start_x, self.crop_start_y = event.x, event.y

    def show_crop_rectangle(self, event):
        if self.cropping:
            self.canvas.delete("crop_rectangle")
            self.crop_end_x, self.crop_end_y = event.x, event.y
            self.canvas.create_rectangle(
                self.crop_start_x, self.crop_start_y, self.crop_end_x, self.crop_end_y, outline="red", tag="crop_rectangle"
            )

    def end_crop(self, event):
        if self.cropping:
            self.crop_end_x, self.crop_end_y = event.x, event.y
            self.cropping = False

            # Calculate cropping box
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            image_width, image_height = self.edited_image.size
            scale_x = image_width / canvas_width
            scale_y = image_height / canvas_height

            left = int(self.crop_start_x * scale_x)
            upper = int(self.crop_start_y * scale_y)
            right = int(self.crop_end_x * scale_x)
            lower = int(self.crop_end_y * scale_y)

            # Crop the image
            self.edited_image = self.edited_image.crop((left, upper, right, lower))
            self.history.append(self.edited_image.copy())  # Save state
            self.display_image(self.edited_image)

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

        resized_image = image.resize((new_width, new_height))
        self.tk_image = ImageTk.PhotoImage(resized_image)
        self.canvas.create_image(canvas_width // 2, canvas_height // 2, image=self.tk_image)


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    editor = ImageEditor(root)
    root.mainloop()
