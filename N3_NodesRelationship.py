import cv2
import json
import numpy as np
import random


def shw_img(img, title='default'):
    cv2.namedWindow(title, 0)
    w, h = min(1920, img.shape[1]), min(1080, img.shape[0])
    cv2.resizeWindow(title, w, h) 
    cv2.imshow(title, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def is_red(img, coordinate):
    red = [0,0,255]
    point_pixel = img[coordinate[1], coordinate[0]]
    judge = np.array_equal(point_pixel, red)
    return judge

def is_black(img, coordinate):
    black = [0,0,0]
    point_pixel = img[coordinate[1], coordinate[0]]
    judge = np.array_equal(point_pixel, black)
    return judge


def exceed_bound(img, coordinate):
    img_h, img_w = img.shape[:2]
    judge = coordinate[0] >= img_w or coordinate[0] < 0 or \
            coordinate[1] >= img_h or coordinate[1] < 0
    return judge

def find_red_bound(img, coordinate):
    red_bound = {'L':[-1,0], 'R':[1,0], 'T':[0,-1], 'B':[0,1]}
    for k, move_one_pixel in red_bound.items():
        current_coord = coordinate
        while is_red(img, current_coord) == True:
            found_bound = current_coord
            current_coord = [x+y for x,y in zip(current_coord, move_one_pixel)]
            
            if exceed_bound(img, current_coord) == True: break
        red_bound[k] = found_bound
    return red_bound


def crop_red_rectangle(img, rL, rR, rT, rB):
    expand_factor = 0.3
    expand_length = max((rR-rL)*expand_factor, (rB-rT)*expand_factor)
    x1, y1 = rL-expand_length, rT-expand_length
    x2, y2 = rR+expand_length, rB+expand_length
    
    x1, y1 = int(x1), int(y1)  
    x2, y2 = int(x2), int(y2)
    red_rect_img = img[y1:y2, x1:x2]
    anchor = [x1, y1]
    return red_rect_img, anchor


def black_lines_corresponding_centers(img, anchor):
    
    
    
    def erosion(img):
        big_kernel = np.ones((6,6), np.uint8)
        img = cv2.erode(img, big_kernel, iterations=2)
        small_kernel = np.ones((3,3), np.uint8)
        img = cv2.erode(img, small_kernel, iterations=2)
        return img
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    
    _, thresh = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY_INV)
    
    erosion_img = erosion(thresh)
    
    _, _, _, centroids = cv2.connectedComponentsWithStats(erosion_img, 8, cv2.CV_32S)
    
    local_center_list = [[int(x[0]), int(x[1])] for x in centroids[1:]]  
    
    global_center_list = [[x[0]+anchor[0], x[1]+anchor[1]] for x in local_center_list]
    return global_center_list


def find_other_red_dots(img, start_point_list, origin_red_dot, test_mode=False):
    
    found_red_dots_coords = []
    
    def calculate_dist(p1, p2):  
        return np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

    for start_point in start_point_list:
        
        current_point = start_point
        current_dist = calculate_dist(start_point, origin_red_dot)

        
        
        directions = [[1,1], [1,-1], [-1,-1], [-1,1],[0, 1], [0, -1], [1, 0], [-1, 0]]
        
        
        tried, d_factor = 0, 1
        while True:
            random_indices = random.sample(range(8), 8)  
            for index in random_indices:
                direct = directions[index]
                next_point = [current_point[0]+direct[0]*d_factor, current_point[1]+direct[1]*d_factor]
                if test_mode: print(f"To next from point(OriginalRedPoint:{origin_red_dot}): {current_point}")
                next_dist = calculate_dist(next_point, origin_red_dot)
                if exceed_bound(img, next_point):  
                    break  
                elif is_red(img, next_point):  
                    found_red_dots_coords.append(next_point)
                    break
                elif is_black(img, next_point) and next_dist >= current_dist:
                    current_point, current_dist = next_point, next_dist
                    break
                else:
                    
                    
                    tried += 1
                    if tried % len(directions) == 0:
                        
                        
                        d_factor += 1


                    continue
            if exceed_bound(img, next_point) or is_red(img, next_point): 
                break  
    return found_red_dots_coords


def serial_number_pairs(mom_dot_key, child_red_dots_coord, coordinates):
    paired_result = []
    for child_coord in child_red_dots_coord:
        dist = float('inf')
        for k, v in coordinates.items():
            if k == mom_dot_key: continue 
            new_dist = np.sqrt((v[0] - child_coord[0])**2 + (v[1] - child_coord[1])**2)
            if new_dist <= dist:
                dist = new_dist
                temp_k = k  
        paired_result.append(sorted([temp_k, mom_dot_key]))
    return paired_result

def relation_in_image(img, coordinates, test_mode=False, test_n=0):
    adjacency_relation = []
    for n, coord in coordinates.items():  
        if test_mode: n, coord = test_n, coordinates[test_n]
        print(f'Processing Node {n}: with coord {coord}')
        '''search two direction(x and y) to find out the boundary of red dot(node)'''
        red_bound = find_red_bound(img, coord)

        '''find out how many black lines connected to the red dot(node)'''
        rL, rR = red_bound['L'][0], red_bound['R'][0]  
        rT, rB = red_bound['T'][1], red_bound['B'][1]  
        
        red_rect_img, anchor = crop_red_rectangle(img, rL, rR, rT, rB)
        
        center_list = black_lines_corresponding_centers(red_rect_img, anchor)

        '''search other red dots(nodes)'''
        found_red_dots = find_other_red_dots(img, center_list, coord, test_mode=test_mode)  
        
        serial_pairs = serial_number_pairs(n, found_red_dots, coordinates)
        
        print(f'Processing Node {n}: Finished')
        adjacency_relation += serial_pairs
        if test_mode: break

    return adjacency_relation

def nodes_relationship(surface_name, test_mode=False, test_n=0):
    '''''''''''''PREPARE FOR MAIN'''''''''''''''
    '''DEFINE FILE PATHS'''
    output_dir = 'Surface_' + surface_name
    
    
    img_path = f'./{output_dir}/{surface_name}_crop.jpg'
    
    coord_path = f'./{output_dir}/coordinates.json'

    '''LOAD DATA'''
    
    with open(coord_path, 'r') as f:
        result = json.load(f)
    coordinates = {int(k): v for k, v in result.items()}

    
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    img[img < 230] = 0  
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    

    for _, v in coordinates.items():
        cv2.circle(img, tuple(v), radius=45, color=(0,0,255), thickness=-1)
    if test_mode: cv2.imwrite(f'./{output_dir}/N3_{surface_name}_test.jpg', img)
    print('Red dots can be set to smaller or bigger by adjusting source code.')
    print('This two parameter can be adjusted: radius and thickness.')
    shw_img(img, 'Please check the image is perfect enough to be process(from N3.py)')
    input('Press ENTER to continue(ctrl+c to quit) >>>>>>')

    '''''''''''''MAIN PART OF THIS FUNCTION'''''''''''''''
    adjacency_relation = relation_in_image(img, coordinates, test_mode, test_n)

    
    adjacency_relation = [list(x) for x in set(tuple(x) for x in adjacency_relation)]
    
    
    with open(f'./{output_dir}/adjacency_relation.json', 'w') as fp:
        json.dump(adjacency_relation, fp, indent=4)


if __name__ == '__main__':
    nodes_relationship(surface_name='G356', test_mode=False, test_n=235)
