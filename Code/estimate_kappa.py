import numpy as np
import pandas as pd
from scipy.ndimage import gaussian_filter1d
from scipy.optimize import curve_fit

def simulate_trajectory(kappa, x0, y0, theta0, velocities, dt=1):
    recon_x = [x0]
    recon_y = [y0]
    theta = theta0
    for v in velocities:
        theta += -kappa * v * dt
        new_x = recon_x[-1] + v * np.cos(theta) * dt
        new_y = recon_y[-1] + v * np.sin(theta) * dt
        recon_x.append(new_x)
        recon_y.append(new_y)
    return np.array(recon_x), np.array(recon_y)

def compute_mse(x1, y1, x2, y2):
    min_len = min(len(x1), len(x2))
    return np.mean((x1[:min_len] - x2[:min_len])**2 + (y1[:min_len] - y2[:min_len])**2)

def estimate_kappa_gridsearch(df, k_range=np.linspace(-0.05, 0.05, 500)):
    df = df.dropna(subset=["velocity_px", "x", "y"]).reset_index(drop=True)
    x = df["x"].values
    y = df["y"].values
    v = df["velocity_px"].values
    dx0 = x[1] - x[0]
    dy0 = y[1] - y[0]
    theta0 = np.arctan2(dy0, dx0)

    best_kappa = None
    best_mse = float("inf")
    best_recon = (None, None)

    for kappa in k_range:
        rx, ry = simulate_trajectory(kappa, x[0], y[0], theta0, v)
        error = compute_mse(x, y, rx, ry)
        if error < best_mse:
            best_mse = error
            best_kappa = kappa
            best_recon = (rx, ry)

    return best_kappa, best_mse, best_recon

def general_theta_model(t, A, theta0):
    return 2 * np.arctan(np.exp(-A * t)) + theta0 - np.pi

def estimate_kappa_from_heading(df, phi_deg, phi_c_deg, v0, max_frames=35, sigma=2):
    df = df.dropna(subset=["x", "y"]).reset_index(drop=True)
    x = df["x"].values
    y = df["y"].values

    dx = np.diff(x)
    dy = np.diff(y)
    theta_raw = np.arctan2(dy, dx)
    theta_unwrapped = np.unwrap(theta_raw)
    theta_smooth = gaussian_filter1d(theta_unwrapped, sigma=sigma)
    theta_crop = theta_smooth[:max_frames]
    t_crop = np.arange(len(theta_crop))

    try:
        popt, _ = curve_fit(general_theta_model, t_crop, theta_crop, p0=[0.01, np.pi / 2])
        A, theta0 = popt
    except RuntimeError:
        return None

    phi = np.deg2rad(phi_deg)
    phi_c = np.deg2rad(phi_c_deg)
    kappa = (A * np.sin(phi_c)) / (v0 * np.sin(phi))
    return kappa
