from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
from scipy.integrate import solve_ivp

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Dopuszczaj dowolne źródła
    allow_credentials=True,
    allow_methods=["*"],  # Zezwalaj na wszystkie metody
    allow_headers=["*"],  # Zezwalaj na wszystkie nagłówki
)

# Funkcja aktualizująca macierze mas i sztywności
def update_matrices(N, masses, k, k_s):
    M = np.diag(masses)  # Macierz mas
    K = (np.diag([k + k_s] * N) +
         np.diag([-k_s] * (N - 1), k=1) +
         np.diag([-k_s] * (N - 1), k=-1))  # Macierz sztywności
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
    masses = np.linspace(1.0, 2.0, N)  # Generujemy masy od 1.0 do 2.0
    x0 = np.zeros(N)  # Pozycje początkowe
    v0 = np.zeros(N)  # Prędkości początkowe
    x0[0] = x0_val  # Odchylenie pierwszego ciężarka
    M, K = update_matrices(N, masses, k, k_s)
    y0 = np.concatenate((x0, v0))
    sol = solve_ivp(equations, t_span, y0, t_eval=t_eval, args=(M, K, N), method='RK45')
    return sol.t.tolist(), sol.y.tolist()

# Model Pydantic do walidacji danych wejściowych
class SystemParams(BaseModel):
    N: int = Query(..., description="Liczba ciezarkow (2-20)", ge=2, le=20)
    k: float = Query(..., description="Stala sprezystosci glowna (1-20)", ge=1.0, le=20.0)
    k_s: float = Query(..., description="Stala sprezystosci sasiadow (1-20)", ge=1.0, le=20.0)
    x0_val: float = Query(1.0, description="Poczatkowe odchylenie pierwszego ciezarka")
    t_max: float = Query(20.0, description="Czas symulacji", ge=5.0, le=50.0)

@app.post("/solve_system")
def solve_spring_system(params: SystemParams):
    """
    Rozwiazuje uklad sprężynowy z podanymi parametrami.
    """
    t_span = (0, params.t_max)
    t_eval = np.linspace(0, params.t_max, 500)
    times, results = solve_system(params.N, params.k, params.k_s, params.x0_val, t_span, t_eval)
    return {
        "time": times,
        "results": results
    }