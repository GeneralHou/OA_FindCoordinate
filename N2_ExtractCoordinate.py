import cv2
import numpy as np
import json


def extract_coordinates(surface_name):
    output_dir = 'Surface_' + surface_name
    def shw_img(img, title='default'):
        cv2.namedWindow(title, 0)
        w, h = min(1920, img.shape[1]), min(1080, img.shape[0])
        cv2.resizeWindow(title, w, h) 
        cv2.imshow(title, img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    img = cv2.imread(f'./{output_dir}/{surface_name}_red_crop.jpg')
    
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    
    lower_red = np.array([0, 50, 50])
    upper_red = np.array([10, 255, 255])

    
    mask1 = cv2.inRange(hsv, lower_red, upper_red)

    
    lower_red = np.array([170, 50, 50])
    upper_red = np.array([180, 255, 255])

    
    mask2 = cv2.inRange(hsv, lower_red, upper_red)

    
    mask = mask1 + mask2
    shw_img(mask, "mask(from N2.py)")

    print('If some nodes are too close and connected, You can use morphology operation: OPEN')
    print("You can adjust 'kernel'in the source code")
    
    
    input("Press 'ENTER' to continue >>>>>>>")

    
    kernel = np.ones((45,45), np.uint8)  
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    shw_img(mask, "after_open(from N2.py)")

    
    contours, _ = cv2.findContours(np.uint8(mask), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    found_coordinates = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w > 1 and h > 1:
            cx = int(x + w / 2)
            cy = int(y + h / 2)
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), -1, cv2.LINE_AA)
            
            found_coordinates.append([round(cx), round(cy)])

    all_coordinates_dict = {x: y for x, y in enumerate(found_coordinates)}
    json_str = json.dumps(all_coordinates_dict, indent=4)
    with open(f'./{output_dir}/coordinates.json', 'w') as json_file:
        json_file.write(json_str)

    cv2.imwrite(f'./{output_dir}/N2_FoundNodes.jpg', img)


if __name__ == '__main__':
    extract_coordinates(surface_name='1-000')