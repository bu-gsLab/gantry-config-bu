import numpy as np
import argparse
import math


parser = argparse.ArgumentParser()
parser.add_argument("--moduleid", action="store")
args = parser.parse_args()

if __name__ == "__main__":
    pts = []
    with open(f'C:/Users/User/Desktop/gantry-config-bu/Logs/PCB_height_survey_{args.moduleid}.txt', 'r') as file:
        for line in file:
            if line.strip() == "":
                continue
            printed = line.split(">>>")[1].strip()
            data = printed.split()
            if data[0] == 'pt':
                pt_string = data[3][1:len(data[3])-1].split(",")
                pt = [round(float(pt_string[0]),3),round(float(pt_string[1]),3),round(float(pt_string[2]),3)]
                pts.append(pt)
            elif data[0] == "tl":
                tl_string = data[1][1:len(data[1])-1].split(",")
                tl = [round(float(tl_string[0]),3),round(float(tl_string[1]),3),round(float(tl_string[2]),3)]
            elif data[0] == "br":
                br_string = data[1][1:len(data[1])-1].split(",")
                br = [round(float(br_string[0]),3),round(float(br_string[1]),3),round(float(br_string[2]),3)]

    corner_to_corner_distance = math.dist(br, tl)

    centroid = np.mean(np.array(pts), axis=0, keepdims=True)
    u, s, vh = np.linalg.svd(np.array(pts) - centroid)

    normal = np.round(vh[-1],decimals=3)
    d = -np.dot(normal, centroid[0])
    numerator = np.dot(pts, normal) + d
    denominator = np.linalg.norm(normal)

    distances = np.round(numerator / denominator,decimals=3)
    abs_distances = np.round(abs(distances),decimals=3)
    max_dist = max(abs_distances)
    warpage = (max_dist / corner_to_corner_distance)*100
    
    with open(f"C:/Users/User/Desktop/gantry-config-bu/Scripts/BostonU/PCB_flatness_survey/results/results_{args.moduleid}.txt","w") as file:
        file.write(f"Corner to corner distance: {corner_to_corner_distance:.3f}\n")
        file.write(f"Points: {pts}\n")
        file.write(f"Best fit plane normal: {normal}\n")
        file.write(f"Centroid of plane: {np.round(centroid[0],decimals=3)}\n")
        file.write(f"Distances: {distances}\n")
        file.write(f"Absolute distances: {abs_distances}\n")
        file.write(f"Max distance: {max_dist:.3f}\n")
        file.write(f"Warpage: {warpage:.3f}%\n")


