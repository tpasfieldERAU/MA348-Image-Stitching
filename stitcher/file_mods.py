import numpy as np

def DrawImageFromCoords(coords, vals):
    # Find max and min of x1 and x2 in coords, use for bounding box of image.
    # Min/Max of vals doesn't matter, we aren't normalizing.
    x1 = coords[:,0]
    x2 = coords[:,1]

    x1_min = np.min(x1)
    x1_max = np.max(x1)
    x2_min = np.min(x2)
    x2_max = np.max(x2)

    width = round(x1_max - x1_min)+1
    height = round(x2_max - x2_min)+1

    img = np.zeros((width, height), dtype=np.uint8)

    for i in range(vals.size):
        x1 = round(coords[i, 0])
        x2 = round(coords[i, 1])
        img[x1,x2] = vals[i]
    return img


def GenerateCoordsFromImage(image):
    (n,m) = image.shape
    coords = np.zeros((image.size, 2))
    vals = np.zeros((image.size,1), dtype=np.uint8)
    k = 0
    for i in range(n):
        for j in range(m):
            coords[k, 0] = i
            coords[k, 1] = j
            vals[k] = image[i,j]
            k += 1
    return coords, vals


def interpolate(image):
    (n,m) = image.shape
    buffer = np.zeros(image.shape, dtype=np.uint8)
    for i in range(n):
        for j in range(m):
            if image[i,j] == 0:
                ## Decide to interpolate or not
                up = image[i-1,j]

                try:
                    down = image[i+1,j]
                except IndexError:
                    down = 0

                left = image[i,j-1]

                try:
                    right = image[i,j+1]
                except IndexError:
                    right = 0

                vals = [up, down, left, right]
                count = 0
                for val in vals:
                    if val > 0:count+=1
                if count > 2:
                    buffer[i,j] = sum(vals)//count
            else:
                buffer[i,j] = image[i,j]

    return buffer