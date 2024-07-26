import numpy as np
import matplotlib.pyplot as plt

def add_randomly_placed_squares(random_images, image_shape, square_size = 50):
    half_square = square_size // 2
    batches = []

    for batch in random_images:
        processed_batch = []
        for image in batch:
            #First define a random postion fo the white square making sure it's entirely in the picture
            random_position_white_square_y = np.random.randint(half_square, high=image_shape[0]-half_square, dtype=int)
            random_position_white_square_x = np.random.randint(half_square, high=image_shape[1]-half_square, dtype=int)

           # Then we define an array of possible x and y positions for the black square by taking away overlapping 
            possible_positions = [
                (x, y) for x in range(half_square, image_shape[1] - half_square) # also make sure in
                for y in range(half_square, image_shape[0] - half_square)
                if not (
                    (x + half_square > random_position_white_square_x - half_square) and
                    (x - half_square < random_position_white_square_x + half_square) and
                    (y + half_square > random_position_white_square_y - half_square) and
                    (y - half_square < random_position_white_square_y + half_square)
                )
            ]

            # Choose a random position from the possible positions
            random_position_black_square_x, random_position_black_square_y = possible_positions[np.random.randint(len(possible_positions))]

             # Place the black square at the random position
            image[random_position_white_square_y - half_square : random_position_white_square_y + half_square,
                random_position_white_square_x  - half_square : random_position_white_square_x  + half_square] = [255, 255, 255]
            
             # Place the black square at the random position
            image[random_position_black_square_y - half_square:random_position_black_square_y + half_square,
                  random_position_black_square_x - half_square:random_position_black_square_x + half_square] = [0, 0, 0]

            processed_batch.append(image)
            
        batches.append(np.array(processed_batch))
    return batches


def generate_random_images(num_batches, batch_size, image_shape):
    batches = []

    for batch in range(num_batches):
        batch = np.random.randint(0, 255, (batch_size, *image_shape), dtype=np.uint8) 
        batches.append(batch)

    return batches

def display_images(batch, num_images=5):
    fig, axes = plt.subplots(1, num_images, figsize=(20, 4))
    for i in range(num_images):
        ax = axes[i]
        ax.imshow(batch[i])
        ax.axis('off')
    plt.show()

if __name__ == "__main__":
    num_batches = 5
    batch_size = 20
    image_shape = (256, 512, 3)

    # Generatw  batches of images with random RGB values
    random_image_batches = generate_random_images(num_batches, batch_size, image_shape)

    processed_images = add_randomly_placed_squares(random_image_batches, image_shape)

    # Display images with matplotlib to test
    display_images(processed_images[1])
    