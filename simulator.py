import random
import matplotlib.pyplot as plt
Kp=50
Kd=141
mass=100
max_time=200
T_max=2000
y=0
t=0
v=0
dt=0.01
g=9.82
y_target=100
t_list=[]
y_list=[]
v_list=[]
Thrust_list=[]
while t<max_time:
    error=random.gauss(0,0.5)
    v_fuzzy=v+error



    T= mass*g+Kp*(y_target-y)-Kd*v_fuzzy
    T = max(0,min(T, T_max))
    a=(T-mass*g)/mass
    v=v+a*dt
    y=y+v*dt
    if y<=0:
        v=0
        y=0
    t=t+dt

    t_list.append(t)
    Thrust_list.append(T)
    y_list.append(y)
    v_list.append(v)


plt.plot(t_list,y_list)
plt.xlabel("time")
plt.ylabel("flight path")

plt.figure(figsize=(10, 8)) 


plt.subplot(3, 1, 1)
plt.plot(t_list, y_list, label='True Altitude')
plt.axhline(y=y_target, color='r', linestyle='--', label='Target (100m)')
plt.ylabel("Altitude (m)")
plt.title("Rocket Flight Simulation")
plt.legend()
plt.grid(True)
# Subplot 2: Velocity
plt.subplot(3, 1, 2)
plt.plot(t_list, v_list, color='orange', label='True Velocity')
plt.ylabel("Velocity (m/s)")
plt.grid(True)
# Subplot 3: Thrust
plt.subplot(3, 1, 3)
plt.plot(t_list, Thrust_list, color='green', label='Thrust')
plt.xlabel("Time (s)")
plt.ylabel("Thrust (N)")
plt.grid(True)

plt.tight_layout() 
plt.show()




