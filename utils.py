from PIL import Image, ImageTk


def resize_icon(icon_path, width, height):
    # Open the image using PIL
    img = Image.open(icon_path)
    # Resize the image
    resized_img = img.resize((width, height), Image.LANCZOS)
    # Convert the resized image to a PhotoImage object
    resized_icon = ImageTk.PhotoImage(resized_img)
    # Return the resized icon
    return resized_icon
