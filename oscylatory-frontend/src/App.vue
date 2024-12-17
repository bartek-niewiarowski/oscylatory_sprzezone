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
        t_max: 20.0,
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

// Funkcja rysująca wykres wyników
const plotResults = () => {
  const canvas = document.getElementById('plot')
  const ctx = canvas.getContext('2d')
  ctx.clearRect(0, 0, canvas.width, canvas.height)

  results.value.slice(0, 10).forEach((positions, index) => {
    ctx.beginPath()
    ctx.moveTo(0, 250)
    for (let i = 0; i < times.value.length; i++) {
      ctx.lineTo(i * 2, 250 - positions[i] * 50)
    }
    ctx.strokeStyle = `hsl(${index * 36}, 100%, 50%)`
    ctx.stroke()
  })
}
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