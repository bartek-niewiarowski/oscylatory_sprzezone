import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button

# Początkowe parametry układu
N = 10  # Liczba ciężarków
masses = np.linspace(1.0, 2.0, N)  # Indywidualne masy
k = 10.0  # Sztywność sprężyny do podłoża
k_s = 5.0  # Sztywność sprężyn między ciężarkami

# Funkcja aktualizująca macierze mas i sztywności
def update_matrices(N, masses, k, k_s):
    M = np.diag(masses)  # Macierz mas
    K = (np.diag([k + k_s] * N) +
         np.diag([-k_s] * (N - 1), k=1) +
         np.diag([-k_s] * (N - 1), k=-1))  # Macierz sztywności
    return M, K

# Funkcja obliczająca pochodne dla solve_ivp
def equations(t, y, M, K):
    x = y[:N]
    v = y[N:]
    dxdt = v
    dvdt = -np.linalg.inv(M) @ (K @ x)
    return np.concatenate((dxdt, dvdt))

# Funkcja do rozwiązywania układu równań
def solve_system(N, masses, k, k_s, x0, v0, t_span, t_eval):
    M, K = update_matrices(N, masses, k, k_s)
    y0 = np.concatenate((x0, v0))
    sol = solve_ivp(equations, t_span, y0, t_eval=t_eval, args=(M, K), method='RK45')
    return sol

# Parametry początkowe i warunki początkowe
x0 = np.zeros(N)
x0[0] = 1.0
v0 = np.zeros(N)
t_span = (0, 20)
t_eval = np.linspace(*t_span, 500)
solution = solve_system(N, masses, k, k_s, x0, v0, t_span, t_eval)

# Przygotowanie wykresu
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.25)
ax.set_xlim(-1, N)
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

# Dodanie suwaków
ax_k = plt.axes([0.25, 0.1, 0.65, 0.03])
ax_k_s = plt.axes([0.25, 0.15, 0.65, 0.03])
slider_k = Slider(ax_k, 'k', 1.0, 20.0, valinit=k)
slider_k_s = Slider(ax_k_s, 'k_s', 1.0, 20.0, valinit=k_s)

# Funkcja aktualizująca po zmianie suwaka
def update(val):
    global solution
    k_new = slider_k.val
    k_s_new = slider_k_s.val
    solution = solve_system(N, masses, k_new, k_s_new, x0, v0, t_span, t_eval)

slider_k.on_changed(update)
slider_k_s.on_changed(update)

# Dodanie przycisku resetowania
ax_reset = plt.axes([0.8, 0.025, 0.1, 0.04])
button_reset = Button(ax_reset, 'Reset')

def reset(event):
    slider_k.reset()
    slider_k_s.reset()

button_reset.on_clicked(reset)

plt.legend()
plt.show()