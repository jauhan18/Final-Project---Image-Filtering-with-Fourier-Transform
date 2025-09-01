import cv2
import numpy as np

def apply_frequency_filter(image_path, filter_type='low', radius=30):

    # baca gambar grayscaale
    original_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if original_image is None:
        print(f"Error: Tidak dapat membuka gambar di path: {image_path}")
        return None, None

    # transformasi fourier (fft)
    # ubah gambar (pixel) menjadi domain frekuensi
    f_transform = np.fft.fft2(original_image)
    # geser komponen frekuensi 0 (dc component) ke tengah
    f_transform_shifted = np.fft.fftshift(f_transform)

    # buat mmask filter
    rows, cols = original_image.shape
    crow, ccol = rows // 2, cols // 2  # Titik tengah spektrum

    mask = np.zeros((rows, cols), np.uint8)
    
    if filter_type == 'low':
        # low-pass filter
        # hasilnya gambar yang lebih halus/blur
        cv2.circle(mask, (ccol, crow), radius, 1, thickness=-1)
    elif filter_type == 'high':
        # high-pass filter
        # hasilnya berupa tepian (edges) dari gambar
        mask = np.ones((rows, cols), np.uint8)
        cv2.circle(mask, (ccol, crow), radius, 0, thickness=-1)
    else:
        raise ValueError("filter_type harus 'low' atau 'high'")

    # gunakan mask ke spektrum fekuensi
    f_transform_shifted_filtered = f_transform_shifted * mask

    # kembalikan pergeseran (inverse shift)
    f_ishift = np.fft.ifftshift(f_transform_shifted_filtered)

    # transformasi forier invers (IFFT)
    # ubah gambar dari domain frekuensi ke domain spasial
    img_back = np.fft.ifft2(f_ishift)
    filtered_image = np.abs(img_back)

    return original_image, filtered_image
    
