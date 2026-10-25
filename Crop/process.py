# Importing Libraries ....

import os
import cv2
import pdfplumber

# from PIL import Image, ImageOps
from PIL import Image
import pytesseract
import fitz  # pyMUPdf
from colorama import Fore, Style
import datetime
import time

# Set path to tesseract application
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


##
def resize_dpi(image_path, current_dpi):

    scaling_factor = 300 / current_dpi
    image = Image.open(image_path)
    # Calculate the new size of the image in pixels
    new_width = int(image.width * scaling_factor)
    new_height = int(image.height * scaling_factor)
    # Resize the image using the calculated size
    resized_image = image.resize((new_width, new_height), Image.LANCZOS)
    # Set the new DPI information to 300 DPI
    resized_image.info["dpi"] = (300, 300)

    return resized_image



# Functios to Extract pages from PDF

def PDF_to_Image(filepath):

    try:

        img_paths = []
        for file in filepath:
            pdf = fitz.open(file)
            dpi = 300
            print(os.path.basename(file))

            with pdfplumber.open(file) as p:
                filename = os.path.splitext(os.path.basename(file))[0]
                path = os.path.join(os.curdir, 'images', filename)

                img_paths.append(path)
            if not os.path.exists(path):
                os.makedirs(path)

            for i in range(len(pdf)):
                page = pdf.load_page(i)
                pix = page.get_pixmap(dpi=dpi)
                pix.save(os.path.join(path, f'page_{i + 1}.jpg'))
                print(f"Image {i + 1} out of {len(pdf)} Saved for {filename}!")
                # Removed time.sleep(2) — was blocking the web server thread

        print(Fore.GREEN + "\nAll Images from PDF are Extracted!\n")
        return img_paths

    except Exception as e:
        print("Problem Occurred During Conversation: " + str(e))



# Function to crop articles
def crop(image_paths):

    try:
        print(Fore.GREEN + "\nCropping Started!\n" + Style.RESET_ALL)
        # Removed time.sleep(2) — was unnecessarily blocking

        for path in image_paths:
            for im in os.listdir(path):

                img = os.path.join(path, im)
                img_basename = os.path.basename(img)  # cross-platform

                if img_basename != 'CROP':
                    split2 = os.path.splitext(img_basename)[0]  # filename without extension
                    # Removed time.sleep(3) — was unnecessarily blocking
                    print(f'Working on Image : {split2}')
                    file_dir = os.path.join(path, "CROP", split2)
                    os.makedirs(file_dir, exist_ok=True)
                    # print(f'created folder:{file_dir}')

                    imag = cv2.imread(img)

                    gray = cv2.cvtColor(imag, cv2.COLOR_BGR2GRAY)

                    bfilter = cv2.bilateralFilter(gray, 11, 17, 17)

                    thresh2 = cv2.adaptiveThreshold(
                        bfilter,
                        255,
                        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                        cv2.THRESH_BINARY_INV,
                        199,
                        7,
                    )

                    contours, hier = cv2.findContours(
                        thresh2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
                    )

                    locat = []

                    # detecting all the contours
                    for contour in contours:
                        approx = cv2.approxPolyDP(
                            contour, 0.01 * cv2.arcLength(contour, True), True
                        )
                        """filter contours having 4(Four) points and area greater than 20000"""
                        if (len(approx) >= 4 & len(approx) <= 8) & (cv2.contourArea(contour) > 25000):
                            locat.append(approx)

                    temp = imag

                    for k, contour in enumerate(locat):
                        # processing filter contours
                        bnd = cv2.drawContours(temp, [contour], 0, (0, 0, 255), 3)

                        x, y, w, h = cv2.boundingRect(contour)

                        # here we get dimensions(x,y,height,width) of the image
                        text = path + "_" + str(k)

                        M = cv2.moments(locat[k])
                        # finds the center of the contour
                        if M["m00"] != 0:
                            cx = int(M["m10"] // M["m00"])
                            cy = int(M["m01"] // M["m00"])
                        else:
                            cx, cy = 0, 0

                        org = (cx, cy)
                        font = cv2.FONT_HERSHEY_COMPLEX
                        fontScale = 1
                        color = (0, 0, 255)  # (B,G,R)
                        thickness = 2
                        lineType = cv2.LINE_4
                        bottomLeftOrigin = False
                        """naming the cropped image in the cemter"""
                        temp = cv2.putText(
                            bnd,
                            text,
                            org,
                            font,
                            fontScale,
                            color,
                            thickness,
                            lineType,
                            bottomLeftOrigin,
                        )
                        # slicing the contours
                        cropped_image = gray[y: y + h, x: x + w]
                        cv2.imwrite(f'{file_dir}/{split2}_{str(k + 1)}.jpg', cropped_image)
                    # oringinal image saved with cropped contours of the image in red border and put text cropped image name at center
                    cv2.imwrite(f'{file_dir}/origin.jpg', temp)

        print(f'\n{Fore.GREEN}Images Have been Cropped Successfully!{Style.RESET_ALL}\n')

        return os.path.join(path, 'CROP')  # FIX: was Windows-only backslash path


    except Exception as e:
        print(f'Crop function did not worked! : {e}')


# Function to extract text from articles
def extraction(path):

    try:

        # path = r"images\\trial\\CROP"
        print(f'\n{Fore.GREEN}Text Extraction has been started{Style.RESET_ALL}\n')
        # print("hello")
        output_file_path = os.path.join(path, 'outputfile.txt')
        # print(path)
        # Open the output text file in append mode
        with open(output_file_path, 'a', encoding='utf-8') as output_file:
            for i in os.listdir(path):
                catch = ['Public Notice', 'public notice', 'જાહેર નોટીસ', 'PUBLIC NOTICE', 'જાહેર નોટિસ','पब्लिक नोटिस','जाहीर नोटीस']
                if i.split('.')[-1] != 'txt':
                    for j in os.listdir(os.path.join(path, i)):
                        if j != 'origin.jpg':
                            print(j)
                            text = pytesseract.image_to_string(os.path.join(path, i, j), lang='guj+eng+hin', config='--psm 6')
                            for key in catch:

                                if key in text:
                                    print(f'{Fore.GREEN}\n{j}{Style.RESET_ALL}')
                                    print(f'{text}\n')

                                    # Write the text content to the output text file

                                    output_file.write(f'{j}\n\n')
                                    output_file.write(f'{text}\n\n')
                                    output_file.write(
                                        "\n\n----------------------------------------------------------------------------\n\n")

    except Exception as e:
        print("Problem Occured : "+str(e))
    # text = pytesseract.image_to_string(, lang='guj+eng', config='--psm 6')
    # for m in catch:
    #     if m in text:
    #         print(text)



def main(filepath):

    image_paths = PDF_to_Image(filepath)

    x = crop(image_paths)

    extraction(x)
