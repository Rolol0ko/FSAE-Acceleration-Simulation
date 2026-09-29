# sim_gui.py
import os, sys

import tkinter as tk
from tkinter import ttk, messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Import from simulation core
from sim_core import (
    simulate_run,
    plot_FD_curves,
    plot_SD_FD_curves,
    plot_torque_curve,
    plot_tire_curve,
    plot_results,
    simulate_FD_curve,
    simulate_SD_FD_curves,
    SHIFT_DELAY,
    MASS_CAR,
    DRAG_C,
    FRONTAL_AREA,
    TARGET_DISTANCE,
    ROLLING_RESISTANCE_C,
    ENGINE_LAUNCH_RPM,
    carInfo
)

def setup_graph(ax):
    ax.set_facecolor('#424242')
    ax.set_ylabel('', color='#ffffff')
    ax.set_xlabel('', color='#ffffff')
    ax.tick_params(labelcolor='#ffffff', color='#ffffff', grid_color='#ffffff')
    ax.set_title('', color='#ffffff')

def make_input(ttk, self, parent_frameA, parent_frameB, label, variable):
    ttk.Label(parent_frameA, text=f"{label}").pack(anchor="w", pady=(0, 3.5), fill=tk.BOTH)
    self.var = tk.StringVar(value=f"{variable:.3f}")
    ttk.Entry(parent_frameB, textvariable=self.var, width=10).pack(anchor="w", pady=(0, 4))
    return self.var

class FSAESimApp:
    def __init__(self, master: tk.Tk):
        self.master = master
        master.title("FSAE Acceleration Simulator")

        filename = "black.tcl"
        if hasattr(sys, "_MEIPASS"):                        # running from PyInstaller bundle
            filename = os.path.join(sys._MEIPASS, filename) # type: ignore #_MEIPASS only exists when program is built with pyinstaller
        else:
            filename = os.path.abspath(filename)            # running from source
        
        master.tk.call('source', filename)
        ttk.Style(master).theme_use("black")
        
        # ----- Left: controls -----
        controls = ttk.Frame(master, padding=5)
        controls.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

        # Parameters
        ttk.Label(controls, text="Car Parameters", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 4))

        parameter_labels = ttk.Frame(controls)
        parameter_labels.pack(side=tk.LEFT, fill=tk.BOTH)
        
        parameter_inputs = ttk.Frame(controls)
        parameter_inputs.pack(side=tk.RIGHT, fill=tk.BOTH)

        #self.fd_var = make_input(ttk, self, parameter_labels, parameter_inputs, "Final drive ratio [-]", FINAL_DRIVE)
        ttk.Label(parameter_labels, text="Final drive ratio [-]").pack(anchor="w", pady=(0, 3.5))

        self.big_ratio = tk.StringVar(value=f"{41}")    # Rear sprocket teeth
        self.little_ratio = tk.StringVar(value=f"{11}") # Front sprocket teeth
        fd_inputs = ttk.Frame(parameter_inputs)
        fd_inputs.pack(side=tk.TOP, fill=tk.Y)
        ttk.Entry(fd_inputs, textvariable=self.big_ratio, width=10).pack(anchor="e", pady=(0, 4), side=tk.RIGHT, fill=tk.Y)
        ttk.Label(fd_inputs, text=":").pack(anchor="e", pady=(0, 3.5), side=tk.RIGHT, fill=tk.Y)
        ttk.Entry(fd_inputs, textvariable=self.little_ratio, width=10).pack(anchor="e", pady=(0, 4), side=tk.RIGHT, fill=tk.Y)
        
        self.sd_var = make_input(ttk, self, parameter_labels, parameter_inputs, "Shift delay [s]", SHIFT_DELAY)
        self.m_var = make_input(ttk, self, parameter_labels, parameter_inputs, "Car Mass [kg]", MASS_CAR)
        self.cd_var = make_input(ttk, self, parameter_labels, parameter_inputs, "Drag Coeffiecent [-]", DRAG_C)
        self.af_var = make_input(ttk, self, parameter_labels, parameter_inputs, "Frontal Area [m^2]", FRONTAL_AREA)
        self.cr_var = make_input(ttk, self, parameter_labels, parameter_inputs, "Rolling Resistance [-]", ROLLING_RESISTANCE_C)
        self.launch_rpm_var = make_input(ttk, self, parameter_labels, parameter_inputs, "Launch Engine Speed [rpm]", ENGINE_LAUNCH_RPM)

        plot_controls = ttk.Frame(controls)
        plot_controls.pack(side=tk.BOTTOM, fill=tk.Y)
        # Plot mode
        ttk.Label(plot_controls, text="Graph type", font=("Segoe UI", 10, "bold")).pack(anchor="center", pady=(8, 2))
        self.plot_mode = tk.StringVar(value="single")

        ttk.Radiobutton(
            plot_controls,
            text="Single run (75 m)",
            value="single",
            variable=self.plot_mode,
        ).pack(anchor="w")
        ttk.Radiobutton(
            plot_controls,
            text="FD sweep (fixed shift delay)",
            value="fd_sweep",
            variable=self.plot_mode,
        ).pack(anchor="w")
        ttk.Radiobutton(
            plot_controls,
            text="FD & shift delay sweep",
            value="fd_sd_sweep",
            variable=self.plot_mode,
        ).pack(anchor="w")
        ttk.Radiobutton(
            plot_controls,
            text="Tourque Curve",
            value="tourque_curve",
            variable=self.plot_mode,
        ).pack(anchor="w")
        ttk.Radiobutton(
            plot_controls,
            text="Grip Curve",
            value="grip_curve",
            variable=self.plot_mode,
        ).pack(anchor="w")

        # Action buttons
        ttk.Button(plot_controls, text="Plot", command=self.run_plot).pack(anchor="center", pady=(12, 4))
        ttk.Button(plot_controls, text="Quit", command=master.destroy).pack(anchor="center", pady=(0, 4))

        # Info label
        self.info_label = ttk.Label(
            plot_controls,
            text=f"Target distance: {TARGET_DISTANCE:.0f} m"
        )
        self.info_label.pack(anchor="center", pady=(10, 0))

        # ----- Right: plot area -----
        plot_frame = ttk.Frame(master, padding=0.5)
        plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.fig = Figure(facecolor="#424242", layout='tight', edgecolor='#ffffff')
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Do an initial plot
        self.run_plot()

    def show_loading_screen(self):
        # Display a loading popup while a graph is generated.
        self.loading = tk.Toplevel(self.master)

        ttk.Style(self.loading).theme_use("black")

        self.loading.title("Loading")
        self.loading.geometry("280x110")
        self.loading.resizable(False, False)
        
        # Keep the popup above the main application
        self.loading.transient(self.master)
        self.loading.grab_set()

        ttk.Label(
            self.loading,
            text="Generating graph...",
            font=("Segoe UI", 10, "bold")
        ).pack(pady=(20, 10))

        # Make the popup appear before plotting begins
        self.loading.update_idletasks()
        self.loading.update()

    def hide_loading_screen(self):
        """Close the loading popup."""
        if hasattr(self, "loading") and self.loading.winfo_exists():
            self.loading.grab_release()
            self.loading.destroy()

    def run_plot(self, initial: bool = False):
        """Read parameters, choose plot mode, and draw the appropriate graph."""

        car = carInfo()

        # Parse parameters
        try:
            car.fd1 = float(self.big_ratio.get()) / float(self.little_ratio.get())
            car.shift_delay = float(self.sd_var.get())
            car.mass = float(self.m_var.get())
            car.drag_c = float(self.cd_var.get())
            car.frontal_area = float(self.af_var.get())
            car.rolling_resistance_c = float(self.cr_var.get())
            car.launch_rpm = float(self.launch_rpm_var.get())
        except ValueError:
            messagebox.showerror("Input error", "Please enter numeric values for final drive and shift delay.")
            return None

        mode = self.plot_mode.get()
        self.show_loading_screen()

        try:
            # Clear figure and create a new Axes
            self.fig.clear()
            ax0 = self.fig.add_subplot(111)
            setup_graph(ax0)
            
            if mode == "single":
                # Run a single simulation and plot speed vs time
                self.fig.clear()
                ax0 = self.fig.add_subplot(411, sharex=ax0)
                setup_graph(ax0)
                ax1 = self.fig.add_subplot(412, sharex=ax0)
                setup_graph(ax1)
                ax2 = self.fig.add_subplot(413, sharex=ax0)
                setup_graph(ax2)
                ax3 = self.fig.add_subplot(414, sharex=ax0)
                setup_graph(ax3)

                res = simulate_run(car)

                plot_results([ax0, ax1, ax2, ax3], res)

                # Simple text summary in the corner
                summary = (
                    "Final Time = {:.3f} s\nFinal Velocity = {:.1f} km/h"
                    .format(res["t_final"], res["v_final"] * 3.6)
                )

                ax0.text(
                    0.02, 0.98, summary,
                    transform=ax0.transAxes,
                    va="top",
                    ha="left",
                    fontsize=9,
                    bbox=dict(boxstyle="round", facecolor="white", alpha=0.6),
                )
            elif mode == "fd_sweep":
                # Plot FD curves on this Axes for a fixed shift delay
                curve = simulate_FD_curve(car)
                plot_FD_curves(ax0, car, curve)
                ax0.set_title(
                    "Final drive sweep (shift delay = {:.0f} ms)".format(car.shift_delay * 1000.0)
                )
            elif mode == "fd_sd_sweep":
                # Plot FD & shift delay sweep on this Axes
                SD_FD_curves = simulate_SD_FD_curves(car)
                plot_SD_FD_curves(ax0, car, SD_FD_curves)
                ax0.set_title("Final drive & shift delay sweep")
            elif mode == "tourque_curve":
                # plot wheel tourque
                plot_torque_curve(ax0)
            elif mode == "grip_curve":
                plot_tire_curve(ax0)
            else:
                ax0.text(0.5, 0.5, "Unknown mode", transform=ax0.transAxes, ha="center", va="center")
            
            self.fig.tight_layout()
            self.canvas.draw()
            
        except Exception as e:
            if not initial:
                messagebox.showerror(
                    "Error",
                    f"Error while plotting:\n{e}"
                )
        finally:
            self.hide_loading_screen()

if __name__ == "__main__":
    root = tk.Tk()
    app = FSAESimApp(root)
    root.mainloop()
