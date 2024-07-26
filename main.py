import numpy as np
import matplotlib.pyplot as plt

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

    # Display images with matplotlib to test
    display_images(random_image_batches[1])
    