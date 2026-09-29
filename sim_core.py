import numpy as np
from matplotlib.figure import Figure

# Enviroment
G = 9.81                        # [m/s^2] gravity
AIR_DENSITY = 1.225             # [kg/m^3] air density

# Vehicle
MASS_CAR = 226.0                # [kg] vehicle + driver mass
ROLLING_RESISTANCE_C = 0.012    # [-] rolling resistance coefficient
TYRE_RADIUS = 0.2032            # [m] effective loaded tire radius
DRAG_C = 0.85                   # [-] drag coefficient
FRONTAL_AREA = 2.0              # [m^2] frontal area

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
TOTAL_RATIO_ON_DYNO = FINAL_DRIVE * GEAR_RATIOS[6] * PRIMARY_REDUCTION

ENGINE_REDLINE_RPM = 13500.0  # [rpm]
ENGINE_IDLE_RPM = 6000.0      # [rpm]
ENGINE_LAUNCH_RPM = 9000.0    # [rpm]

# Torque map (Linearly interpolated between these points [rpm, Nm])
WHEEL_TORQUE_POINTS = np.array([
    [5050.0,45.7241379310345],
    [5100.0,46.9770114942529],
    [5150.0,52.0],
    [5200.0,53.0919540229885],
    [5250.0,52.8620689655172],
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
    [12950.0,44.0229885057471],
    [13000.0,43.6551724137931]
])

# Shifting
SHIFT_DELAY = 0.225       # [s] duration of no drive force during an upshift
CHANGE_GEARS = True     # [bool] Shift or not

# Upshift RPM thresholds
SHIFT_RPM_THRESHOLDS = {
    1: 11000.0,
    2: 12500.0,
    3: 12500.0,
    4: 12500.0,
    5: 13000.0,
    6: None,        # no upshift from 6th
}

# Simulation control
TIME_STEP = 0.005      # [s] time step
MAX_TIME = 10.0         # [s] safety time limit

# Distance Based
TARGET_DISTANCE = 75.0  # [m] acceleration event distance

# FD SD Graph limits
FD_LOW_LIMIT = 2
FD_HIGH_LIMIT = 7
TIME_LOW_LIMIT = 3.5
TIME_HIGH_LIMIT = 6

class carInfo:
    def __init__(self, 
                 mass = MASS_CAR,
                 cr = ROLLING_RESISTANCE_C,
                 tireRad = TYRE_RADIUS, 
                 cd = DRAG_C,
                 af = FRONTAL_AREA,
                 fd = FINAL_DRIVE, 
                 sd = SHIFT_DELAY,
                 launch_rpm = ENGINE_LAUNCH_RPM):
        self.mass = mass
        self.rolling_resistance_c = cr
        self.tyre_radius = tireRad
        self.drag_c = cd
        self.frontal_area = af
        self.final_drive = fd
        self.shift_delay = sd
        self.launch_rpm = launch_rpm

def engine_tq_from_rpm(rpm: float) -> float:
    """
    Return wheel torque [Nm] at a given engine speed [rpm],
    using linear interpolation.
    """
    rpms = WHEEL_TORQUE_POINTS[:, 0]
    torques_Nm = WHEEL_TORQUE_POINTS[:, 1]

    # Clamp rpm inside range
    if rpm <= rpms[0]:
        tq_Nm = torques_Nm[0]
    elif rpm >= rpms[-1]:
        tq_Nm = torques_Nm[-1]
    else:
        tq_Nm = float(np.interp(rpm, rpms, torques_Nm))

    # wheel to engine
    tq_Nm = tq_Nm * TOTAL_RATIO_ON_DYNO

    return tq_Nm

def pacejka_traction_limited_force(F_drive_ideal: float, kappa: float):
    C = 5.83         # Shape Factor
    D = 4100         # Peak Factor
    B = 600          # Stiffness Factor B = change of stiffness with slip · Fz / (C · D)
    E = 0.993        # Curvature Factor
    F_max = D * np.sin(C * np.arctan(B * kappa - E * (B * kappa - np.arctan(B * kappa))))
    return float(np.clip(F_drive_ideal, -F_max, F_max))

def simulate_run(carInfo):
    elapsed_time = 0.0              # Total time passed
    velocity = 0.0                  # Velocity [m/s]
    elapsed_distance = 0.0          # Total distance passed
    current_gear = 2                # Current gear in use
    shifting = False                # Activley shifting
    shift_time_left = 0.0           # Time left shifting
    engine_rpm = ENGINE_IDLE_RPM    # Engine RPM

    # Data recording lists
    ts = []
    ds = []
    vs = []
    axs = []
    gears = []
    eng_rpms = []
    drive_forces = []

    while elapsed_distance < TARGET_DISTANCE and elapsed_time < MAX_TIME:
        # Wheel speed from vehicle speed
        angular_velocity = velocity / carInfo.tyre_radius  # [rad/s]

        # Engine speed from wheel speed
        gear_ratio = GEAR_RATIOS[current_gear]
        engine_rad_per_s = angular_velocity * PRIMARY_REDUCTION * gear_ratio * carInfo.fd1
        real_engine_rpm = engine_rad_per_s * 60.0 / (2.0 * np.pi)

        if real_engine_rpm < engine_rpm and current_gear == 2 and shifting == False:
            # During launch: hold engine at fixed RPM
            engine_rpm = np.clip(carInfo.launch_rpm, ENGINE_IDLE_RPM, ENGINE_REDLINE_RPM)
        else:
            # After launch: use real speed
            engine_rpm = np.clip(real_engine_rpm, ENGINE_IDLE_RPM, ENGINE_REDLINE_RPM)

        # Shifting logic
        if CHANGE_GEARS == True and not shifting:
            shift_rpm = SHIFT_RPM_THRESHOLDS[current_gear]
            if shift_rpm is not None and engine_rpm >= shift_rpm and current_gear < max(GEAR_RATIOS.keys()):
                # Start shift
                shifting = True
                shift_time_left = carInfo.shift_delay
                next_gear = current_gear + 1

        if shifting:
            F_drive = 0.0
            shift_time_left -= TIME_STEP
            if shift_time_left <= 0.0:
                shifting = False
                current_gear = next_gear

        # Compute drive force
        else:
            # Engine torque at current rpm
            T_e = engine_tq_from_rpm(engine_rpm)

            # Driveline torque to wheel
            gear_ratio = GEAR_RATIOS[current_gear]
            T_in = T_e * PRIMARY_REDUCTION * gear_ratio * carInfo.fd1

            # Ideal wheel thrust
            drive_thrust_ideal = T_in / carInfo.tyre_radius
            
            # slip ratio (simple definition, avoid div-by-zero)
            if real_engine_rpm < engine_rpm and current_gear == 2 and shifting == False:  # during launch, approximate high slip
                kappa = 4.0
            else:
                kappa = (angular_velocity - velocity) / max(velocity, 1e-3)

            # Apply traction limit
            F_drive = pacejka_traction_limited_force(drive_thrust_ideal, kappa)

        # Resistive forces
        F_drag = 0.5 * AIR_DENSITY * velocity**2 * carInfo.drag_c * carInfo.frontal_area
        F_roll = carInfo.rolling_resistance_c * carInfo.mass * G

        # Longitudinal acceleration
        a_x = (F_drive - F_drag - F_roll) / carInfo.mass

        # Integrate state
        velocity = velocity + a_x * TIME_STEP
        if velocity < 0.0:
            velocity = 0.0
        elapsed_distance = elapsed_distance + velocity * TIME_STEP
        elapsed_time = elapsed_time + TIME_STEP

        # Record data into 
        ts.append(elapsed_time)
        ds.append(elapsed_distance)
        vs.append(velocity)
        axs.append(a_x)
        gears.append(current_gear)
        eng_rpms.append(engine_rpm)
        drive_forces.append(F_drive)

    results = {
        "t": np.array(ts),
        "x": np.array(ds),
        "v": np.array(vs),
        "a": np.array(axs),
        "gear": np.array(gears),
        "engine_rpm": np.array(eng_rpms),
        "F_drive": np.array(drive_forces),
        "t_final": elapsed_time,
        "x_final": elapsed_distance,
        "v_final": velocity,
        "final_drive": carInfo.fd1,
        "shift_delay": carInfo.shift_delay,
    }
    return results

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
    ax1.set_ylim(-0.5, 1.5)
    ax1.grid(True)
    
    # Engine RPM
    ax2.plot(t, rpm, label="Engine RPM", color="C3", lw=2)
    ax2.set_ylabel("RPM")
    ax2.set_ylim(3000, ENGINE_REDLINE_RPM * 1.1)
    ax2.grid(True)

    # Gear
    ax3.step(t, gear, where="post", label="Gear", color="C2", lw=2)
    ax3.set_ylabel("Gear")
    ax3.set_ylim(1, 6)
    ax3.set_xlabel("Time [s]")
    ax3.grid(True)

def plot_torque_curve(ax):
    """Plot the engine torque curve using engine_torque_from_rpm()."""
    # Base RPM points from the map (for markers)
    rpms_base = WHEEL_TORQUE_POINTS[:, 0]
    tq_Nm_base = WHEEL_TORQUE_POINTS[:, 1]

    # Smooth RPM range
    rpm_smooth = np.linspace(rpms_base[0], rpms_base[-1], 300)

    # Use the sim's interpolation function (returns N·m), then convert to lb·ft
    tq_nm_smooth = np.array([engine_tq_from_rpm(r) for r in rpm_smooth])
    tq_lbft_smooth = tq_nm_smooth * 1.35581795 / TOTAL_RATIO_ON_DYNO

    ax.set_xlim(4000, 14000)
    ax.set_ylim(0, 100)
    ax.plot(rpm_smooth, tq_lbft_smooth, label="Torque", color="C0")
    ax.scatter(rpms_base, tq_Nm_base * 1.35581795, color="C1", label="Input map points")
    ax.set_xlabel("Engine speed [rpm]")
    ax.set_ylabel("Wheel torque [lb·ft]")
    ax.set_title("Input Wheel Torque Map")
    ax.grid(True)
    ax.legend()

def plot_tire_curve(ax):
    """Plot the frictional force of the tires across the power"""
    kappa_range = [0, 4]

    # Smooth kappa range
    kappa_smooth = np.linspace(kappa_range[0], kappa_range[-1], 300)

    # Use the sim's grip function (N)
    grip_N_smooth = np.array([pacejka_traction_limited_force(100000, r) for r in kappa_smooth])

    ax.plot(kappa_smooth * 100, grip_N_smooth, color="C3", lw=3)
    ax.set_xlabel("Slip Ratio [%]")
    ax.set_xlim(0, 400)
    ax.set_ylabel("Friction force [N]")
    ax.set_ylim(0, 6000)
    ax.set_title("Friction Limited Force of Tires")
    ax.grid(True)

def possible_final_drives():
    # realisticly, 11-18 and 39-66. For full data, 10-70 is fine for both I guess
    front_min = 11
    front_max = 18
    rear_min = 39
    rear_max = 66

    rear_sprockets = np.linspace(rear_min, rear_max, rear_max - rear_min)
    front_sprockets = np.linspace(front_min, front_max, front_max - front_min)
    final_drive_ratios = []

    for rear_sprocket in rear_sprockets:
        for front_sprocket in front_sprockets:
            final_drive_ratio = float(rear_sprocket / front_sprocket)
            final_drive_ratios.append(final_drive_ratio)

    final_drive_ratios.sort()

    for i in range(len(final_drive_ratios)-1, -1, -1):
        if np.abs(final_drive_ratios[i] - final_drive_ratios[i-1]) < 0.005:
            del final_drive_ratios[i]

    return final_drive_ratios

def highlight_fds(ax, carInfo):
    # Highlight specific FD values at nominal SHIFT_DELAY
    for fd, color, marker, label in [
        (FINAL_DRIVE, "r", "o", "11:41"),
        (FINAL_DRIVE_NEW, "g", "o", "12:41"),
        (3.182, "b", "*", "11:35"),
        (2.917, "c", "*", "12:35"),
    ]:
        carInfo.fd1 = fd
        carInfo.shift_delay = SHIFT_DELAY
        res = simulate_run(carInfo)
        ax.plot(res["t_final"], fd, marker + color, label=label)

def simulate_FD_curve(carInfo):
    times = []
    ratios = possible_final_drives()

    for r in ratios:
        carInfo.fd1 = r
        res_fd = simulate_run(carInfo)
        times.append(res_fd["t_final"])

    FD_curve = {"ratio" : np.array(ratios), "time" : np.array(times)}

    return FD_curve

def plot_FD_curves(ax, carInfo, FD_curve):
    # Plot FD sweep into the provided Axes
    t = FD_curve["time"]
    r = FD_curve["ratio"]
    ax.plot(t, r, "k", label="FD sweep")

    highlight_fds(ax, carInfo)

    ax.set_ylabel("Final drive ratio")
    ax.set_ylim(FD_LOW_LIMIT, FD_HIGH_LIMIT)
    ax.set_xlabel(f"Time to {TARGET_DISTANCE:.0f} m [s]")
    ax.set_xlim(TIME_LOW_LIMIT, TIME_HIGH_LIMIT)
    ax.grid(True)
    ax.set_title(f"Optimized Final Drive Ratios\nshift delay: {carInfo.shift_delay*1000:.0f} ms")
    ax.legend()    

def simulate_SD_FD_curves(carInfo):
    shift_delays = np.linspace(0.1, 1, 2)
    shift_delays = np.append(shift_delays, carInfo.shift_delay)
    shift_delays = np.sort(shift_delays)
    sd1 = carInfo.shift_delay
    FD_curves = []

    for sd in shift_delays:
        carInfo.shift_delay = sd
        FD_curves.append(simulate_FD_curve(carInfo))

    carInfo.shift_delay = sd1
    results = {"sds" : shift_delays, "FD_curves" : np.array(FD_curves)}
    return results

def plot_SD_FD_curves(ax, carInfo, FD_SD_curves):
    # Plot multiple FD curves for different shift delays

    i = 0
    for sd in FD_SD_curves["sds"]:
        time = FD_SD_curves["FD_curves"][i]["time"]
        ratio = FD_SD_curves["FD_curves"][i]["ratio"]
        ax.plot(time, ratio, label=f"SD: {sd*1000:.0f} ms")
        i += 1

    highlight_fds(ax, carInfo)
    ax.set_ylabel("Final drive ratio")
    ax.set_ylim(FD_LOW_LIMIT, FD_HIGH_LIMIT)
    ax.set_xlabel(f"Time to {TARGET_DISTANCE:.0f} m [s]")
    ax.set_xlim(TIME_LOW_LIMIT, TIME_HIGH_LIMIT)
    ax.grid(True)
    ax.set_title("Shift delay effect on final drive")
    ax.legend()