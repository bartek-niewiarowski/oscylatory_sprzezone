import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Parametry symulacji
num_pendulums = 7  # Liczba wahadeł
lengths = np.linspace(0.8, 1.2, num_pendulums)  # Długości wahadeł (różne, wpływa na częstotliwość)
natural_frequencies = np.sqrt(9.81 / lengths)  # Częstotliwości własne wahadeł (z prawa fizyki)
coupling_strength = 0.05  # Siła sprzężenia między wahadłami
time_step = 0.05  # Krok czasowy
num_steps = 400  # Liczba kroków czasowych

# Inicjalizacja kątów i prędkości kątowych wahadeł
angles = np.random.uniform(-0.5, 0.5, num_pendulums)  # Początkowe kąty
angular_velocities = np.zeros(num_pendulums)  # Początkowe prędkości kątowe
angle_history = []

# Funkcja aktualizacji stanu wahadeł
def update_pendulums(angles, angular_velocities, dt, coupling_strength, natural_frequencies):
    new_angular_velocities = angular_velocities.copy()
    for i in range(len(angles)):
        # Równanie ruchu z uwzględnieniem sprzężenia
        coupling = np.sum(np.sin(angles - angles[i]))
        new_angular_velocities[i] += (
            -natural_frequencies[i]**2 * np.sin(angles[i]) + coupling_strength * coupling
        ) * dt
    new_angles = angles + new_angular_velocities * dt
    return new_angles, new_angular_velocities

# Symulacja
for _ in range(num_steps):
    angle_history.append(angles.copy())
    angles, angular_velocities = update_pendulums(
        angles, angular_velocities, time_step, coupling_strength, natural_frequencies
    )

angle_history = np.array(angle_history)

# Wizualizacja
fig, ax = plt.subplots(figsize=(8, 6))
ax.set_xlim(-1.5 * num_pendulums, 1.5 * num_pendulums)
ax.set_ylim(-1.5, 1.5)
lines = []
for i in range(num_pendulums):
    # Dodajemy etykiety dla każdego wahadła
    line, = ax.plot([], [], 'o-', lw=2, label=f'Wahadło {i + 1}')
    lines.append(line)

# Aktualizacja animacji
def update(frame):
    ax.clear()
    ax.set_xlim(-1.5 * num_pendulums, 1.5 * num_pendulums)
    ax.set_ylim(-1.5, 1.5)
    for i, line in enumerate(lines):
        x = [i - num_pendulums // 2, i - num_pendulums // 2 + np.sin(angle_history[frame, i])]
        y = [0, -np.cos(angle_history[frame, i])]
        line.set_data(x, y)
        ax.plot(x, y, 'o-', lw=2, label=f'Wahadło {i + 1}')  # Dodajemy linie i etykiety
    ax.axhline(0, color='k', linestyle='--')  # Belka
    ax.legend(loc='upper right')  # Legenda
    return lines

# Tworzenie animacji
ani = FuncAnimation(fig, update, frames=num_steps, interval=30, blit=False)

plt.show()

