import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def count_color_pixels(image, color):
    color = np.array(color)
    count = np.sum(np.all(image == color, axis=-1))
    print(count)
    return count

def calculate_statistics(batches):
    white = [255, 255, 255]
    black = [0, 0, 0]

    batch_counter=0
    batch_statistics = []

    for batch in batches:
        white_counts = []
        black_counts = []
        batch_counter += 1

        for image in batch:
            white_count = count_color_pixels(image, white)
            black_count = count_color_pixels(image, black)
            white_counts.append(white_count)
            black_counts.append(black_count)
        
        print(f"Batch {batch_counter} - White counts: {white_counts}, Black counts: {black_counts}")
        
        batch_stats = {
            'batch_id': "batch_" + str(batch_counter),
            'white_avg': np.mean(white_counts),
            'white_min': np.min(white_counts),
            'white_max': np.max(white_counts),
            'white_std': np.std(white_counts),
            'black_avg': np.mean(black_counts),
            'black_min': np.min(black_counts),
            'black_max': np.max(black_counts),
            'black_std': np.std(black_counts)
        }

        batch_statistics.append(batch_stats)
    
    df_batch_statistics = pd.DataFrame(batch_statistics)
    
    return df_batch_statistics


def random_crop(images, crop_size):
    crop_height, crop_width = crop_size
    cropped_batches = []

    for batch in images:
        cropped_batch = []
        for image in batch:
            # first determine what is max x and y
            max_x = image.shape[1] - crop_width
            max_y = image.shape[0] - crop_height
            
            # then choose random starting crop
            x = np.random.randint(0, max_x + 1)
            y = np.random.randint(0, max_y + 1)

            # crop the image
            cropped_image = image[y:y + crop_height, x:x + crop_width]
            cropped_batch.append(cropped_image)
        cropped_batches.append(np.array(cropped_batch))

    return cropped_batches

def add_randomly_placed_squares(random_images, image_shape, square_size):
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

def display_images(batch, num_images=20):
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
    random_black_and_white_square_size_in_px = 50
    crop_size = (200, 200)

    # Generatw  batches of images with random RGB values
    random_image_batches = generate_random_images(num_batches, batch_size, image_shape)

    processed_images_with_squares = add_randomly_placed_squares(random_image_batches, image_shape, random_black_and_white_square_size_in_px)

    randomly_cropped_images=random_crop(processed_images_with_squares, crop_size)

    # Calculate statistics for each batch and color
    stats_df = calculate_statistics(randomly_cropped_images)

    print(stats_df)

    # Display images with matplotlib to test
    display_images(randomly_cropped_images[0])
    