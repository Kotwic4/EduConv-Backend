from PIL import Image
def generate_8bit_bitmap(width, height, RGB_list):
    image = Image.new('L',(width,height))
    pixels = image.load()
    for i in range(width):
        for j in range(height):
            image.putpixel((i,j),int(255*RGB_list[j*width+i]))
    return image
