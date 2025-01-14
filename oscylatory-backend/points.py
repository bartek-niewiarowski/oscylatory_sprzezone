import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Parametry układu
num_oscillators = 5
natural_frequencies = np.random.uniform(0.8, 1.2, num_oscillators)
coupling_strength = 0.5
time_step = 0.1
num_steps = 200

# Inicjalizacja faz oscylatorów
phases = np.random.uniform(0, 2 * np.pi, num_oscillators)
phase_history = []

# Funkcja aktualizacji faz (model Kuramoto)
def update_phases(phases, dt, coupling_strength, natural_frequencies):
    new_phases = np.zeros_like(phases)
    for i in range(len(phases)):
        interaction_sum = np.sum(np.sin(phases - phases[i]))
        new_phases[i] = phases[i] + dt * (natural_frequencies[i] + (coupling_strength / num_oscillators) * interaction_sum)
    return new_phases % (2 * np.pi)

# Symulacja
for _ in range(num_steps):
    phase_history.append(phases.copy())
    phases = update_phases(phases, time_step, coupling_strength, natural_frequencies)

phase_history = np.array(phase_history)

# Wizualizacja
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(-1.2, 1.2)
ax.set_ylim(-1.2, 1.2)
ax.set_aspect('equal')
lines = [plt.plot([], [], marker='o', markersize=10, linestyle='', label=f'Osc {i+1}')[0] for i in range(num_oscillators)]

# Aktualizacja animacji
def update(frame):
    ax.clear()
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_aspect('equal')
    for i, line in enumerate(lines):
        x = [np.cos(phase_history[frame, i])]
        y = [np.sin(phase_history[frame, i])]
        line.set_data(x, y)
        ax.add_artist(line)
    ax.legend(loc='upper right')
    return lines

# Tworzenie animacji
ani = FuncAnimation(fig, update, frames=num_steps, interval=50, blit=False)

plt.show()
