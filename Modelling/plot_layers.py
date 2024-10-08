import matplotlib.patches as patches

def draw_layers(ax, z1, u, v, W):
    layers = [
        {'name': 'Buffer and substrate layers', 'color': 'lightgrey', 'width': 1 * 1e-4},
        {'name': 'Absorption layer', 'color': 'orange', 'width': z1},
        {'name': 'Grading layer', 'color': 'grey', 'width': u},
        {'name': 'Charge layer', 'color': 'lightgrey', 'width': v},
        {'name': 'Multiplication layer', 'color': 'red', 'width': W},
        {'name': 'Diffused layer', 'color': 'blue', 'width': 1 * 1e-4}
    ]

    start = 0
    for layer in layers:
        ax.add_patch(patches.Rectangle((start, 0), layer['width'], 5, edgecolor='black', facecolor=layer['color'], lw=1))
        ax.text(start + layer['width']/2, 2.5, layer['name'], ha='center', va='top', fontsize=12)
        start += layer['width']

    ax.annotate('', xy=(1e-4, 5.4), xytext=(1e-4 + z1, 5.4),
            arrowprops=dict(arrowstyle='<->', color='black'))
    ax.text(1e-4 + (z1 / 2), 5.5, f'z1 = {z1* 1e4:.1f} µm', ha='center', va='bottom', fontsize=12)
    
    z3 = 1e-4 + z1 + u + v
    ax.annotate('', xy=(z3, 5.2), xytext=(z3 + W, 5.2),
                arrowprops=dict(arrowstyle='<->', color='black'))
    ax.text(1e-4 + z1 + u + v + (W / 2), 5.3, f'W = {W* 1e4:.1f} µm', ha='center', va='bottom', fontsize=12)

    ax.set_xlim(0, start)
    ax.set_ylim(0, 6)
    ax.axis('off')
