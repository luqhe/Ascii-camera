import numpy as np
import tkinter as tk
import cv2

# Video object
vid = cv2.VideoCapture(0)

# Chars_density
chars_density = r''' .:-=+*#%@'''

# Conversion functions
converter_vector = np.vectorize(lambda old_value: int((old_value * (len(chars_density)-1) / 255) + 1))
changer_vector = np.vectorize(lambda num: chars_density[num-1])

# Color inversion
inverter_vector = np.vectorize(lambda l_value: 255 - l_value)

def atualizar():
    ret, frame = vid.read()

    # Image reduction
    f_ndim = (int(frame.shape[1]*0.3), int(frame.shape[0]*0.3))
    frame = cv2.resize(frame, f_ndim)

    # Conversion to grayscale
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Grayscale array
    frame_arr = np.array(frame)

    # Color inversion
    frame_arr = inverter_vector(frame_arr)

    # Conversion from 255 range to range(chars_density)
    frame_arr = converter_vector(frame_arr)

    # Conversion from range(chars_density) to chars
    frame_arr = changer_vector(frame_arr)

    # Printing
    frame_arr = list(frame_arr)

    for i, row in enumerate(frame_arr): frame_arr[i] = '  '.join(row)
    
    frame_arr = '\n'.join(frame_arr)

    label.config(text=frame_arr)

    # Returning
    root.after(1, atualizar)

# Window
root = tk.Tk()
root.title("Ascii art")
root.config(bg='black')
label = tk.Label(root, bg='black', fg='white', font=('Courier', 1))
label.pack()

atualizar()
root.mainloop()

vid.release()
cv2.destroyAllWindows()