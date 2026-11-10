import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. Load CSV data
csv_file = "raw_data_sensor_bottom.csv"
print(f"[INFO] Reading {csv_file}...")
df = pd.read_csv(csv_file)

# Total simulated events from main.conf
N_TOTAL_EVENTS = 20000

# 2. Residual distance cut (|residual_x| <= 200 um)
df_linked = df[df["residual_x_um"].abs() <= 200.0]

# 3. Threshold range: 6000e to 50000e (step 1000e)
thresholds = np.arange(6000, 51000, 1000)

data_list = []

print("\n" + "="*58)
print(f"{'Threshold (e-)':<16} | {'Passed':<8} | {'Efficiency':<12} | {'Error':<10}")
print("="*58)

for thr in thresholds:
    n_passed = int((df_linked["cluster_charge_e"] >= thr).sum())
    eff = n_passed / N_TOTAL_EVENTS
    err = np.sqrt(eff * (1.0 - eff) / N_TOTAL_EVENTS)
    
    data_list.append({
        "threshold_e": thr,
        "n_passed": n_passed,
        "efficiency": eff,
        "error": err
    })
    
    # Har 2000e par terminal mein print karega
    if thr % 2000 == 0:
        print(f"{thr:<16} | {n_passed:<8} | {eff:<12.5f} | {err:<10.5f}")

print("="*58)

# Results ko CSV mein save karein (aglay derivative step ke liye)
results_df = pd.DataFrame(data_list)
results_df.to_csv("scurve_points.csv", index=False)
print("[INFO] Results saved to 'scurve_points.csv'")

# 4. Plot S-Curve
plt.figure(figsize=(9, 6))
plt.errorbar(
    results_df["threshold_e"],
    results_df["efficiency"],
    yerr=results_df["error"],
    fmt="s-",
    color="crimson",
    markersize=4,
    capsize=2,
    label=f"Bottom Sensor (U = 300 V, N={N_TOTAL_EVENTS})"
)

plt.xlabel(r"Threshold ($e^-$)", fontsize=13)
plt.ylabel("Cluster efficiency", fontsize=13)
plt.title("CMS 2S Prototype: Cluster Efficiency vs Threshold", fontsize=14)
plt.grid(True, which="both", linestyle="--", alpha=0.5)
plt.ylim(0.0, 1.05)
plt.xlim(5000, 52000)
plt.legend(fontsize=12)

plot_name = "s_curve_efficiency.png"
plt.tight_layout()
plt.savefig(plot_name, dpi=300)
print(f"[INFO] Plot saved to '{plot_name}'\n")

