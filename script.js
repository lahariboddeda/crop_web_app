console.log("✅ charts.js loaded");

let cropChartInstance = null;
let importanceChartInstance = null;

function createCropChart(crops, counts) {
  console.log("Creating crop chart with:", crops, counts);

  const canvas = document.getElementById('cropChart');
  if (!canvas) {
    console.error("❌ cropChart canvas not found");
    return;
  }

  if (cropChartInstance) {
    cropChartInstance.destroy();
  }

  const ctx = canvas.getContext('2d');

  cropChartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: crops || ['No Data'],
      datasets: [{
        label: 'Predictions',
        data: counts || [0],
        backgroundColor: '#2ecc71',
        borderColor: '#27ae60',
        borderWidth: 2
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });

  console.log("✅ Crop chart created");
}

function createImportanceChart() {
  console.log("Creating importance chart");

  const canvas = document.getElementById('importanceChart');
  if (!canvas) {
    console.error("❌ importanceChart canvas not found");
    return;
  }

  if (importanceChartInstance) {
    importanceChartInstance.destroy();
  }

  const ctx = canvas.getContext('2d');

  importanceChartInstance = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['N', 'P', 'K', 'Temperature', 'Humidity', 'pH', 'Rainfall'],
      datasets: [{
        data: [15, 12, 14, 18, 16, 10, 15],
        backgroundColor: ['#2ecc71', '#3498db', '#e74c3c', '#f39c12', '#9b59b6', '#1abc9c', '#e67e22'],
        borderColor: '#fff',
        borderWidth: 2
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false
    }
  });

  console.log("✅ Importance chart created");
}