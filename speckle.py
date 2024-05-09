import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from scipy.fft import fft2, ifft2, fftshift
from scipy.ndimage import rotate
from numpy.ma import masked_array

# Загрузка данных из файла FITS
with fits.open('speckledata.fits') as hdul:
    data = hdul[2].data  # предполагаем, что данные находятся во втором HDU

# 1. Вычисление усреднённого по времени изображения
mean_image = np.mean(data, axis=0)
plt.imshow(mean_image, cmap='gray')
plt.colorbar()
plt.title('Mean Image')
plt.savefig('mean.png')
plt.clf()

# 2. Вычисление среднего спектра мощности
fft_images = fft2(data, axes=(-2, -1))
power_spectrum = np.abs(fft_images)**2
mean_power_spectrum = np.mean(power_spectrum, axis=0)
plt.imshow(np.log1p(fftshift(mean_power_spectrum)), cmap='gray')
plt.colorbar()
plt.title('Mean Fourier Power Spectrum')
plt.savefig('fourier.png')
plt.clf()

# 3. Усреднение спектра мощности по углам
angles = np.linspace(0, 360, 36, endpoint=False)
rotated_spectra = [rotate(mean_power_spectrum, angle, reshape=False) for angle in angles]
average_spectrum = np.mean(rotated_spectra, axis=0)
plt.imshow(np.log1p(fftshift(average_spectrum)), cmap='gray')
plt.colorbar()
plt.title('Averaged Fourier Image')
plt.savefig('rotaver.png')
plt.clf()

# 4. Зануление всех частот выше частоты отсечения
radius = 5
y, x = np.ogrid[:data.shape[1], :data.shape[2]]
center = (data.shape[1] // 2, data.shape[2] // 2)
mask = (y - center[0])**2 + (x - center[1])**2 > radius**2
filtered_spectrum = masked_array(average_spectrum, mask=mask).filled(0)

# 5. Применение обратного двумерного преобразования Фурье
restored_image = ifft2(fftshift(filtered_spectrum)).real
normalized_image = (restored_image - np.min(restored_image)) / (np.max(restored_image) - np.min(restored_image))

# Сохранение и визуализация конечного изображения
plt.imshow(normalized_image, cmap='gray')
plt.colorbar()
plt.title('Restored Binary Image')
plt.savefig('binary.png')
plt.show()
