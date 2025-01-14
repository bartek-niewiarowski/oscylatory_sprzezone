import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button

# Funkcja aktualizująca macierze mas i sztywności
def update_matrices(N, masses, k, k_s):
    M = np.diag(masses)
    K = (np.diag([k + k_s] * N) +
         np.diag([-k_s] * (N - 1), k=1) +
         np.diag([-k_s] * (N - 1), k=-1))
    return M, K

# Funkcja obliczająca pochodne dla solve_ivp
def equations(t, y, M, K, N):
    x = y[:N]
    v = y[N:]
    dxdt = v
    dvdt = -np.linalg.inv(M) @ (K @ x)
    return np.concatenate((dxdt, dvdt))

# Funkcja do rozwiązywania układu równań
def solve_system(N, k, k_s, x0_val, t_span, t_eval):
    masses = np.linspace(1.0, 2.0, N)
    x0 = np.zeros(N)
    v0 = np.zeros(N)
    x0[0] = x0_val
    M, K = update_matrices(N, masses, k, k_s)
    y0 = np.concatenate((x0, v0))
    sol = solve_ivp(equations, t_span, y0, t_eval=t_eval, args=(M, K, N), method='RK45')
    return sol

# Parametry początkowe i warunki początkowe
N = 10
k = 10.0
k_s = 5.0
x0_val = 1.0
t_max = 20
t_span = (0, t_max)
t_eval = np.linspace(*t_span, 500)
solution = solve_system(N, k, k_s, x0_val, t_span, t_eval)

# Przygotowanie wykresu
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.4)
ax.set_xlim(-1, 20)
ax.set_ylim(-2, 2)
points, = ax.plot([], [], 'o', lw=2, label="Ciężarki")
springs, = ax.plot([], [], '-', lw=1, color='gray', label="Sprężyny")

# Funkcja animacji
def animate(frame):
    positions = solution.y[:N, frame]
    x_coords = np.arange(N)
    points.set_data(x_coords, positions)
    spring_x, spring_y = [], []
    for i in range(N - 1):
        spring_x.extend([x_coords[i], x_coords[i + 1], None])
        spring_y.extend([positions[i], positions[i + 1], None])
    springs.set_data(spring_x, spring_y)
    return points, springs

ani = FuncAnimation(fig, animate, frames=len(t_eval), interval=30, blit=True)

# Dodanie suwaków dla `k`, `k_s`, `N` i czasu `t_max`
ax_k = plt.axes([0.25, 0.3, 0.65, 0.03])
ax_k_s = plt.axes([0.25, 0.25, 0.65, 0.03])
ax_N = plt.axes([0.25, 0.2, 0.65, 0.03])
ax_t_max = plt.axes([0.25, 0.15, 0.65, 0.03])
slider_k = Slider(ax_k, 'k', 1.0, 20.0, valinit=k)
slider_k_s = Slider(ax_k_s, 'k_s', 1.0, 20.0, valinit=k_s)
slider_N = Slider(ax_N, 'N', 2, 20, valinit=N, valstep=1)
slider_t_max = Slider(ax_t_max, 'Czas (t_max)', 5.0, 50.0, valinit=t_max)

# Funkcja aktualizująca po zmianie suwaków
def update(val):
    global solution, N, t_span, t_eval
    k_new = slider_k.val
    k_s_new = slider_k_s.val
    N_new = int(slider_N.val)
    t_max_new = slider_t_max.val
    t_span = (0, t_max_new)
    t_eval = np.linspace(*t_span, 500)
    if N_new != N:
        ax.set_xlim(-1, N_new)
    N = N_new
    solution = solve_system(N, k_new, k_s_new, x0_val, t_span, t_eval)

slider_k.on_changed(update)
slider_k_s.on_changed(update)
slider_N.on_changed(update)
slider_t_max.on_changed(update)

# Dodanie przycisku resetowania
ax_reset = plt.axes([0.8, 0.025, 0.1, 0.04])
button_reset = Button(ax_reset, 'Reset')

def reset(event):
    slider_k.reset()
    slider_k_s.reset()
    slider_N.reset()
    slider_t_max.reset()

button_reset.on_clicked(reset)

plt.legend()
plt.show()