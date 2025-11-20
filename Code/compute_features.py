import numpy as np
import pandas as pd
from scipy.ndimage import gaussian_filter1d

def trial_summary(trial_name, position, orientation, velocities, accelerations, displacement, directional_bias, startup_acc):
    return {
        'trial': trial_name,
        'position': position,
        'orientation': orientation,
        'mean_velocity': np.mean(velocities) if len(velocities) > 0 else np.nan,
        'std_velocity': np.std(velocities) if len(velocities) > 0 else np.nan,
        'mean_acceleration': np.mean(accelerations) if len(accelerations) > 0 else np.nan,
        'std_acceleration': np.std(accelerations) if len(accelerations) > 0 else np.nan,
        'startup_acceleration': startup_acc if startup_acc is not None else np.nan,
        'displacement': displacement if not np.isnan(displacement) else np.nan,
        'directional_bias': directional_bias if not np.isnan(directional_bias) else np.nan
    }

def summarize_all_trials(df, fps=60, scale=0.17):
    summaries = []

    for trial_name, trial_df in df.groupby("trial"):
        position = trial_df["position"].iloc[0]
        orientation = trial_df["orientation"].iloc[0]

        xy = trial_df.sort_values("frame")[["x", "y"]].dropna().values * scale  # to cm!

        if len(xy) < 3:
            continue

        velocities = np.linalg.norm(np.diff(xy, axis=0), axis=1) * fps
        velocities_smoothed = gaussian_filter1d(velocities, sigma=1)
        accelerations = np.diff(velocities_smoothed)

        startup_acc = next((v for v in velocities if v > 0), np.nan)
        displacement = np.linalg.norm(xy[-1] - xy[0])
        directional_bias = xy[-1, 1] - xy[0, 1]  # vertical**** offset (cm)

        summary = trial_summary(
            trial_name, position, orientation,
            velocities, accelerations, displacement, directional_bias, startup_acc
        )

        summaries.append(summary)

    return pd.DataFrame(summaries)