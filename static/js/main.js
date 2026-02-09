document.addEventListener('DOMContentLoaded', function () {
  // Initialize Charts
  initializeCharts();
  
  // Animate stat numbers (data-target)
  const counters = document.querySelectorAll('.stat-number');
  if (counters.length) {
    counters.forEach(counter => {
      const target = +counter.getAttribute('data-target') || 0;
      let current = 0;
      const step = Math.max(1, Math.floor(target / 80));
      const updater = () => {
        current += step;
        if (current >= target) {
          counter.textContent = target.toString();
        } else {
          counter.textContent = current.toString();
          requestAnimationFrame(updater);
        }
      };
      // Simple visibility check before animating
      const io = new IntersectionObserver(entries => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            updater();
            io.disconnect();
          }
        });
      }, { threshold: 0.4 });
      io.observe(counter);
    });
  }

  // Small enhancement: smooth scroll for anchor links (fallback)
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', (e) => {
      const target = document.querySelector(a.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });

  // Show registration modal (if present) after a short delay
  try {
    const modalEl = document.getElementById('registrationModal');
    if (modalEl) {
      const modal = new bootstrap.Modal(modalEl);
      // Always show after a short delay (force on every visit)
      setTimeout(() => {
        try {
          modal.show();
          const first = modalEl.querySelector('input[name="name"]');
          if (first) first.focus();
        } catch (e) { console.warn('could not show modal', e); }
      }, 700);
      // Keep submit/close handlers but do NOT persist 'seen' to localStorage so modal appears every time
      const form = modalEl.querySelector('form');
      if (form) form.addEventListener('submit', () => {/* no-op: allow submit but don't persist shown state */});
    }
  } catch (e) {
    // fail silently if bootstrap isn't available yet
    console.warn('modal init failed', e);
  }
});

// Chart initialization function
function initializeCharts() {
  // Chart.js global defaults
  Chart.defaults.font.family = "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif";
  Chart.defaults.color = '#6b7280';
  Chart.defaults.borderColor = 'rgba(200, 161, 101, 0.2)';
  
  // Monthly Sales Trend Chart
  const salesCtx = document.getElementById('salesChart');
  if (salesCtx) {
    new Chart(salesCtx, {
      type: 'line',
      data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        datasets: [{
          label: 'Sales (Tons)',
          data: [65, 78, 90, 81, 96, 105, 114, 129, 135, 142, 155, 168],
          borderColor: '#c8a165',
          backgroundColor: 'rgba(200, 161, 101, 0.1)',
          borderWidth: 3,
          fill: true,
          tension: 0.4,
          pointBackgroundColor: '#c8a165',
          pointBorderColor: '#fff',
          pointBorderWidth: 2,
          pointRadius: 5,
          pointHoverRadius: 7
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            backgroundColor: 'rgba(45, 24, 16, 0.9)',
            titleColor: '#fff',
            bodyColor: '#fff',
            padding: 12,
            displayColors: false,
            callbacks: {
              label: function(context) {
                return context.parsed.y + ' tons';
              }
            }
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            grid: {
              color: 'rgba(200, 161, 101, 0.1)'
            },
            ticks: {
              callback: function(value) {
                return value + ' tons';
              }
            }
          },
          x: {
            grid: {
              display: false
            }
          }
        }
      }
    });
  }

  // Top Spice Categories Chart
  const categoryCtx = document.getElementById('categoryChart');
  if (categoryCtx) {
    new Chart(categoryCtx, {
      type: 'doughnut',
      data: {
        labels: ['Cardamom', 'Cinnamon', 'Cloves', 'Black Pepper', 'Coriander', 'Others'],
        datasets: [{
          data: [28, 22, 18, 15, 12, 5],
          backgroundColor: [
            '#c8a165',
            '#a67c52',
            '#8b6239',
            '#6b4c2f',
            '#4a5d3f',
            '#2d1810'
          ],
          borderWidth: 2,
          borderColor: '#fff'
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              padding: 15,
              usePointStyle: true,
              font: {
                size: 11
              }
            }
          },
          tooltip: {
            backgroundColor: 'rgba(45, 24, 16, 0.9)',
            titleColor: '#fff',
            bodyColor: '#fff',
            padding: 12,
            displayColors: false,
            callbacks: {
              label: function(context) {
                return context.label + ': ' + context.parsed + '%';
              }
            }
          }
        },
        cutout: '60%'
      }
    });
  }

  // Export Distribution by Region Chart
  const regionCtx = document.getElementById('regionChart');
  if (regionCtx) {
    new Chart(regionCtx, {
      type: 'bar',
      data: {
        labels: ['North America', 'Europe', 'Middle East', 'Asia', 'Africa', 'South America'],
        datasets: [{
          label: 'Export Volume (Tons)',
          data: [450, 380, 290, 220, 180, 120],
          backgroundColor: '#4a5d3f',
          borderColor: '#4a5d3f',
          borderWidth: 0,
          borderRadius: 8,
          barPercentage: 0.7
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            backgroundColor: 'rgba(45, 24, 16, 0.9)',
            titleColor: '#fff',
            bodyColor: '#fff',
            padding: 12,
            displayColors: false,
            callbacks: {
              label: function(context) {
                return context.parsed.y + ' tons';
              }
            }
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            grid: {
              color: 'rgba(200, 161, 101, 0.1)'
            },
            ticks: {
              callback: function(value) {
                return value + ' tons';
              }
            }
          },
          x: {
            grid: {
              display: false
            }
          }
        }
      }
    });
  }

  // Quality Metrics Chart
  const qualityCtx = document.getElementById('qualityChart');
  if (qualityCtx) {
    new Chart(qualityCtx, {
      type: 'radar',
      data: {
        labels: ['Purity', 'Aroma', 'Freshness', 'Grading', 'Packaging', 'Moisture'],
        datasets: [{
          label: 'Current Month',
          data: [95, 92, 88, 94, 90, 87],
          borderColor: '#c8a165',
          backgroundColor: 'rgba(200, 161, 101, 0.2)',
          borderWidth: 2,
          pointBackgroundColor: '#c8a165',
          pointBorderColor: '#fff',
          pointBorderWidth: 2,
          pointRadius: 4
        }, {
          label: 'Previous Month',
          data: [92, 89, 85, 91, 88, 84],
          borderColor: '#4a5d3f',
          backgroundColor: 'rgba(74, 93, 63, 0.1)',
          borderWidth: 2,
          pointBackgroundColor: '#4a5d3f',
          pointBorderColor: '#fff',
          pointBorderWidth: 2,
          pointRadius: 4
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              padding: 15,
              usePointStyle: true,
              font: {
                size: 11
              }
            }
          },
          tooltip: {
            backgroundColor: 'rgba(45, 24, 16, 0.9)',
            titleColor: '#fff',
            bodyColor: '#fff',
            padding: 12,
            displayColors: false
          }
        },
        scales: {
          r: {
            beginAtZero: true,
            max: 100,
            ticks: {
              stepSize: 20,
              callback: function(value) {
                return value + '%';
              }
            },
            grid: {
              color: 'rgba(200, 161, 101, 0.1)'
            },
            pointLabels: {
              font: {
                size: 11
              }
            }
          }
        }
      }
    });
  }
}
