<script setup>
import { ref } from 'vue'

// Dane do wyświetlania wyników
const times = ref([])
const results = ref([])

// Funkcja pobierająca wyniki z API FastAPI
const fetchResults = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/solve_system', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        N: 10,
        k: 10.0,
        k_s: 5.0,
        x0_val: 1.0,
        t_max: 120.0,
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
  const positions = results.value.slice(0, 10); // Pobierz tylko pozycje pierwszych 10 ciężarków
  const timeSteps = times.value.length; // Ilość kroków czasowych
  let currentFrame = 0; // Licznik klatek

  const animate = () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height); // Wyczyść canvas
    const canvasWidth = canvas.width;
    const canvasHeight = canvas.height;

    // Rysowanie sprężyn jako linii między ciężarkami
    ctx.strokeStyle = "gray";
    for (let i = 0; i < positions.length - 1; i++) {
      ctx.beginPath();
      ctx.moveTo(i * (canvasWidth / positions.length), canvasHeight / 2 - positions[i][currentFrame] * 50);
      ctx.lineTo((i + 1) * (canvasWidth / positions.length), canvasHeight / 2 - positions[i + 1][currentFrame] * 50);
      ctx.stroke();
    }

    // Rysowanie ciężarków jako okręgów
    for (let i = 0; i < positions.length; i++) {
      ctx.beginPath();
      const x = i * (canvasWidth / positions.length);
      const y = canvasHeight / 2 - positions[i][currentFrame] * 50;
      ctx.arc(x, y, 10, 0, 2 * Math.PI); // Rysowanie kółek
      ctx.fillStyle = `hsl(${i * 36}, 100%, 50%)`;
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
    <h1>Spring System Visualization</h1>
    <button @click="fetchResults">Run Experiment</button>
    <canvas id="plot" width="800" height="500" style="border: 1px solid #ccc;"></canvas>
  </div>
</template>

<style scoped>
.container {
  text-align: center;
  margin-top: 20px;
}
button {
  padding: 10px 20px;
  font-size: 16px;
  margin-bottom: 10px;
  cursor: pointer;
}
canvas {
  margin-top: 20px;
}
</style>