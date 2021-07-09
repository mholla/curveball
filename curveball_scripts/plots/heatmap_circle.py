"""
Cortical thickness map with size of circles indicating total number of vertices
"""

def heatmap_circle(t_ave_map, ind_ave_map, s, l):
    
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.collections import PatchCollection
    
    # arrange size of the circles according to total # of vertex map
    N = len(t_ave_map)
    M = len(t_ave_map)
    
    size = np.zeros([M,N])
    
    for i in range(len(ind_ave_map)):
        for j in range(len(ind_ave_map)):
            if ind_ave_map[i,j] > 500:
                size[i,j] = 0.5
            elif ind_ave_map[i,j] > 100 and ind_ave_map[i,j] <= 500:
                size[i,j] = 0.4
            elif ind_ave_map[i,j] > 10 and ind_ave_map[i,j] <= 100:
                size[i,j] = 0.3
                
            else:
                size[i,j] = 0.2
            
    # reverse color map    
    color_map = plt.cm.get_cmap('viridis')
    rev_color_map = color_map.reversed()
    
    ylabels = l
    xlabels = s
    
    x, y = np.meshgrid(np.arange(M), np.arange(N))
    
    fig, ax = plt.subplots()
    circles = [plt.Circle((j,i), radius=r) for r, j, i in zip(size.flat, x.flat, y.flat)]
    col = PatchCollection(circles, array=t_ave_map.flatten(), cmap=rev_color_map)
    ax.add_collection(col)
    ax.set_aspect(1)
    ax.set(xticks=np.arange(M+1)-0.5, yticks=np.arange(N+1)-0.5, xticklabels=xlabels, yticklabels=ylabels)
    ax.tick_params(axis='x', labelrotation = 45)
    plt.gca().invert_yaxis()
    
    fig.colorbar(col)
    plt.show()
    
    return

