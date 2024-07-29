import unittest
import numpy as np
import pandas as pd

from config import (
    IMAGE_SHAPE,
    BATCH_SIZE,
    NUM_BATCHES,
    RANDOM_BLACK_AND_WHITE_SQUARE_SIZE_IN_PX,
    CROP_SIZE
)

from main import (
    count_color_pixels,
    calculate_statistics,
    random_crop,
    generate_random_images,
    validate_batches,
)


class TestImageProcessing(unittest.TestCase):

    def setUp(self):
        self.img_shape = IMAGE_SHAPE
        self.batch_size = BATCH_SIZE
        self.num_batches = NUM_BATCHES
        self.random_black_and_white_square_size_in_px = (
            RANDOM_BLACK_AND_WHITE_SQUARE_SIZE_IN_PX
        )
        self.crop_size = CROP_SIZE

    # Creates a full white, black and red image and
    # checks that the pixel color counting is working well
    def test_count_color_pixels(self):
        white_image = np.full(self.img_shape, [255, 255, 255], dtype=np.uint8)
        black_image = np.full(self.img_shape, [0, 0, 0], dtype=np.uint8)
        red_image = np.full(self.img_shape, [255, 0, 0], dtype=np.uint8)

        self.assertEqual(
            count_color_pixels(white_image, [255, 255, 255]),
            np.prod(self.img_shape[:2]),
            "Count of white pixels is incorrect."
        )

        self.assertEqual(
            count_color_pixels(black_image, [0, 0, 0]),
            np.prod(self.img_shape[:2]),
            "Count of black pixels is incorrect."
        )

        self.assertEqual(
            count_color_pixels(red_image, [255, 0, 0]),
            np.prod(self.img_shape[:2]),
            "Count of red pixels is incorrect."
        )

    # Creates full white image batches and
    # checks that the statistics is working well
    def test_calculate_statistics(self):
        white_batches = []

        for batch in range(self.num_batches):
            batch = np.full(
                (self.batch_size, *self.img_shape),
                [255, 255, 255],
                dtype=np.uint8
            )
            white_batches.append(batch)

        stats_df = calculate_statistics(white_batches)

        self.assertIsInstance(
            stats_df,
            pd.DataFrame,
            "Output is not a DataFrame."
        )

        self.assertEqual(
            stats_df.shape[0],
            self.num_batches,
            "Number of batches in statistics DataFrame is incorrect."
        )

        self.assertEqual(
            stats_df["white_avg"].mean(),
            self.img_shape[0]*self.img_shape[1],
            "white_avg count of statistic test for full white image wrong."
        )

        self.assertEqual(
            stats_df["black_avg"].mean(),
            0,
            "black_avg count of statistic test for full white image wrong."
        )

        expected_columns = [
            'batch_id',
            'white_avg',
            'white_min',
            'white_max',
            'white_std',
            'black_avg',
            'black_min',
            'black_max',
            'black_std']

        self.assertTrue(
            all(column in stats_df.columns for column in expected_columns),
            "Statistics DataFrame missing expected columns."
        )

    def test_random_crop(self):
        batches = generate_random_images(
            self.num_batches,
            self.batch_size,
            self.img_shape
        )
        cropped_batches = random_crop(batches, self.crop_size)

        self.assertEqual(
            len(cropped_batches),
            self.num_batches,
            "Number of cropped batches is incorrect."
        )
        self.assertEqual(
            cropped_batches[0].shape,
            (self.batch_size, *self.crop_size, 3),
            "Cropped batch shape is incorrect."
        )

    def test_corrupted_images(self):
        # Generate a batch with the wrong shape
        corrupted_batches = generate_random_images(
            self.num_batches,
            self.batch_size,
            (self.img_shape[0], self.img_shape[1]-1)
        )

        # Insert an image with wrong pixel values
        corrupted_image = np.full(
            (self.img_shape[0], self.img_shape[1]-1),
            300,
            dtype=np.uint8
        )
        corrupted_batches[1][1] = corrupted_image

        # Validate and check for exception
        with self.assertRaises(ValueError):
            validate_batches(corrupted_batches, self.img_shape)


if __name__ == "__main__":
    unittest.main()
