from PIL import Image
import CommonLib.Common as common
nowdate = common.Regexp_OnlyNumberbyDate()

def calculatesize(files):
    size_x = []
    size_y = []

    for file in files:
        image = Image.open(file)
        size_x.append(image.size[0])
        size_y.append(image.size[1])

    x_min = min(size_x)
    y_min = min(size_y)
    total_y_size = y_min * len(files)

    return x_min, y_min, total_y_size

def ResizeTomin(files,x_min,y_min,y_size):
    file_list=[]
    for file in files:
        image = Image.open(file)
        resized_file = image.resize((x_min,y_min))
        file_list.append(resized_file)

    return file_list, y_size, x_min, y_min

def ImageMerge(file_list, y_size, x_min, y_min, num):
    try:
        saveImageFileName = "PasteImageMerge.jpg"
        new_image = Image.new("RGB", (x_min, y_size), (256, 256, 256))
        for index in range(len(file_list)):
            area = (0, (index * y_min), x_min, (y_min * (index + 1)))
            new_image.paste(file_list[index], area)
        new_image.save("C:/Users/areum/Documents/GitHub/ML_Project/Image/ReportResult/result" + str(num) + "_" + nowdate + '.png', "PNG")
        return new_image
    except Exception as err:
        common.exception_print(err)

def all(file, num):
    x_min, y_min, y_size = calculatesize(file)
    file_list, y_size, x_min, y_min = ResizeTomin(file, x_min, y_min, y_size)
    ImageMerge(file_list, y_size, x_min, y_min, num)