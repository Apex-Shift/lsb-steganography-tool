import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

def embed_image(original_path, secret_path, output_path):
    original = Image.open(original_path)
    secret = Image.open(secret_path)

    # Resize secret image to fit into original image
    secret = secret.resize(original.size)

    # Convert images to RGB
    original = original.convert("RGB")
    secret = secret.convert("RGB")

    # Embed the secret image into the original image
    width, height = original.size
    for x in range(width):
        for y in range(height):
            original_pixel = list(original.getpixel((x, y)))
            secret_pixel = list(secret.getpixel((x, y)))

            # Modify the least significant bit of the original pixel
            original_pixel[0] = (original_pixel[0] & ~1) | (secret_pixel[0] >> 7)
            original_pixel[1] = (original_pixel[1] & ~1) | (secret_pixel[1] >> 7)
            original_pixel[2] = (original_pixel[2] & ~1) | (secret_pixel[2] >> 7)

            original.putpixel((x, y), tuple(original_pixel))

    original.save(output_path)
    messagebox.showinfo("Success", "Image embedded successfully!")

def unhide_image(original_path, output_path):
    original = Image.open(original_path)
    width, height = original.size

    # Create a new image for the hidden image
    hidden_image = Image.new("RGB", (width, height))

    for x in range(width):
        for y in range(height):
            original_pixel = list(original.getpixel((x, y)))

            # Extract the least significant bit
            hidden_pixel = [
                (original_pixel[0] & 1) * 255,
                (original_pixel[1] & 1) * 255,
                (original_pixel[2] & 1) * 255
            ]

            hidden_image.putpixel((x, y), tuple(hidden_pixel))

    hidden_image.save(output_path)
    messagebox.showinfo("Success", "Image unhidden successfully!")

def select_original_embed():
    path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
    original_embed_entry.delete(0, tk.END)
    original_embed_entry.insert(0, path)

def select_secret():
    path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
    secret_entry.delete(0, tk.END)
    secret_entry.insert(0, path)

def select_output_embed():
    path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    output_embed_entry.delete(0, tk.END)
    output_embed_entry.insert(0, path)

def select_original_unhide():
    path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
    original_unhide_entry.delete(0, tk.END)
    original_unhide_entry.insert(0, path)

def select_output_unhide():
    path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    output_unhide_entry.delete(0, tk.END)
    output_unhide_entry.insert(0, path)

def embed():
    embed_image(original_embed_entry.get(), secret_entry.get(), output_embed_entry.get())

def unhide():
    unhide_image(original_unhide_entry.get(), output_unhide_entry.get())

# Create the main window
root = tk.Tk()
root.title("Image Steganography")
root.maxsize(1200, 160)
root.resizable(False, False)
root.configure(bg="#CA6666")  # Set the background color of the root window

# Frame for embedding images
embed_frame = tk.Frame(root, padx=10, pady=10, bg="#CA6666")  # Set frame background color
embed_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

tk.Label(embed_frame, text="Embed Hidden Image", bg="#CA6666").grid(row=0, column=0, columnspan=3)

tk.Label(embed_frame, text="Original Image Path:", bg="#CA6666").grid(row=1, column=0)
original_embed_entry = tk.Entry(embed_frame, width=50)
original_embed_entry.grid(row=1, column=1)
tk.Button(embed_frame, text="Browse", bg="lightblue", fg="black", command=select_original_embed).grid(row=1, column=2)

tk.Label(embed_frame, text="Secret Image Path:", bg="#CA6666").grid(row=2, column=0)
secret_entry = tk.Entry(embed_frame, width=50)
secret_entry.grid(row=2, column=1)
tk.Button(embed_frame, text="Browse", bg="lightblue", fg="black", command=select_secret).grid(row=2, column=2)

tk.Label(embed_frame, text="Output Embedded Image Path:", bg="#CA6666").grid(row=3, column=0)
output_embed_entry = tk.Entry(embed_frame, width=50)
output_embed_entry.grid(row=3, column=1)
tk.Button(embed_frame, text="Browse", bg="lightblue", fg="black", command=select_output_embed).grid(row=3, column=2)

tk.Button(embed_frame, text="Embed Image", bg="lightblue", fg="black", command=embed).grid(row=4, column=1)

# Frame for un-hiding images
unhide_frame = tk.Frame(root, padx=10, pady=10, bg="#CA6666")  # Set frame background color
unhide_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

tk.Label(unhide_frame, text="Unhide Hidden Image", bg="#CA6666").grid(row=0, column=0, columnspan=3)

tk.Label(unhide_frame, text="Original Image Path:", bg="#CA6666").grid(row=1, column=0)
original_unhide_entry = tk.Entry(unhide_frame, width=50)
original_unhide_entry.grid(row=1, column=1)
tk.Button(unhide_frame, text="Browse", bg="lightblue", fg="black", command=select_original_unhide).grid(row=1, column=2)

tk.Label(unhide_frame, text="Output Unhidden Image Path:", bg="#CA6666").grid(row=2, column=0)
output_unhide_entry = tk.Entry(unhide_frame, width=50)
output_unhide_entry.grid(row=2, column=1)
tk.Button(unhide_frame, text="Browse", bg="lightblue", fg="black", command=select_output_unhide).grid(row=2, column=2)

tk.Button(unhide_frame, text="Unhide Image", bg="lightblue", fg="black", command=unhide).grid(row=3, column=1)

# Start the GUI event loop
root.mainloop()