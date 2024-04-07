import json
from N5_UseCoordTopoDrawGrid import CoordTopo2grid


def interaction():
    result_list = []
    while True:
        try:
            input_str = input("Enter two numbers separated by a space (or enter 'q' to quit): ")
            if input_str in ['q', 'Q']:
                break
            nums = [int(num) for num in input_str.split()]
            
            if len(nums) != 2:
                print("Please enter only two numbers!")
                continue
            if nums[0] > nums[1]:
                result_list.append([nums[1], nums[0]])
            else:
                result_list.append(nums)
        except ValueError:
            print("Please enter only numeric values!")
            continue
    return result_list


def Rmv_add_relatn(surface_name, final_img_name):
    output_dir = 'Surface' + '_' + surface_name
    
    CoordTopo2grid(surface_name, final_img_name, show_text=True).run()

    
    with open(f'{output_dir}/adjacency_relation.json', 'r') as f:
        adjacency_relation = json.load(f)


    '''remove the wrong adjacency relationship'''
    
    print('*'*50)
    print("Now, please remove wrong relationship(REMIND: open N4_GridWithKeys.jpg in folder to check).")
    
    wrong_list = interaction()
    
    adjacency_relation = [x for x in adjacency_relation if x not in wrong_list]


    '''add the missing adjacency relationship'''
    
    print('*'*50)
    print("Now, please add the missing relationship.")
    
    missing_list = interaction()
    
    for item in missing_list:
        adjacency_relation.append(item)
    
    '''write back the adjust adjacency relationship file'''
    with open(f'./{output_dir}/adjacency_relation.json', 'w') as fp:
        json.dump(adjacency_relation, fp, indent=4)


if __name__ == '__main__':
    Rmv_add_relatn(surface_name = '4-000', final_img_name='N4_GridwithKeys')