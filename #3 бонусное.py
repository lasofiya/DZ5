#3 бонусное
import numpy as np
from astropy.io import fits
from photutils import find_peaks
from astropy.table import Table
import json

# Загрузка автокорреляционной функции 
with fits.open('autocorrelation_function.fits') as hdul:
    autocorr_image = hdul[0].data

# Нахождение пиков с помощью photutils
peaks_table = find_peaks(autocorr_image, threshold=np.max(autocorr_image)*0.5, npeaks=3)
peaks_table.sort('peak_value', reverse=True)  # Сортировка по интенсивности пиков

# Расчет угловых расстояний между первым пиком и остальными
scale = 0.0206  # угловых секунд на пиксель
first_peak = peaks_table[0]
distances = []

for peak in peaks_table[1:]:
    distance_pixels = np.sqrt((first_peak['x_peak'] - peak['x_peak'])**2 + (first_peak['y_peak'] - peak['y_peak'])**2)
    distance_arcsec = distance_pixels * scale
    distances.append(distance_arcsec)

# Сохранение результатов в JSON
result = {'distances': distances}
with open('binary.json', 'w') as f:
    json.dump(result, f)

print("Результаты сохранены в binary.json")
