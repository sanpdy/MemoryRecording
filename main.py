import tkinter as tk
from PIL import Image, ImageTk
import sv_ttk
from record import Record, record_main  # Ensure these are correctly defined
import random
from threading import Thread

class ImageDisplayApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Display")

        window_width = 800
        window_height = 600
        self.root.geometry(f"{window_width}x{window_height}")
        self.images = ["dog.png", "cat.png", "bird.png"]
        self.preload_images()
        self.current_image_index = 0
        self.displayed_images = []
        self.score = 0
        self.scored = False  # Flag to track if the score has been awarded

        self.img_label = tk.Label(root)
        self.img_label.pack(expand=True)

        self.score_label = tk.Label(root, text=f"Score: {self.score}", font=("Arial", 16))
        self.score_label.pack_forget()

        self.root.bind("<space>", self.check_repeat_image)  # Bind the space bar key

        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.root.winfo_width() // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.root.winfo_height() // 2)
        self.root.geometry(f"+{x}+{y}")
        self.start_time = None
        self.countdown()

    def preload_images(self):
        self.preloaded_images = {}
        for img_name in self.images:
            img_path = 'images/' + img_name
            original_img = Image.open(img_path)
            resized_img = original_img.resize((200, 200))
            self.preloaded_images[img_name] = ImageTk.PhotoImage(resized_img)

    def countdown(self):
        def decrement(count):
            label['text'] = count
            if count > 0:
                self.root.after(1000, decrement, count-1)
            if count == 0:
                label.destroy()
                self.start_image_display_recordings()

        label = tk.Label(self.root)
        label.config(font=('Helvetica bold', 35))
        label.place(x=400, y=275)
        decrement(2)

    def start_image_display_recordings(self):
        record_duration_s = 30
        thread = Thread(target=record_main, args=(record_duration_s,))
        thread.start()
        self.start_time = self.root.winfo_toplevel().tk.call('clock', 'seconds')
        self.score_label.pack()
        self.update_image()

    def update_image(self):
        current_time = self.root.winfo_toplevel().tk.call('clock', 'seconds')
        elapsed_time = current_time - self.start_time
        if elapsed_time < 30:
            img_index = random.randint(0, len(self.images) - 1)
            img_name = self.images[img_index]
            img = self.preloaded_images[img_name]
            self.img_label.config(image=img)
            self.img_label.image = img

            self.displayed_images.append(img_name)
            if len(self.displayed_images) > 3:
                self.displayed_images.pop(0)

            self.scored = False
            self.root.after(1000, self.update_image)
        else:
            self.img_label.config(image='')
            label = tk.Label(self.root, text='Well done. You have completed the task!')
            label.config(font=('Helvetica bold', 35))
            label.place(x=50, y=275)

    def check_repeat_image(self, event):
        if not self.scored and len(self.displayed_images) >= 3:
            if self.displayed_images[-1] == self.displayed_images[-3]:
                self.score += 1
                self.score_label.config(text=f"Score: {self.score}")
                self.scored = True

def main():
    root = tk.Tk()
    app = ImageDisplayApp(root)
    sv_ttk.set_theme("dark")
    root.mainloop()

if __name__ == "__main__":
    main()
