import cv2
import os
import numpy as np
import math
import pandas as pd

# Path to the folder containing images
# folder_path = "/home/nebulaa/Desktop/calculate_length/Broken Grains"
folder_path=input("enter the folder path: ")
# Get a list of image files in the folder
image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

# Sort the image files for consistent order
image_files.sort()
folder_name = 'prossed_image'
folder_name=os.path.join(folder_path,folder_name)
if not os.path.exists(folder_name):
    os.makedirs(folder_name)
    print(f"Folder '{folder_name}' created successfully.")

# Initialize variables.
current_index = 0
total_images = len(image_files)
data_excel=[]
def mouse_callback(event, x, y, flags, param):
    global prev_x, prev_y, total_length, clik, points, contour_number, total_list,data_excel,image_files,current_index,i
    if event == cv2.EVENT_LBUTTONDBLCLK:
        clik=True
        # print(clik)
        # print("left double click")
        print(f"Clicked at pixel coordinates: ({x}, {y})")
        points.append((x, y))
        if prev_x is not None and prev_y is not None:
            length = math.sqrt((x - prev_x)**2 + (y - prev_y)**2)
            total_length += length
            # print(f"Length of the current line: {length:.2f} pixels")
            # print(f"Total pixel length: {total_length:.2f} pixels")
            cv2.line(image, (prev_x, prev_y), (x, y), (0, 255, 0), 1)
        prev_x, prev_y = x, y
    if event == cv2.EVENT_LBUTTONDOWN and clik == True:
        # print(clik)
        # print("left click")
        print(f"Clicked at pixel coordinates: ({x}, {y})")
        points.append((x, y))
        if prev_x is not None and prev_y is not None:
            length = math.sqrt((x - prev_x)**2 + (y - prev_y)**2)
            total_length += length
            # print(f"Length of the current line: {length:.2f} pixels")
            # print(f"Total pixel length: {total_length:.2f} pixels")
            cv2.line(image, (prev_x, prev_y), (x, y), (0, 255, 0), 1)
        prev_x, prev_y = x, y
    if event == cv2.EVENT_RBUTTONDOWN:
        i=i+1
        clik=False
        # print(i)
        # print("rigth click")
        if len(points) > 0:
        # Calculate centroid
            centroid = np.mean(points, axis=0).astype(int)
        print(centroid)

        print(f"Total pixel length: {total_length:.2f} pixels")
        cv2.putText(image, f"{total_length:.2f}", tuple(centroid),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA)
        
        # append total length to list
        points=[]
        data_excel.append([image_files[current_index],i,f"{total_length:.2f}"])
        prev_x, prev_y, total_length = None, None, 0.0
    cv2.imshow("Image", image)
    cv2.resizeWindow('Image', 800, 600)
# Create a window
cv2.namedWindow("Image", cv2.WINDOW_NORMAL)





while True:
    # Read the current image
    image_path = os.path.join(folder_path, image_files[current_index])
    
    image = cv2.imread(image_path)
    clik=False
    points=[]
    total_list=[]
    contour_number = 1
    prev_x, prev_y, total_length = None, None, 0.0
    i=0

    cv2.namedWindow("Image")
    cv2.setMouseCallback("Image", mouse_callback)
    
    # Display the image
    
    # cv2.moveWindow('Image Viewer', 200, 200)
    # cv2.setWindowProperty('Image Viewer', cv2.WND_PROP_AUTOSIZE, 0)
    # Wait for a key event
    key = cv2.waitKey(0)

    # Check for key actions
    if key == 27 or current_index==total_images:  # If the Esc key is pressed, exit the loop
        break
    elif key == ord('n') or key == ord('N'):
        # Move to the next image
        save_path = os.path.join(folder_name, image_files[current_index])
        cv2.imwrite(save_path, image)
        current_index = (current_index + 1)
        if current_index>=total_images:
            break

    elif key == ord('r') or key == ord('R'):
        for j in range(i):
            data_excel.pop()
        current_index = (current_index)
        # Remove all dots
        dots = []

# Destroy the OpenCV window
cv2.destroyAllWindows()
# Convert the list to a DataFrame
df = pd.DataFrame(data_excel, columns=['Image', 'No_of_contours', 'contour_lenght'])

# Save the DataFrame to an Excel file
excel_filename = 'contour_lengths.xlsx'
excel_filename=os.path.join(folder_path, excel_filename)
df.to_excel(excel_filename, index=False)

print(f"Excel file '{excel_filename}' created successfully.")
