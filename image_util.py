from PIL import Image
def generate_8bit_gray_bitmap(width, height, RGB_list):
    image = Image.new('L',(width,height))
    for i in range(width):
        for j in range(height):
            image.putpixel((i,j),int(255*RGB_list[j*width+i]))
    return image

def generate_24bit_color_bitmap(width, height, RGB_list):
    image = Image.fromarray(RGB_list,'RGB')
    # image.show()
    # image = Image.new('RGB', (width, height))
    # for i in range(width):
    #     for j in range(height):
    #         image.putpixel((i, j), int(255 * RGB_list[j * width + i]))
    return image
