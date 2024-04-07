import N1_CropToLeftGrid
import N2_ExtractCoordinate
import N3_NodesRelationship
import N4_RemoveAddRelation
import N5_UseCoordTopoDrawGrid

surface_name = '1G20'

output_dir = 'Surface' + '_' + surface_name


print('■'*5, 'STEP 1: CROP IMAGE')
N1_CropToLeftGrid.crop(surface_name)

print()
print('■'*5, 'STEP 2: EXTRACT COORDINATES')

N2_ExtractCoordinate.extract_coordinates(surface_name)

print()
print('■'*5, 'STEP 3: EXTRACT RELATIONSHIP')

N3_NodesRelationship.nodes_relationship(surface_name)

print()
print('■'*5, 'STEP 4: FIX THE BUG MAY EXIST')

N4_RemoveAddRelation.Rmv_add_relatn(surface_name, final_img_name="N4_GridWithKeys")

print()
print('■'*5, 'STEP 5: DRAW THE FINAL RESULT')

N5_UseCoordTopoDrawGrid.CoordTopo2grid(surface_name, show_text=False).run()


print("If there still exists any wrong relationship, just run 'N4_RemoveAddRelation.py' separately.")