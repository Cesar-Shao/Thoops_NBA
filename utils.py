import numpy as np
import matplotlib.pyplot as plt
from matplotlib.image import imread

color_map = {
    'RA2': 'r',
    'BA2': 'orange',
    'LB2': 'g',
    'RB2': 'b',
    'LE2': 'lime',
    'RE2': 'royalblue',
    'SL2': 'darkcyan',
    'LC3': 'gold',
    'RC3': 'darkviolet',
    'LW3': 'bisque',
    'RW3': 'plum',
    'SL3': 'navy',
    'OUT': 'gray'
}

area_id = {
    'RA2': 0,
    'BA2': 1,
    'LB2': 2,
    'RB2': 3,
    'LE2': 4,
    'RE2': 5,
    'SL2': 6,
    'LC3': 7,
    'RC3': 8,
    'LW3': 9,
    'RW3': 10,
    'SL3': 11,
    'OUT': 12
}

RA2_radius = 4
BA2_point = np.array([8, 11 - 5.25])
BA2_radius = np.linalg.norm(BA2_point)

three_radius = 23.75
LB2_point = np.array([22, np.sqrt(three_radius ** 2 - 22 ** 2)])

LW3_point = np.array([25, 28])
LW3_radius = np.linalg.norm(LW3_point)

ft_point = np.array([0, 19 - 5.25])
ft_radius = 6
cos_ = (ft_point[1] ** 2 + BA2_radius ** 2 - ft_radius ** 2) / 2 / ft_point[1] / BA2_radius
sin_ = np.sqrt(1 - cos_ ** 2)
LE2_slope = cos_ / sin_

def area_name(p):
    # origin = np.array([0, 0])
    dist = np.linalg.norm(p)

    if dist <= RA2_radius:
        return 'RA2'
    if dist <= BA2_radius:
        return 'BA2'
    if p[0] > 0 and p[0] < LB2_point[0] and p[1] / p[0] < LB2_point[1] / LB2_point[0]:
        return 'LB2'
    if p[0] < 0 and p[0] > -LB2_point[0] and p[1] / p[0] > -LB2_point[1] / LB2_point[0]:
        return 'RB2'
    if p[0] > 0 and p[0] < LB2_point[0] and dist <= three_radius and p[1] / p[0] < LE2_slope:
        return 'LE2'
    if p[0] < 0 and p[0] > -LB2_point[0] and dist <= three_radius and p[1] / p[0] > -LE2_slope:
        return 'RE2'
    if p[0] < LB2_point[0] and p[0] > -LB2_point[0] and dist <= three_radius:
        return 'SL2'
    if p[0] > 0 and p[1] < LB2_point[1]:
        return 'LC3'
    if p[0] < 0 and p[1] < LB2_point[1]:
        return 'RC3'
    if p[0] > 0 and dist <= LW3_radius and p[1] / p[0] < LE2_slope:
        return 'LW3'
    if p[0] < 0 and dist <= LW3_radius and p[1] / p[0] > -LE2_slope:
        return 'RW3'
    if dist <= LW3_radius:
        return 'SL3'
    return 'OUT'

def court_to_image(x=None, y=None):
    if x is not None:
        Y = (x + 25) * 10
    else:
        Y = None
    if y is not None:
        X = (y + 5.25) * 10
    else:
        X = None
    return X, Y

def inter_y(r, k):
    x = np.sqrt(r ** 2 / (k ** 2 + 1))
    y = np.sqrt(r ** 2 - x ** 2)
    return y

def draw_court_weights(w, w_t, fn=None):
    w = (w - w.min()) / (w.max() - w.min())
    w_t = (w_t - w_t.min()) / (w_t.max() - w_t.min()) + 0.1
    court = imread('court/court.png')
    plt.imshow(court)

    # RA2
    y = np.arange(-RA2_radius, RA2_radius, 0.1)
    x1 = np.sqrt(RA2_radius ** 2 - y ** 2)
    x2 = - x1
    x, y1 = court_to_image(x1, y)
    x, y2 = court_to_image(x2, y)
    plt.fill_between(x, y1, y2, facecolor='blue', alpha=w[0])

    # BA2
    y = np.arange(-5.25, BA2_radius, 0.1)
    x1 = np.sqrt(BA2_radius ** 2 - y ** 2)
    x2 = np.sqrt(RA2_radius ** 2 - np.maximum(np.minimum(y, RA2_radius), -RA2_radius) ** 2)
    x, y1 = court_to_image(x1, y)
    x, y2 = court_to_image(x2, y)
    plt.fill_between(x, y1, y2, facecolor='blue', alpha=w[1])
    x1 = - x1
    x2 = - x2
    x, y1 = court_to_image(x1, y)
    x, y2 = court_to_image(x2, y)
    plt.fill_between(x, y1, y2, facecolor='blue', alpha=w[1])
    
    # LB2
    y = np.arange(-5.25, LB2_point[1], 0.1)
    x1 = np.maximum(np.sqrt(BA2_radius ** 2 - y ** 2), y * LB2_point[0] / LB2_point[1])
    x2 = LB2_point[0]
    x, y1 = court_to_image(x1, y)
    x, y2 = court_to_image(x2, y)
    plt.fill_between(x, y1, y2, facecolor='blue', alpha=w[2])

    # RB2
    x1 = - x1
    x2 = - x2
    x, y1 = court_to_image(x1, y)
    x, y2 = court_to_image(x2, y)
    plt.fill_between(x, y1, y2, facecolor='blue', alpha=w[3])
    
    # LE2
    y = np.arange(inter_y(BA2_radius, LB2_point[1] / LB2_point[0]), inter_y(three_radius, LE2_slope))
    x1 = np.maximum(np.sqrt(BA2_radius ** 2 - np.minimum(y, BA2_radius) ** 2), y / LE2_slope)
    x2 = np.minimum(np.sqrt(three_radius ** 2 - y ** 2), y * LB2_point[0] / LB2_point[1])
    x, y1 = court_to_image(x1, y)
    x, y2 = court_to_image(x2, y)
    plt.fill_between(x, y1, y2, facecolor='blue', alpha=w[4])

    # RE2
    x1 = - x1
    x2 = - x2
    x, y1 = court_to_image(x1, y)
    x, y2 = court_to_image(x2, y)
    plt.fill_between(x, y1, y2, facecolor='blue', alpha=w[5])

    # SL2
    y = np.arange(inter_y(BA2_radius, LE2_slope), three_radius, 0.1)
    x1 = np.sqrt(BA2_radius ** 2 - np.minimum(y, BA2_radius) ** 2)
    x2 = np.minimum(np.sqrt(three_radius ** 2 - y ** 2), y / LE2_slope)
    x, y1 = court_to_image(x1, y)
    x, y2 = court_to_image(x2, y)
    plt.fill_between(x, y1, y2, facecolor='blue', alpha=w[6])
    x1 = - x1
    x2 = - x2
    x, y1 = court_to_image(x1, y)
    x, y2 = court_to_image(x2, y)
    plt.fill_between(x, y1, y2, facecolor='blue', alpha=w[6])

    # LC3
    y = np.arange(-5.25, LB2_point[1], 0.1)
    x1 = LB2_point[0]
    x2 = 25
    x, y1 = court_to_image(x1, y)
    x, y2 = court_to_image(x2, y)
    plt.fill_between(x, y1, y2, facecolor='blue', alpha=w[7])

    # RC3
    x1 = - x1
    x2 = - x2
    x, y1 = court_to_image(x1, y)
    x, y2 = court_to_image(x2, y)
    plt.fill_between(x, y1, y2, facecolor='blue', alpha=w[8])

    # LW3
    y = np.arange(LB2_point[1], inter_y(LW3_radius, LE2_slope))
    x1 = np.maximum(np.sqrt(three_radius ** 2 - np.minimum(y, three_radius) ** 2), y / LE2_slope)
    x2 = np.minimum(np.sqrt(LW3_radius ** 2 - y ** 2), 25)
    x, y1 = court_to_image(x1, y)
    x, y2 = court_to_image(x2, y)
    plt.fill_between(x, y1, y2, facecolor='blue', alpha=w[9])

    # RW3
    x1 = - x1
    x2 = - x2
    x, y1 = court_to_image(x1, y)
    x, y2 = court_to_image(x2, y)
    plt.fill_between(x, y1, y2, facecolor='blue', alpha=w[10])

    # SL3
    y = np.arange(inter_y(three_radius, LE2_slope), LW3_radius, 0.1)
    x1 = np.sqrt(three_radius ** 2 - np.minimum(y, three_radius) ** 2)
    x2 = np.minimum(np.sqrt(LW3_radius ** 2 - y ** 2), y / LE2_slope)
    x, y1 = court_to_image(x1, y)
    x, y2 = court_to_image(x2, y)
    plt.fill_between(x, y1, y2, facecolor='blue', alpha=w[11])
    x1 = - x1
    x2 = - x2
    x, y1 = court_to_image(x1, y)
    x, y2 = court_to_image(x2, y)
    plt.fill_between(x, y1, y2, facecolor='blue', alpha=w[11])

    #OUT
    y = np.arange(LW3_point[1], 41.75, 0.1)
    x1 = np.sqrt(LW3_radius ** 2 - np.minimum(y, LW3_radius) ** 2)
    x2 = 25
    x, y1 = court_to_image(x1, y)
    x, y2 = court_to_image(x2, y)
    plt.fill_between(x, y1, y2, facecolor='blue', alpha=w[12])
    x1 = - x1
    x2 = - x2
    x, y1 = court_to_image(x1, y)
    x, y2 = court_to_image(x2, y)
    plt.fill_between(x, y1, y2, facecolor='blue', alpha=w[12])
    
    for i in range(len(w_t)):
        circle = plt.Circle((590, 130 + 60 * i), w_t[i] * 20, color='b', fill='True')
        plt.gcf().gca().add_artist(circle)

    if fn is not None:
        plt.savefig(fn)
    else:
        plt.show()
    plt.close()

if __name__ == '__main__':
    for x in range(-25, 25):
        for y in range(-5, 42):
            label = area_name(np.array([x, y]))
            # plt.scatter(x, y, c=color_map[label])
            plt.scatter((y + 5.25) * 10, (x + 25) * 10, c=color_map[label], linewidths=0, alpha=0.3)
    plt.axis('equal')
    court = imread('court/court.png')
    plt.imshow(court)
    plt.show()