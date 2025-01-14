import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Parametry systemu
N = 10
masses = np.linspace(1.0, 2.0, N)
k = 10.0
k_s = 5.0

# Macierz mas (diagonalna z indywidualnymi masami)
M = np.diag(masses)

# Macierz sztywności (trójdiagonalna)
K = np.diag([k + k_s] * N) + np.diag([-k_s] * (N-1), k=1) + np.diag([-k_s] * (N-1), k=-1)

# Funkcja obliczająca pochodne dla solve_ivp
def equations(t, y):
    x = y[:N]
    v = y[N:]

    dxdt = v
    dvdt = -np.linalg.inv(M) @ (K @ x)
    return np.concatenate((dxdt, dvdt))

# Warunki początkowe
x0 = np.zeros(N)
x0[0] = 1.0
v0 = np.zeros(N)
y0 = np.concatenate((x0, v0))

# Rozwiązanie układu równań
t_span = (0, 20)
t_eval = np.linspace(*t_span, 500)
solution = solve_ivp(equations, t_span, y0, t_eval=t_eval, method='RK45')

# Przygotowanie animacji
fig, ax = plt.subplots()
ax.set_xlim(-1, N)
ax.set_ylim(-2, 2)
points, = ax.plot([], [], 'o', lw=2, label="Ciężarki")
springs, = ax.plot([], [], '-', lw=1, color='gray', label="Sprężyny")

def animate(frame):
    positions = solution.y[:N, frame]
    x_coords = np.arange(N)
    points.set_data(x_coords, positions)

    spring_x = []
    spring_y = []
    for i in range(N - 1):
        spring_x.extend([x_coords[i], x_coords[i + 1], None])
        spring_y.extend([positions[i], positions[i + 1], None])
    springs.set_data(spring_x, spring_y)
    return points, springs

ani = FuncAnimation(fig, animate, frames=len(t_eval), interval=30, blit=True)
plt.legend()
plt.show()