import numpy as np
import matplotlib.pyplot as plt

# --- Load your ET arrays ---
ET1 = np.load("/Users/moasjoberg/Documents/Turbulence_cource/Turbulence_course/ET_main_data1.npy")
ET2 = np.load("/Users/moasjoberg/Documents/Turbulence_cource/Turbulence_course/ET_main_data2.npy")

# --- Time axis (10 min resolution = 144 steps per day) ---
time_hours = np.arange(0, 24, 10/60)   # 0..24 in 0.167h steps

# --- Labels for your three crop heights ---
heights = ["12 cm", "33 cm", "60 cm"]

# --- Plot ---
fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

for i in range(3):
    axes[i].plot(time_hours, ET1[i], label="Main_data1", linewidth=2)
    axes[i].plot(time_hours, ET2[i], label="Main_data2", linewidth=2, alpha=0.8)
    axes[i].set_ylabel(f"ET [{heights[i]}]\n(mm h$^{{-1}}$)")
    axes[i].legend()
    axes[i].grid(True, linestyle="--", alpha=0.5)

axes[-1].set_xlabel("Time [hours]")
fig.suptitle("Evapotranspiration Comparison at Three Crop Heights", fontsize=14)
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()
