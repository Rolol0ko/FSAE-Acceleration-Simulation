import numpy as np

# Distance Based
TARGET_DISTANCE = 75.0   # [m] acceleration event distance (FSAE-style)

# Or Speed Based
TARGET_SPEED_KMH = 100.0                  # [km/h] target speed
TARGET_SPEED_MS = TARGET_SPEED_KMH / 3.6  # [m/s]

# Old tyre friction model
def tire_mu_from_slip(kappa: float, carInfo) -> float:
    """
    Very simple longitudinal mu(kappa) curve.
    Curve rises to a peak then falls slightly.
    """
    kappa = max(kappa, 0.0)

    if kappa <= carInfo.kappa_peak:
        # Linear build-up to peak
        return carInfo.mu_peak * (kappa / carInfo.kappa_peak)
    else:
        # Exponential decay toward slide friction
        decay = np.exp(-(kappa - carInfo.kappa_peak) / 0.2)
        return carInfo.mu_slide + (carInfo.mu_peak - carInfo.mu_slide) * decay

def basic_traction_limited_force(F_drive_ideal: float, kappa: float, carInfo) -> float:
    """
    Traction limit using a simple mu(kappa) curve.
    """
    mu = tire_mu_from_slip(kappa, carInfo)
    F_max = mu * carInfo.n_driven
    return float(np.clip(F_drive_ideal, -F_max, F_max))

# Printing to cmdline
def print_distance_summary(results):
    t_final = results["t_final"]
    v_final = results["v_final"]
    print(f"Final distance: {TARGET_DISTANCE:.1f} m")
    print(f"Time to {TARGET_DISTANCE:.1f} m: {t_final:.3f} s")
    print(f"Final speed: {v_final * 3.6:.1f} km/h")

def print_time_summary(results):
    t_final = results["t_final"]
    v_final = results["v_final"]
    x_final = results["x_final"]
    print(f"Target: 0 -> {TARGET_SPEED_KMH:.0f} km/h")
    print(f"Time to {TARGET_SPEED_KMH:.0f} km/h: {t_final:.3f} s")
    print(f"Speed at end: {v_final * 3.6:.1f} km/h")
    print(f"Distance covered: {x_final:.1f} m")
