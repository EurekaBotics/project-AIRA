import math

def inverse_kinematics_3d(target, a, b, c, hip_position):
    # Calculate θ
    delta_x = target[0] - hip_position[0]
    delta_z = target[2] - hip_position[2]
    theta = math.atan2(delta_z, delta_x)

    # Calculate A
    delta_y = target[1] - hip_position[1]
    delta_w = math.sqrt((delta_x ** 2) + (delta_y ** 2) + (delta_z ** 2))
    A_prime = math.atan2(delta_y, delta_w)

    # Calculate A
    alpha = math.acos((b**2 + c**2 - a**2) / (2 * b * c))
    A = alpha + A_prime

    # Calculate B
    beta = math.acos((a**2 + c**2 - b**2) / (2 * a * c))
    B = math.pi - beta

    return A, B, theta

# Example usage:
target_point = (1.0, 2.0, 3.0)  # Replace with your target point coordinates
segment_lengths = (2.0, 3.0, 4.0)  # Replace with your segment lengths (a, b, c)
hip_position = (0.0, 0.0, 0.0)  # Replace with the hip joint position (A_X, A_Y, A_Z)

A_angle, B_angle, theta_angle = inverse_kinematics_3d(target_point, *segment_lengths, *hip_position)

print(f"A Angle: {math.degrees(A_angle)} degrees")
print(f"B Angle: {math.degrees(B_angle)} degrees")
print(f"θ Angle: {math.degrees(theta_angle)} degrees")
