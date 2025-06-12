document.addEventListener('DOMContentLoaded', () => {
    const calendarioEl = document.getElementById('calendario');

    if (!calendarioEl) {
        console.error('No se encontró el contenedor del calendario.');
        return;
    }

    const calendar = new FullCalendar.Calendar(calendarioEl, {
        initialView: 'dayGridMonth',
        locale: 'es',
        events: '/clases/eventos/', // URL para obtener las clases
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        dateClick: function(info) {
            const nombreClase = prompt('Introduce el nombre de la clase:');
            if (nombreClase) {
                const docente = prompt('Introduce el nombre del docente:');
                const carrera = prompt('Introduce la carrera:');
                const clase = {
                    title: nombreClase,
                    start: info.dateStr,
                    docente: docente,
                    carrera: carrera
                };

                // Enviar la clase al backend
                fetch('/clases/registrar_evento/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken') // Obtener el token CSRF
                    },
                    body: JSON.stringify(clase)
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        alert('Clase registrada correctamente.');
                        calendar.refetchEvents(); // Recargar las clases
                    } else {
                        alert('Error al registrar la clase: ' + data.message);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Error al registrar la clase.');
                });
            }
        }
    });

    calendar.render();
});

// Función para obtener el token CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
