// Comprobar si el modo oscuro estaba activado previamente en localStorage
let isDarkMode = localStorage.getItem("darkMode") === "enabled";

function applyTheme() {
    const dashboard = document.getElementById("dashboard");
    const sidebar = document.getElementById("sidebar");
    const themeIcon = document.getElementById("theme-icon");
    const body = document.body; 

    if (isDarkMode) {
        body.classList.add("dark");
        dashboard.classList.add("dark");
        sidebar.classList.add("dark"); // Asegurar que el sidebar también cambie
        themeIcon.classList.replace("bx-moon", "bx-sun");

        // Actualizar filtros al modo oscuro
        document.querySelectorAll(".filter-select").forEach(select => {
            select.classList.add("dark:bg-gray-700", "dark:text-gray-300", "dark:border-gray-600");
        });
    } else {
        body.classList.remove("dark");
        dashboard.classList.remove("dark");
        sidebar.classList.remove("dark");
        themeIcon.classList.replace("bx-sun", "bx-moon");

        // Actualizar filtros al modo claro
        document.querySelectorAll(".filter-select").forEach(select => {
            select.classList.remove("dark:bg-gray-700", "dark:text-gray-300", "dark:border-gray-600");
        });
    }

    // Aplicar el cambio de color en los gráficos
    updateChartColors(isDarkMode);
}

function toggleSidebar() {
    const sidebar = document.getElementById("sidebar");
    sidebar.classList.toggle("collapsed");
}

function toggleTheme() {
    isDarkMode = !isDarkMode;
    localStorage.setItem("darkMode", isDarkMode ? "enabled" : "disabled");
    applyTheme(); // Aplicar cambios de inmediato
}

// Función para actualizar los colores de los gráficos según el modo
function updateChartColors(isDarkMode) {
    const textColor = isDarkMode ? "#f1f1f1" : "#333"; // Blanco en modo oscuro, gris oscuro en modo claro

    // Actualizar las opciones de los gráficos
    chartClases.options.scales.x.ticks.color = textColor;
    chartClases.options.scales.y.ticks.color = textColor;
    chartClases.options.plugins.legend.labels.color = textColor;

    chartCumplimiento.options.plugins.legend.labels.color = textColor;

    // Actualizar los gráficos para reflejar los cambios
    chartClases.update();
    chartCumplimiento.update();
}

function logoutUser() {
    Swal.fire({
        title: '¿Estás seguro?',
        text: "Tu sesión será cerrada.",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        confirmButtonText: 'Sí, cerrar sesión',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = "{% url 'logout' %}";
        }
    });
}

// Aplicar el tema correcto al cargar la página
document.addEventListener("DOMContentLoaded", applyTheme);

document.addEventListener("DOMContentLoaded", function () {
    // Datos de prueba para los gráficos
    const clasesData = {
        labels: ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes'],
        datasets: [
            {
                label: 'Clases',
                data: [14, 18, 20, 25, 22],
                borderColor: '#007bff',
                backgroundColor: 'rgba(0, 123, 255, 0.2)',
                borderWidth: 2
            },
            {
                label: 'Docentes',
                data: [10, 15, 16, 20, 18],
                borderColor: '#00C49F',
                backgroundColor: 'rgba(0, 196, 159, 0.2)',
                borderWidth: 2
            }
        ]
    };

    const cumplimientoData = {
        labels: ['Cumplimiento', 'Incumplimiento'],
        datasets: [{
            data: [75, 25],
            backgroundColor: ['#00C49F', '#FF4444']
        }]
    };

    // Configuración de los gráficos
    const configClases = {
        type: 'line',
        data: clasesData,
        options: {
            responsive: true,
            plugins: {
                legend: { display: true }
            },
            maintainAspectRatio: false, // Aseguramos que se mantenga el tamaño del canvas
            interaction: {
                mode: 'index', // Hacer los gráficos interactivos al pasar el mouse
                intersect: false
            },
            scales: {
                x: {
                    ticks: {
                        color: isDarkMode ? "#f1f1f1" : "#333", // Cambio de color dinámico
                    }
                },
                y: {
                    ticks: {
                        color: isDarkMode ? "#f1f1f1" : "#333", // Cambio de color dinámico
                    }
                }
            }
        }
    };

    const configCumplimiento = {
        type: 'pie',
        data: cumplimientoData,
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: true,
                    labels: {
                        color: isDarkMode ? "#f1f1f1" : "#333", // Cambio de color dinámico
                    }
                }
            },
            maintainAspectRatio: false, // Aseguramos que se mantenga el tamaño del canvas
            interaction: {
                mode: 'nearest', // Hacer los gráficos interactivos
                intersect: false
            }
        }
    };

    // Crear los gráficos y almacenarlos en variables
    chartClases = new Chart(document.getElementById('clasesChart'), configClases);
    chartCumplimiento = new Chart(document.getElementById('cumplimientoChart'), configCumplimiento);
});

function confirmLogout() {
    Swal.fire({
        title: '¿Estás seguro?',
        text: "Tu sesión será cerrada.",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        confirmButtonText: 'Sí, cerrar sesión',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            // Enviar el formulario de logout
            document.getElementById('logout-form').submit();
        }
    });
}

const container = document.querySelector('.container');
const registerBtn = document.querySelector('.register-btn');
const loginBtn = document.querySelector('.login-btn');

registerBtn.addEventListener('click', () => {
    container.classList.add('active');
});

loginBtn.addEventListener('click', () => {
    container.classList.remove('active');
});

// Sidebar responsive para móvil
document.addEventListener("DOMContentLoaded", function () {
    const sidebar = document.getElementById('sidebar');
    const hamburgerBtn = document.getElementById('hamburgerBtn');
    const closeSidebarBtn = document.getElementById('closeSidebarBtn');
    if (hamburgerBtn && sidebar) {
        hamburgerBtn.addEventListener('click', function() {
            sidebar.classList.add('active');
            if (closeSidebarBtn) closeSidebarBtn.style.display = 'inline-block';
        });
    }
    if (closeSidebarBtn && sidebar) {
        closeSidebarBtn.addEventListener('click', function() {
            sidebar.classList.remove('active');
            closeSidebarBtn.style.display = 'none';
        });
    }
    // Cerrar sidebar al hacer click fuera en móvil
    document.addEventListener('click', function(e) {
        if (window.innerWidth <= 768 && sidebar && sidebar.classList.contains('active')) {
            if (!sidebar.contains(e.target) && e.target !== hamburgerBtn) {
                sidebar.classList.remove('active');
                if (closeSidebarBtn) closeSidebarBtn.style.display = 'none';
            }
        }
    });
});