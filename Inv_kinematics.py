import numpy as np

def movetopos(x, y, z):

    b = np.arctan2(y,x) * (180/3.1415)
    l = np.sqrt(x**2 + y**2)
    h = np.arctan(l**2+z**2)
    phi = np.arctan(z/l)*(180/3.1415)
    theta = np.arccos((h/2)/75)*(180/3.1415)

    a1 = phi+theta
    a2 = phi+theta

    return b, a1, a2

def calculate_angles(x, y, a1, a2):

    q2 = np.arccos((x**2+y**2-a1**2-a2**2)/(2*a1*a2))
    q1 = np.arctan(y/x)-np.arctan((a2*np.sin(q2))/(a1+a2*np.cos(q2)))

    return q1, q2
if __name__ == "__main__":
    # print(movetopos(90,100,10))
    # print(calculate_angles(2,2,2,1.6))
    q1, q2 = calculate_angles(1,2,2,1.6)
    print((180/np.pi)*q1, (180/np.pi)*q2)