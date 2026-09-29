import numpy as np
from matplotlib.figure import Figure

# Vehicle & environment
M_VEHICLE = 226.0       # [kg] vehicle + driver mass
G = 9.81                # [m/s^2] gravity
CR = 0.012              # [-] rolling resistance coefficient
R_TIRE = 0.2032         # [m] effective loaded tire radius
D_AIR = 1.225           # [kg/m^3] air density
CD = 0.85                # [-] drag coefficient
A_FRONTAL = 2.2         # [m^2] frontal area
MU_PEAK = 1.4           # peak friction coefficient
KAPPA_PEAK = 0.60       # slip ratio at peak (~10%)
MU_SLIDE = 0.9          # sliding friction at high slip
N_DRIVEN = M_VEHICLE * G

# Powertrain
PRIMARY_REDUCTION = 1.974     # [-] engine primary reduction
FINAL_DRIVE = 3.727           # [-] final drive ratio
FINAL_DRIVE_NEW = 3.417       # [-] proposed final drive ratio
GEAR_RATIOS = {
    1: 2.687,
    2: 2.105,
    3: 1.761,
    4: 1.521,
    5: 1.347,
    6: 1.23,
}

ENGINE_REDLINE_RPM = 13000.0  # [rpm]
ENGINE_IDLE_RPM = 6000.0      # [rpm]
ENGINE_LAUNCH_RPM = 9000.0    # [rpm]
LAUNCH_DURATION = 1.3         # [s]

# Torque map
# Linearly interpolated between these points [rpm, lbft]
WHEEL_TORQUE_POINTS = np.array([
    [5050.0,45.7241379310345],
    [5100.0,46.9770114942529],
    [5150.0,52.0],
    [5200.0,53.0919540229885],
    [5250.0, 52.8620689655172],
    [5300.0,52.9655172413793],
    [5350.0,53.2298850574713],
    [5400.0,53.6436781609195],
    [5450.0,53.7931034482759],
    [5500.0,54.183908045977],
    [5550.0,54.4597701149425],
    [5600.0,54.6091954022988],
    [5650.0,54.6206896551724],
    [5700.0,54.7126436781609],
    [5750.0,54.632183908046],
    [5850.0,54.4252873563218],
    [5900.0,54.0919540229885],
    [5950.0,53.6781609195402],
    [6000.0,53.3563218390805],
    [6050.0,53.2068965517241],
    [6100.0,53.2413793103448],
    [6150.0,53.4597701149425],
    [6200.0,53.7931034482759],
    [6300.0,54.5172413793103],
    [6350.0,55.0344827586207],
    [6400.0,55.2873563218391],
    [6450.0,55.632183908046],
    [6500.0,55.6666666666667],
    [6550.0,55.5747126436782],
    [6600.0,55.4712643678161],
    [6630.0,55.4712643678161],
    [6650.0,55.4712643678161],
    [6700.0,55.1264367816092],
    [6750.0,54.9425287356322],
    [6800.0,54.8620689655172],
    [6850.0,54.6896551724138],
    [6900.0,54.4597701149425],
    [6950.0,54.2988505747126],
    [7000.0,54.4137931034483],
    [7020.0,54.4137931034483],
    [7050.0,54.4137931034483],
    [7100.0,54.0344827586207],
    [7150.0,53.2298850574713],
    [7200.0,52.551724137931],
    [7250.0,52.1724137931034],
    [7300.0,52.2528735632184],
    [7350.0,52.6896551724138],
    [7400.0,53.264367816092],
    [7500.0,54.3218390804598],
    [7550.0,54.632183908046],
    [7600.0,54.9080459770115],
    [7650.0,55.2643678160919],
    [7700.0,55.551724137931],
    [7750.0,55.4597701149425],
    [7800.0,54.8620689655172],
    [7850.0,54.0114942528736],
    [7900.0,53.4367816091954],
    [7950.0,53.2528735632184],
    [8000.0,53.3908045977011],
    [8100.0,54.0459770114943],
    [8150.0,54.4367816091954],
    [8200.0,54.5287356321839],
    [8250.0,54.735632183908],
    [8300.0,55.0229885057471],
    [8350.0,55.3563218390805],
    [8400.0,55.2758620689655],
    [8450.0,54.9885057471264],
    [8500.0,54.7471264367816],
    [8550.0,54.6896551724138],
    [8600.0,54.9655172413793],
    [8650.0,55.5747126436782],
    [8700.0,56.4252873563218],
    [8750.0,57.3448275862069],
    [8800.0,58.5862068965517],
    [8850.0,59.3333333333333],
    [8900.0,60.2298850574713],
    [9000.0,61.0],
    [9050.0,61.0344827586207],
    [9100.0,61.1149425287356],
    [9150.0,61.1609195402299],
    [9200.0,61.3793103448276],
    [9250.0,62.1149425287356],
    [9300.0,62.7471264367816],
    [9400.0,64.8505747126437],
    [9500.0,66.7011494252874],
    [9550.0,66.7011494252874],
    [9600.0,66.4827586206897],
    [9650.0,65.8045977011494],
    [9700.0,65.2413793103448],
    [9750.0,64.9885057471264],
    [9800.0,65.0919540229885],
    [9850.0,65.2298850574713],
    [9950.0,65.9310344827586],
    [10000.0,66.3218390804598],
    [10050.0,66.3103448275862],
    [10100.0,65.7586206896552],
    [10200.0,63.8275862068965],
    [10250.0,63.2873563218391],
    [10300.0,63.0574712643678],
    [10350.0,63.0344827586207],
    [10450.0,63.3908045977011],
    [10500.0,63.6666666666667],
    [10550.0,63.8735632183908],
    [10600.0,63.632183908046],
    [10650.0,62.9080459770115],
    [10700.0,61.8965517241379],
    [10750.0,60.9885057471264],
    [10800.0,60.4827586206897],
    [10850.0,60.2068965517241],
    [10900.0,60.1379310344828],
    [10950.0,60.1724137931034],
    [11000.0,60.0689655172414],
    [11050.0,59.9080459770115],
    [11100.0,59.5977011494253],
    [11150.0,59.1034482758621],
    [11200.0,58.367816091954],
    [11250.0,57.5057471264368],
    [11350.0,56.2183908045977],
    [11400.0,55.8620689655172],
    [11450.0,55.6206896551724],
    [11500.0,55.448275862069],
    [11600.0,55.0344827586207],
    [11650.0,54.7471264367816],
    [11700.0,54.3333333333333],
    [11850.0,52.7816091954023],
    [11900.0,52.367816091954],
    [11950.0,52.1609195402299],
    [12000.0,52.0689655172414],
    [12050.0,52.0],
    [12100.0,51.8275862068966],
    [12150.0,51.5402298850575],
    [12200.0,51.1034482758621],
    [12300.0,49.8965517241379],
    [12350.0,49.1724137931034],
    [12400.0,48.5747126436782],
    [12450.0,48.1379310344828],
    [12500.0,47.8850574712644],
    [12600.0,47.4827586206897],
    [12650.0,47.2183908045977],
    [12700.0,46.8620689655172],
    [12750.0,46.3908045977011],
    [12800.0,45.8045977011494],
    [12900.0,44.551724137931],
    [12950.0, 44.0229885057471],
    [13000.0, 43.6551724137931]
])

# Shifting & control
SHIFT_DELAY = 0.225       # [s] duration of no drive force during an upshift
USE_AUTO_SHIFT = True    # if False, no shifting: stay in 1st gear

# Per-gear upshift RPM thresholds
SHIFT_RPM_THRESHOLDS = {
    1: 11000.0,
    2: 12500.0,
    3: 12500.0,
    4: 12500.0,
    5: 13000.0,
    6: None,     # no upshift from 6th
}

# Simulation control
DT = 0.005                 # [s] time step
T_MAX = 10.0             # [s] safety time limit

# Distance Based
TARGET_DISTANCE = 75.0   # [m] acceleration event distance (FSAE-style)

# Or Speed Based
TARGET_SPEED_KMH = 100.0           # [km/h] target speed
TARGET_SPEED_MS = TARGET_SPEED_KMH / 3.6  # [m/s]

class carInfo:
    def __init__(self, 
                 mass = M_VEHICLE, cr = CR, tireRad = R_TIRE, 
                 cd = CD, af = A_FRONTAL, mu_peak = MU_PEAK, 
                 kappa_peak = KAPPA_PEAK, mu_slide = MU_SLIDE, fd1 = FINAL_DRIVE, 
                 fd2 = FINAL_DRIVE_NEW, sd = SHIFT_DELAY):
        self.mass = mass
        self.cr = cr
        self.tireRad = tireRad
        self.cd = cd
        self.af = af
        self.mu_peak = mu_peak
        self.kappa_peak = kappa_peak
        self.mu_slide = mu_slide
        self.n_driven = self.mass * G

        self.fd1 = fd1
        self.fd2 = fd2

        self.sd = sd

def wheel_torque_from_rpm(rpm: float) -> float:
    """
    Return wheel torque [N·m] at a given engine speed [rpm],
    using linear interpolation of ENGINE_TORQUE_POINTS_LBFT (in lb·ft).
    """
    rpms = WHEEL_TORQUE_POINTS[:, 0]
    torques_lbft = WHEEL_TORQUE_POINTS[:, 1]

    # Clamp rpm inside range
    if rpm <= rpms[0]:
        tq_lbft = torques_lbft[0]
    elif rpm >= rpms[-1]:
        tq_lbft = torques_lbft[-1]
    else:
        tq_lbft = float(np.interp(rpm, rpms, torques_lbft))

    # Convert to N·m for the rest of the model
    return tq_lbft * 1.35581795

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

def pacejka_traction_limited_force(F_drive_ideal: float, kappa: float, carInfo):
    C = 5.83         # Shape Factor
    D = 3900         # Peak Factor
    b = 600          # Stiffness Factor B = change of stiffness with slip · Fz / (C · D)
    E = 0.993        # Curvature Factor
    F_max = D * np.sin(C * np.arctan(b * kappa - E * (b * kappa - np.arctan(b * kappa))))
    return float(np.clip(F_drive_ideal, -F_max, F_max))

def simulate_run(carInfo):
    deltaT = 0.0
    velocity = 0.0
    deltaX = 0.0
    gear = 2
    shifting = False
    shift_time_left = 0.0
    next_gear = gear

    # Data recording lists
    ts = []
    xs = []
    vs = []
    axs = []
    gears = []
    eng_rpms = []
    drive_forces = []

    while deltaX < TARGET_DISTANCE and deltaT < T_MAX:
    #while velocity < TARGET_SPEED_MS and deltaT < T_MAX:
        # Wheel speed from vehicle speed
        omega_w = velocity / carInfo.tireRad  # [rad/s]
        gear_ratio = GEAR_RATIOS[gear]

        if deltaT < LAUNCH_DURATION:
            # During launch: hold engine at (roughly) fixed high RPM
            engine_rpm = np.clip(ENGINE_LAUNCH_RPM, ENGINE_IDLE_RPM, ENGINE_REDLINE_RPM)
        else:
            # After launch: fully coupled engine–wheel kinematics
            engine_rad_per_s = omega_w * PRIMARY_REDUCTION * gear_ratio * carInfo.fd1
            engine_rpm = engine_rad_per_s * 60.0 / (2.0 * np.pi)
            engine_rpm = np.clip(engine_rpm, ENGINE_IDLE_RPM, ENGINE_REDLINE_RPM)

        # Automatic upshift logic (initiate shift)
        if USE_AUTO_SHIFT and not shifting:
            shift_rpm = SHIFT_RPM_THRESHOLDS[gear]
            if shift_rpm is not None and engine_rpm >= shift_rpm and gear < max(GEAR_RATIOS.keys()):
                # Start shift
                shifting = True
                shift_time_left = carInfo.sd
                next_gear = gear + 1

        # Compute drive force
        if shifting:
            F_drive = 0.0
            shift_time_left -= DT
            if shift_time_left <= 0.0:
                shifting = False
                gear = next_gear
        else:
            # Engine torque at current rpm
            T_e = wheel_torque_from_rpm(engine_rpm)

            # Driveline torque to wheel
            gear_ratio = GEAR_RATIOS[gear]
            T_in = T_e * PRIMARY_REDUCTION * gear_ratio * carInfo.fd1

            # Ideal wheel thrust
            F_drive_ideal = T_in / carInfo.tireRad
            
            # Longitudinal slip ratio (simple definition, avoid div-by-zero)
            if velocity < 0.1:  # near standstill, approximate high slip
                kappa = 1.0
            else:
                kappa = (omega_w - velocity) / max(velocity, 1e-3)

            # Apply simple traction limit
            F_drive = pacejka_traction_limited_force(F_drive_ideal, kappa, carInfo)

        # Resistive forces
        F_drag = 0.5 * D_AIR * velocity**2 * carInfo.cd * carInfo.af
        F_roll = carInfo.cr * carInfo.mass * G

        # Longitudinal acceleration
        a_x = (F_drive - F_drag - F_roll) / carInfo.mass

        # Integrate state (simple Euler)
        velocity = velocity + a_x * DT
        if velocity < 0.0:
            velocity = 0.0
        deltaX = deltaX + velocity * DT
        deltaT = deltaT + DT

        # Record data
        ts.append(deltaT)
        xs.append(deltaX)
        vs.append(velocity)
        axs.append(a_x)
        gears.append(gear)
        eng_rpms.append(engine_rpm)
        drive_forces.append(F_drive)

    results = {
        "t": np.array(ts),
        "x": np.array(xs),
        "v": np.array(vs),
        "a": np.array(axs),
        "gear": np.array(gears),
        "engine_rpm": np.array(eng_rpms),
        "F_drive": np.array(drive_forces),
        "t_final": deltaT,
        "x_final": deltaX,
        "v_final": velocity,
        "final_drive": carInfo.fd1,
        "shift_delay": carInfo.sd,
    }
    return results

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

def plot_results(axes, results):
    t = results["t"]
    v = results["v"]
    a = results["a"]
    gear = results["gear"]
    rpm = results["engine_rpm"]

    ax0, ax1, ax2, ax3 = axes

    # Speed
    ax0.plot(t, v * 3.6, label="Speed", lw=2)
    ax0.set_ylabel("Speed [km/h]")
    ax0.grid(True)

    # Acceleration in Gs
    ax1.plot(t, a / G, label="Accel", color="C1", lw=2)  # G = 9.81 defined at top
    ax1.set_ylabel("a_x [G]")
    ax1.grid(True)
    
    # Engine RPM
    ax2.plot(t, rpm, label="Engine RPM", color="C3", lw=2)
    ax2.set_ylabel("RPM")
    ax2.grid(True)
    ax2.set_ylim(3000, ENGINE_REDLINE_RPM * 1.1)

    # Gear
    ax3.step(t, gear, where="post", label="Gear", color="C2", lw=2)
    ax3.set_ylabel("Gear")
    ax3.set_xlabel("Time [s]")
    ax3.grid(True)

def plot_torque_curve(ax):
    """Plot the engine torque curve using engine_torque_from_rpm()."""
    # Base RPM points from the map (for markers)
    rpms_base = WHEEL_TORQUE_POINTS[:, 0]
    tq_lbft_base = WHEEL_TORQUE_POINTS[:, 1]

    # Smooth RPM range
    rpm_smooth = np.linspace(rpms_base[0], rpms_base[-1], 300)

    # Use the sim's interpolation function (returns N·m), then convert to lb·ft
    tq_nm_smooth = np.array([wheel_torque_from_rpm(r) for r in rpm_smooth])
    tq_lbft_smooth = tq_nm_smooth / 1.35581795

    ax.set_xlim(5000, 14000)
    ax.set_ylim(0, 100)
    ax.plot(rpm_smooth, tq_lbft_smooth, label="Torque", color="C0")
    ax.scatter(rpms_base, tq_lbft_base, color="C1", label="Input map points")
    ax.set_xlabel("Engine speed [rpm]")
    ax.set_ylabel("Wheel torque [lb·ft]")
    ax.set_title("Input Wheel Torque Map")
    ax.grid(True)
    ax.legend()

def plot_tire_curve(ax, carInfo):
    """Plot the frictional force of the tires across the power"""
    kappa_range = [0, 4]

    # Smooth kappa range
    kappa_smooth = np.linspace(kappa_range[0], kappa_range[-1], 300)

    # Use the sim's grip function (N)
    grip_N_smooth = np.array([pacejka_traction_limited_force(100000, r, carInfo) for r in kappa_smooth])

    ax.plot(kappa_smooth * 100, grip_N_smooth, color="C3", lw=3)
    ax.set_xlabel("Slip Ratio [%]")
    ax.set_xlim(0, 400)
    ax.set_ylabel("Friction force [N]")
    ax.set_ylim(0, 6000)
    ax.set_title("Friction Limited Force of Tires")
    ax.grid(True)

def possible_final_drives():
    big_gears = np.linspace(35, 66, 66 - 35)
    little_gears = np.linspace(14, 18, 18 - 14)
    ratios = []

    for bgear in big_gears:
        for lgear in little_gears:
            ratio = float(bgear / lgear)
            ratios.append(ratio)
    ratios.sort()
    for i in range(len(ratios)-1, -1, -1):
        if np.abs(ratios[i] - ratios[i-1]) < 0.005:
            del ratios[i]

    return ratios

def highlight_fds(ax, carInfo):
    # Highlight specific FD values at nominal SHIFT_DELAY
    for fd, color, marker, label in [
        (FINAL_DRIVE, "r", "o", "11:41"),
        (FINAL_DRIVE_NEW, "g", "o", "12:41"),
        (3.182, "b", "*", "11:35"),
        (2.917, "c", "*", "12:35"),
    ]:
        carInfo.fd1 = fd
        carInfo.sd = SHIFT_DELAY
        res = simulate_run(carInfo)
        ax.plot(res["t_final"], fd, marker + color, label=label)

def plot_FD_curves(ax, carInfo):
    """Plot FD sweep into the provided Axes ax."""
    times = []
    ratios = possible_final_drives()

    for r in ratios:
        carInfo.fd1 = r
        res_fd = simulate_run(carInfo)
        times.append(res_fd["t_final"])
    ax.plot(times, ratios, "k", label="FD sweep")

    highlight_fds(ax, carInfo)
    ax.set_ylabel("Final drive ratio")
    ax.set_ylim(2, 4.5)
    ax.set_xlabel(f"Time to {TARGET_DISTANCE:.0f} m [s]")
    ax.set_xlim(3.5, 6)
    ax.grid(True)
    ax.set_title(f"Optimized Final Drive Ratios\nshift delay: {carInfo.sd*1000:.0f} ms")
    ax.legend()

def plot_SD_FD_curves(ax, carInfo):
    """Plot multiple FD curves for different shift delays into ax."""
    fds = possible_final_drives()
    shift_delays = np.linspace(0.09, carInfo.sd, 3)
    sd1 = carInfo.sd
    
    for sd in shift_delays:
        times = []
        carInfo.sd = sd
        for fd in fds:
            carInfo.fd1 = fd
            res_fd = simulate_run(carInfo)
            times.append(res_fd["t_final"])
        ax.plot(times, fds, label=f"SD: {sd*1000:.0f} ms")

    carInfo.sd = sd1
    highlight_fds(ax, carInfo)
    ax.set_ylabel("Final drive ratio")
    ax.set_ylim(2.5, 4.5)
    ax.set_xlabel(f"Time to {TARGET_DISTANCE:.0f} m [s]")
    ax.set_xlim(4, 5)
    ax.grid(True)
    ax.set_title("Shift delay effect on final drive")
    ax.legend()