import networkx as nx
import matplotlib.pyplot as plt
import json


class CoordTopo2grid:
    def __init__(self, surface_name, final_img_name='N5_FinalResult', show_text=False):
        self.surface_name = surface_name
        self.final_img_name = final_img_name
        self.show_text = show_text

    def run(self):
        output_dir = 'Surface_' + self.surface_name
        with open(f'{output_dir}/coordinates.json', 'r') as f:
            coordinates = json.load(f)
        coordinates = {int(k): v for k, v in coordinates.items()}

        with open(f'{output_dir}/adjacency_relation.json', 'r') as f:
            adjacency_relation = json.load(f)

        G = nx.Graph()

        
        for k, v in coordinates.items():
            
            x, y = v[0], -v[1]
            G.add_node(k, pos=(x, y))

        
        G.add_edges_from(adjacency_relation)

        pos = nx.get_node_attributes(G, 'pos')

        nx.draw(G, pos, node_color='red', node_size=1, edge_color='black', width=0.5)

        
        if self.show_text:
            for k, v in coordinates.items():
                x, y = v[0], -v[1]
                plt.text(x, y, str(k), fontsize=4, ha='left', va='center', color='blue')

        plt.savefig(f'{output_dir}/{self.final_img_name}.jpg', dpi=1200)


if __name__ == '__main__':
    Grid2d = CoordTopo2grid(surface_name='4-000', final_img_name='N5_FinalResult', show_text=True)
    Grid2d.run()