1. Purpose

Reusable launch vehicles and planetary landers require precise vertical control under gravity, uncertainty, and actuator limits. This project implements a one-dimensional rocket hover simulation to study how classical feedback control stabilizes vertical motion and how real-world non-idealities affect performance. The focus is on correctness, robustness, and interpretability rather than visual realism.

2. System Scope and Assumptions

The vehicle is modeled as a point mass moving in one vertical axis. Mass and gravity are constant, and aerodynamic forces and fuel consumption are intentionally omitted. These assumptions isolate the guidance and control problem while preserving the dominant dynamics relevant to powered ascent and hover.

3. Governing Dynamics

The system follows Newton’s second law. Vertical motion is determined by the balance between engine thrust and gravitational force:

m ÿ = T - m g


Where y is altitude, ẏ is vertical velocity, and ÿ is vertical acceleration. This equation is evaluated at each timestep and defines the physical constraints under which the controller operates.

4. Control Objective

The goal is to drive the vehicle from rest to a commanded altitude (y_target) and maintain that altitude with minimal overshoot and rapid settling. The controller must remain stable in the presence of sensor noise and bounded actuator authority while respecting physical constraints such as ground contact.

5. Control Architecture

A proportional–derivative (PD) controller with gravity compensation is used:

T = m g + Kp * (y_target - y) - Kd * ẏ


The proportional term (Kp) corrects altitude error.

The derivative term (Kd) damps vertical motion.

Gravity compensation ensures thrust commands represent control effort rather than static load balancing.

6. Closed-Loop Dynamics

Substituting the control law into the system dynamics gives a second-order linear closed-loop system:

m ÿ + Kd ẏ + Kp y = Kp * y_target


This structure allows analytical reasoning about damping, transient response, and stability, analogous to a mass–spring–damper system.

7. Gain Selection Strategy

The damping ratio of the closed-loop system is:

ζ = Kd / (2 * sqrt(m * Kp))


Setting ζ = 1 achieves critical damping and the fastest non-oscillatory response.
For m = 100 and Kp = 50, the optimal derivative gain is:

Kd ≈ 141


Gains are chosen analytically rather than empirically.

8. Non-Idealities and Constraints

To reflect operational conditions:

Velocity measurements are corrupted with Gaussian noise.

Thrust commands are limited to T_max using:

T = max(0, min(T, T_max))


Ground contact is enforced:

if y <= 0:
    v = 0
    y = 0


These constraints expose realistic failure modes and demonstrate interactions between control law and hardware limits.

9. Observed Behavior

With critically damped gains, the vehicle ascends smoothly to the target altitude and settles without sustained oscillation. Noise introduces small steady-state fluctuations, while thrust saturation demonstrates the effect of limited actuator authority. The system remains stable throughout extended simulation.
10. Findings. After a bit of experimenting with diffrent Kd and Kp. Here are my findings of what happens when you increase Kd and Kp. 
1. Effects of Increasing/Decreasing Kp (Proportional Gain)
	
Increase in Kp	↑ More overshoot	↓ Settling faster	↑ More jitter
Decrease in Kp 	↓ Less overshoot	↑ Settling slower	↓ Less jitter

Explanation:

Higher Kp reacts more aggressively to position errors → faster response → can overshoot → more thrust oscillation.

Lower Kp is sluggish → slower settling → smoother thrust.

2. Effects of Increasing/Decreasing Kd (Derivative Gain)
Increase in Kd:	↓ Less overshoot	↓ Settling faster	↓ Thrust jitter
Decrease in Kd 	↑ More overshoot	↑ Settling slower	↑ Thrust jitter

Explanation:

Kd adds damping → resists velocity → reduces overshoot and stabilizes thrust.

Too high Kd → slows system too much (overdamped), can make response sluggish.

Too low Kd → underdamped → large oscillations and thrust spikes.
Kp acts like the rocket’s thrusters firing to quickly correct altitude errors, while Kd acts like fine-tuned stabilizers that resist excessive speed, damping oscillations and keeping the flight smooth.
11. Extensions

This framework can be extended to:

Include aerodynamic drag and time-varying mass

Model planar or three-dimensional motion

Implement advanced control strategies such as LQR or MPC

Integrate state estimation with Kalman filtering for improved robustness
