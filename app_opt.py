import pygame

# Initialize pygame
pygame.init()

# Set up display
window = pygame.display.set_mode((1200, 400))
track = pygame.image.load('track6.png')
car_image = pygame.image.load('tesla.png')
car_image = pygame.transform.scale(car_image, (30, 60))

# Car properties
car_x, car_y = 155, 280
focal_dist = 25
cam_x_offset, cam_y_offset = 0, 0
direction = 'up'
drive = True
clock = pygame.time.Clock()


def detect_road(camera_position):
    """Detects road pixels around the camera position."""
    cam_x, cam_y = camera_position
    up_px = window.get_at((cam_x, cam_y - focal_dist))[0]
    down_px = window.get_at((cam_x, cam_y + focal_dist))[0]
    right_px = window.get_at((cam_x + focal_dist, cam_y))[0]
    return up_px, down_px, right_px


def update_direction(up_px, down_px, right_px):
    """Updates car direction and offsets based on detected pixels."""
    global direction, cam_x_offset, cam_y_offset, car_image, car_x, car_y

    if direction == 'up' and up_px != 255 and right_px == 255:
        direction = 'right'
        cam_x_offset = 30
        car_image = pygame.transform.rotate(car_image, -90)
    elif direction == 'right' and right_px != 255 and down_px == 255:
        direction = 'down'
        car_x += 30
        cam_x_offset, cam_y_offset = 0, 30
        car_image = pygame.transform.rotate(car_image, -90)
    elif direction == 'down' and down_px != 255 and right_px == 255:
        direction = 'right'
        car_y += 30
        cam_x_offset, cam_y_offset = 30, 0
        car_image = pygame.transform.rotate(car_image, 90)
    elif direction == 'right' and right_px != 255 and up_px == 255:
        direction = 'up'
        car_x += 30
        cam_x_offset = 0
        car_image = pygame.transform.rotate(car_image, 90)


def move_car(up_px, down_px, right_px):
    """Moves car based on the current direction and detected road pixels."""
    global car_x, car_y

    if direction == 'up' and up_px == 255:
        car_y -= 2
    elif direction == 'right' and right_px == 255:
        car_x += 2
    elif direction == 'down' and down_px == 255:
        car_y += 2


def main():
    global drive
    while drive:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                drive = False

        # Camera position for obstacle detection
        cam_x, cam_y = car_x + cam_x_offset + 15, car_y + cam_y_offset + 15
        up_px, down_px, right_px = detect_road((cam_x, cam_y))

        # Print detected pixel values
        print(up_px, right_px, down_px)

        # Update direction based on road detection
        update_direction(up_px, down_px, right_px)

        # Move the car in the current direction
        move_car(up_px, down_px, right_px)

        # Draw everything
        window.blit(track, (0, 0))
        window.blit(car_image, (car_x, car_y))
        pygame.draw.circle(window, (0, 0, 255), (cam_x, cam_y), 5, 5)
        pygame.display.update()


# Run the main loop
main()
