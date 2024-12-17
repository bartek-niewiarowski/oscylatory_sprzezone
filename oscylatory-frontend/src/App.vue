<script setup>
import { ref } from 'vue'

// Dane do wyświetlania wyników
const times = ref([])
const results = ref([])

// Parametry układu z wartościami domyślnymi
const params = ref({
  N: 10,
  k: 10.0,
  k_s: 5.0,
  x0_val: 1.0,
  t_max: 20.0,
})

// Funkcja pobierająca wyniki z API FastAPI
const fetchResults = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/solve_system', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        N: params.value.N,
        k: params.value.k,
        k_s: params.value.k_s,
        x0_val: params.value.x0_val,
        t_max: params.value.t_max,
      }),
    })

    const data = await response.json()
    times.value = data.time
    results.value = data.results
    plotResults()
  } catch (error) {
    console.error('Error fetching results:', error)
  }
}

const plotResults = () => {
  const canvas = document.getElementById('plot');
  const ctx = canvas.getContext('2d');

  const totalWeights = results.value.length / 2; // Liczba ciężarków (połowa wyników)
  const positions = results.value.slice(0, totalWeights); // Pobierz tylko pozycje ciężarków
  const timeSteps = times.value.length; // Ilość kroków czasowych

  let currentFrame = 0; // Licznik klatek

  const marginX = 50; // Margines na osi X
  const canvasWidth = canvas.width - 2 * marginX; // Efektywna szerokość kanwy
  const canvasHeight = canvas.height;

  const animate = () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height); // Wyczyść canvas

    // Rysowanie sprężyn jako linii między ciężarkami
    ctx.strokeStyle = "gray";
    for (let i = 0; i < totalWeights - 1; i++) {
      ctx.beginPath();
      ctx.moveTo(
        marginX + i * (canvasWidth / (totalWeights - 1)),
        canvasHeight / 2 - positions[i][currentFrame] * 50
      );
      ctx.lineTo(
        marginX + (i + 1) * (canvasWidth / (totalWeights - 1)),
        canvasHeight / 2 - positions[i + 1][currentFrame] * 50
      );
      ctx.stroke();
    }

    // Rysowanie ciężarków jako okręgów
    for (let i = 0; i < totalWeights; i++) {
      ctx.beginPath();
      const x = marginX + i * (canvasWidth / (totalWeights - 1));
      const y = canvasHeight / 2 - positions[i][currentFrame] * 50;
      ctx.arc(x, y, 10, 0, 2 * Math.PI); // Rysowanie kółek
      ctx.fillStyle = `hsl(${i * (360 / totalWeights)}, 100%, 50%)`;
      ctx.fill();
    }

    // Przejdź do następnej klatki
    currentFrame = (currentFrame + 1) % timeSteps; // Zapętl klatki
    requestAnimationFrame(animate); // Wywołanie rekurencyjne dla animacji
  };

  animate(); // Uruchom animację
};
</script>

<template>
  <div class="container">
    <!-- Główna sekcja z animacją i kontrolkami -->
    <div class="content">
      <!-- Sekcja z animacją -->
      <div class="canvas-container">
        <h1 class="title">Spring System Visualization</h1>
        <canvas id="plot" width="800" height="500" style="border: 1px solid #ccc;"></canvas>
      </div>

      <!-- Sekcja z kontrolkami -->
      <div class="controls">
        <h2>Parameters</h2>
        <div class="grid-container">
          <!-- Kolumna 1: 3 suwaki -->
          <div class="column">
            <label>Liczba ciężarków (N): {{ params.N }}</label>
            <input type="range" v-model="params.N" min="2" max="20" step="1" />

            <label>Stała sprężystości głównej (k): {{ params.k }}</label>
            <input type="range" v-model="params.k" min="1.0" max="20.0" step="0.1" />

            <label>Stała sprężystości sąsiadów (k_s): {{ params.k_s }}</label>
            <input type="range" v-model="params.k_s" min="1.0" max="20.0" step="0.1" />
          </div>

          <!-- Kolumna 2: 2 suwaki + przycisk -->
          <div class="column">
            <label>Początkowe odchylenie pierwszego ciężarka (x0_val): {{ params.x0_val }}</label>
            <input type="range" v-model="params.x0_val" min="0.1" max="5.0" step="0.1" />

            <label>Czas symulacji (t_max): {{ params.t_max }}</label>
            <input type="range" v-model="params.t_max" min="5.0" max="120.0" step="5.0" />

            <button @click="fetchResults">Run Experiment</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.container {
  width: 90%; /* 90% szerokości z marginesami */
  margin: 0 auto; /* Wyśrodkowanie */
  height: 100vh; /* Pełna wysokość okna przeglądarki */
  display: flex;
  justify-content: center;
  align-items: center;
}

.content {
  display: flex;
  gap: 20px; /* Odstęp między sekcjami */
  width: 100%; /* Zajmuje całą dostępną szerokość kontenera */
}

.canvas-container {
  flex: 3; /* Większa część dla animacji */
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: rgb(54, 54, 54); /* Tło dla głównego kontenera Vue */
  border-bottom: #d6bb4c;
}

.controls {
  flex: 1; /* Mniejsza część dla kontrolek */
  background-color: #f4f4f4;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.title {
  color: white;
}

.grid-container {
  display: grid;
  grid-template-columns: 1fr 1fr; /* Dwie kolumny o równej szerokości */
  gap: 20px;
}

.column {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

h1, h2 {
  margin-bottom: 20px;
}

label {
  font-weight: bold;
}

input {
  width: 100%;
}

button {
  padding: 10px 20px;
  font-size: 16px;
  margin-top: 10px;
  cursor: pointer;
  background-color: #d6bb4c;
}
</style>