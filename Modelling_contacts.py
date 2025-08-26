import numpy as np, pandas as pd, matplotlib.pyplot as plt

# ---- CONFIG ----
BASE = 60                 # baseline level
PEAKS = [(13, 40), (20, 10)]   # (hour_of_peak, amplitude)
USE = "cos"               # "cos" → peaks at hour h; "sin" → peaks at ~h+6
MINUTES = 30              # interval size

# ---- BUILD CURVE ----
t = np.arange(0, 24, MINUTES/60)          # hours: 0..24 step by interval
w = 2*np.pi/24
y = np.full_like(t, BASE, dtype=float)
for h, A in PEAKS:
    y += A * (np.cos(w*(t - h)) if USE=="cos" else np.sin(w*(t - h)))

df = pd.DataFrame({"hour": t, "level": y})

# ---- OPTIONAL: simulate arrivals around the curve (Poisson) ----
rng = np.random.default_rng(7)
df["arrivals_sim"] = rng.poisson(lam=np.clip(df["level"], 0, None))

# ---- PLOT ----
plt.figure(figsize=(7,4))
plt.plot(df["hour"], df["level"], label=f"expected ({USE})", lw=2)
plt.scatter(df["hour"], df["arrivals_sim"], s=12, alpha=.6, label="simulated arrivals")
for h,_ in PEAKS: plt.axvline(h, ls="--", lw=1, alpha=.4)
plt.xticks(range(0,25,2)); plt.xlabel("Hour of day"); plt.ylabel("Level")
plt.title("Intraday pattern with specified peak hours")
plt.legend(); plt.grid(True, alpha=.3); plt.tight_layout(); plt.show()

# Save 
df.to_csv("intraday_pattern.csv", index=False)


