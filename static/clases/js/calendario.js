document.addEventListener('DOMContentLoaded', () => {
    const calendarioEl = document.getElementById('calendar');

    if (!calendarioEl) {
        console.error("❌ Contenedor del calendario no encontrado");
        return;
    }

    // ✅ Parsear datos enviados desde el backend
    const listaDocentes = JSON.parse(document.getElementById('docentes-json').textContent);
    const listaMaterias = JSON.parse(document.getElementById('materias-json').textContent);
    const listaAulas = JSON.parse(document.getElementById('aulas-json').textContent);
    const listaClases = JSON.parse(document.getElementById('clases-json').textContent);

    // Asegura que ES_STAFF sea booleano verdadero si es true o "true"
    const ES_STAFF = window.ES_STAFF === true || window.ES_STAFF === "true";
    const USER_ID = window.USER_ID;

    const calendar = new FullCalendar.Calendar(calendarioEl, {
        initialView: 'dayGridMonth',
        locale: 'es',
        aspectRatio: 1.5,
        height: 'auto',
        contentHeight: 600,
        scrollTime: '08:00:00',
        events: listaClases.map(clase => {
            const now = new Date();
            const endDate = new Date(`${clase.fecha}T${clase.hora_fin}`);
            // Sumar 12 horas a la hora de fin
            const endDatePlus12h = new Date(endDate.getTime() + 12 * 60 * 60 * 1000);
            const isInactive = endDatePlus12h < now;

            // Buscar el aula correspondiente
            const aulaObj = listaAulas.find(aula => aula.id == clase['aula__id']);
            // Buscar la materia por id para obtener la descripción
            const materiaObj = listaMaterias.find(m => m.id == clase['materia__id']);

            return {
                id: clase.id,
                // Cambia aquí: usa la descripción de la materia
                title: `${materiaObj ? materiaObj.descripcion : 'Sin materia'} - ${clase['docente__nombre']}`,
                start: `${clase.fecha}T${clase.hora_inicio}`,
                end: `${clase.fecha}T${clase.hora_fin}`,
                className: isInactive ? 'pasado' : 'activo',
                extendedProps: {
                    aula: aulaObj ? `${aulaObj.codigo_aula} - ${aulaObj.descripcion}` : 'No especificado',
                    docente_id: clase['docente__id'],
                    materia_id: clase['materia__id'],
                    aula_id: clase['aula__id']
                }
            };
        }),
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        dateClick: function(info) {
            // Eliminar este bloque:
            // if (!ES_STAFF) {
            //     Swal.fire('Acción no permitida', 'Solo el personal autorizado puede registrar clases.', 'warning');
            //     return;
            // }
            // Ahora todos pueden crear clases

            let docenteSelectHtml;
            if (ES_STAFF) {
                docenteSelectHtml = `
                    <label>Docente</label>
                    <select id="docente" class="swal2-input" style="grid-column: span 2;">
                        ${listaDocentes.map(docente => `<option value="${docente.id}">${docente.nombre}</option>`).join('')}
                    </select>
                `;
            } else {
                const docente = listaDocentes.find(d => d.id == USER_ID);
                docenteSelectHtml = `
                    <label>Docente</label>
                    <select id="docente" class="swal2-input" style="grid-column: span 2;" disabled>
                        <option value="${docente.id}">${docente.nombre}</option>
                    </select>
                `;
            }
            Swal.fire({
                title: 'Registrar Clase',
                html: `
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; text-align: left;">
                        ${docenteSelectHtml}
                        <label>Materia</label>
                        <select id="materia" class="swal2-input" style="grid-column: span 2;">
                            ${listaMaterias.map(materia => `
                                <option value="${materia.id}">
                                    ${materia.codigo_materia} - ${materia.descripcion} (Trayecto: ${materia.trayecto})
                                </option>
                            `).join('')}
                        </select>

                        <label>Aula</label>
                        <select id="aula" class="swal2-input" style="grid-column: span 2;">
                            ${listaAulas.map(aula => `
                                <option value="${aula.id}">
                                    ${aula.codigo_aula} - ${aula.descripcion}
                                </option>`).join('')}
                        </select>

                        <label>Hora Inicio</label>
                        <input id="hora_inicio" type="time" class="swal2-input" value="08:00">

                        <label>Hora Fin</label>
                        <input id="hora_fin" type="time" class="swal2-input" value="09:00">
                    </div>
                `,
                confirmButtonText: 'Guardar',
                showCancelButton: true,
                cancelButtonText: 'Cancelar',
                preConfirm: () => {
                    const materia = document.getElementById('materia').value;
                    const aula = document.getElementById('aula').value;
                    let docenteId;
                    if (ES_STAFF) {
                        docenteId = document.getElementById('docente').value;
                    } else {
                        docenteId = USER_ID;
                    }
                    const hora_inicio = document.getElementById('hora_inicio').value;
                    const hora_fin = document.getElementById('hora_fin').value;

                    if (!materia || !aula || !hora_inicio || !hora_fin) {
                        Swal.showValidationMessage('Todos los campos son obligatorios');
                        return false;
                    }

                    return {
                        materia_id: materia,
                        aula_id: aula,
                        docente_id: docenteId,
                        fecha_inicio: info.dateStr,
                        hora_inicio,
                        hora_fin
                    };
                }
            }).then((result) => {
                if (result.isConfirmed) {
                    const nuevaClase = result.value;

                    fetch('/clases/registrar-clase/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': getCookie('csrftoken')
                        },
                        body: JSON.stringify(nuevaClase)
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.status === 'success') {
                            Swal.fire('Clase Registrada', 'La clase fue creada exitosamente.', 'success');
                            calendar.addEvent({
                                id: data.id,
                                title: `${listaMaterias.find(m => m.id == nuevaClase.materia_id).nombre} - ${listaDocentes.find(d => d.id == nuevaClase.docente_id).nombre}`,
                                start: `${nuevaClase.fecha_inicio}T${nuevaClase.hora_inicio}`,
                                end: `${nuevaClase.fecha_inicio}T${nuevaClase.hora_fin}`,
                                extendedProps: {
                                    aula: (() => {
                                        const aulaObj = listaAulas.find(aula => aula.id == nuevaClase.aula_id);
                                        return aulaObj ? `${aulaObj.codigo_aula} - ${aulaObj.descripcion}` : 'No especificado';
                                    })()
                                }
                            });
                        } else {
                            Swal.fire('Error', data.message || 'No se pudo registrar la clase.', 'error');
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        Swal.fire('Error', 'Ocurrió un error al registrar la clase.', 'error');
                    });
                }
            });
        },
        eventClick: function(info) {
            // ✅ Mostrar información de la clase y permitir acciones
            Swal.fire({
                title: info.event.title,
                html: `
                    <p><strong>Aula:</strong> ${info.event.extendedProps.aula || 'No especificado'}</p>
                    <p><strong>Inicio:</strong> ${info.event.start.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit', hour12: true })}</p>
                    <p><strong>Fin:</strong> ${info.event.end ? info.event.end.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit', hour12: true }) : 'No especificado'}</p>
                    <div style="display: flex; justify-content: space-around; margin-top: 20px;">
                        ${ES_STAFF ? `
                        <button id="btn-eliminar" class="swal2-styled" style="background-color: #dc3545; color: white; border: none; padding: 10px; border-radius: 5px; font-size: 12px;">
                            <i class="fas fa-trash-alt" style="font-size: 14px; margin-right: 5px;"></i> Eliminar
                        </button>
                        <button id="btn-reprogramar" class="swal2-styled" style="background-color: #ffc107; color: white; border: none; padding: 10px; border-radius: 5px; font-size: 12px;">
                            <i class="fas fa-edit" style="font-size: 14px; margin-right: 5px;"></i> Reprogramar
                        </button>
                        ` : ''}
                        <button id="btn-asistencia" class="swal2-styled" style="background-color: #28a745; color: white; border: none; padding: 10px; border-radius: 5px; font-size: 12px;">
                            <i class="fas fa-check-circle" style="font-size: 14px; margin-right: 5px;"></i> Asistencia
                        </button>
                    </div>
                `,
                showConfirmButton: false,
                didOpen: () => {
                    if (ES_STAFF) {
                        document.getElementById('btn-eliminar').addEventListener('click', () => {
                            Swal.fire({
                                title: '¿Estás seguro?',
                                text: 'Esta acción eliminará la clase seleccionada.',
                                icon: 'warning',
                                showCancelButton: true,
                                confirmButtonText: 'Sí, eliminar',
                                cancelButtonText: 'Cancelar'
                            }).then((result) => {
                                if (result.isConfirmed) {
                                    fetch(`/clases/eliminar-clase/`, {
                                        method: 'DELETE',
                                        headers: {
                                            'Content-Type': 'application/json',
                                            'X-CSRFToken': getCookie('csrftoken')
                                        },
                                        body: JSON.stringify({ id: info.event.id })
                                    })
                                    .then(response => response.json())
                                    .then(data => {
                                        if (data.status === 'success') {
                                            Swal.fire('Eliminado', 'La clase ha sido eliminada.', 'success');
                                            info.event.remove(); // ✅ Eliminar el evento del calendario
                                        } else {
                                            Swal.fire('Error', data.message || 'No se pudo eliminar la clase.', 'error');
                                        }
                                    })
                                    .catch(error => {
                                        console.error('Error:', error);
                                        Swal.fire('Error', 'Ocurrió un error al eliminar la clase.', 'error');
                                    });
                                }
                            });
                        });

                        // ✅ Acción para el botón "Reprogramar"
                        document.getElementById('btn-reprogramar').addEventListener('click', () => {
                            Swal.fire({
                                title: 'Reprogramar Clase',
                                html: `
                                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; text-align: left;">
                                        <label>Docente</label>
                                        <select id="docente" class="swal2-input" style="grid-column: span 2;">
                                            ${listaDocentes.map(docente => `
                                                <option value="${docente.id}" ${docente.id == info.event.extendedProps.docente_id ? 'selected' : ''}>
                                                    ${docente.nombre}
                                                </option>`).join('')}
                                        </select>

                                        <label>Materia</label>
                                        <select id="materia" class="swal2-input" style="grid-column: span 2;">
                                            ${listaMaterias.map(materia => `
                                                <option value="${materia.id}" ${materia.id == info.event.extendedProps.materia_id ? 'selected' : ''}>
                                                    ${materia.codigo_materia} - ${materia.descripcion} (Trayecto: ${materia.trayecto})
                                                </option>`).join('')}
                                        </select>

                                        <label>Aula</label>
                                        <select id="aula" class="swal2-input" style="grid-column: span 2;">
                                            ${listaAulas.map(aula => `
                                                <option value="${aula.id}" ${aula.id == info.event.extendedProps.aula_id ? 'selected' : ''}>
                                                    ${aula.codigo_aula} - ${aula.descripcion}
                                                </option>`).join('')}
                                        </select>

                                        <label>Hora Inicio</label>
                                        <input id="hora_inicio" type="time" class="swal2-input" value="${info.event.start.toISOString().substring(11, 16)}">

                                        <label>Hora Fin</label>
                                        <input id="hora_fin" type="time" class="swal2-input" value="${info.event.end ? info.event.end.toISOString().substring(11, 16) : ''}">
                                    </div>
                                `,
                                confirmButtonText: 'Guardar',
                                showCancelButton: true,
                                cancelButtonText: 'Cancelar',
                                preConfirm: () => {
                                    const materia = document.getElementById('materia').value;
                                    const aula = document.getElementById('aula').value;
                                    const docenteId = document.getElementById('docente').value;
                                    const hora_inicio = document.getElementById('hora_inicio').value;
                                    const hora_fin = document.getElementById('hora_fin').value;

                                    if (!materia || !aula || !hora_inicio || !hora_fin) {
                                        Swal.showValidationMessage('Todos los campos son obligatorios');
                                        return false;
                                    }

                                    return {
                                        id: info.event.id,
                                        materia_id: materia,
                                        aula_id: aula,
                                        docente_id: docenteId,
                                        fecha_inicio: info.event.start.toISOString().substring(0, 10),
                                        hora_inicio,
                                        hora_fin
                                    };
                                }
                            }).then((result) => {
                                if (result.isConfirmed) {
                                    fetch(`/clases/reprogramar-clase/`, {
                                        method: 'PUT',
                                        headers: {
                                            'Content-Type': 'application/json',
                                            'X-CSRFToken': getCookie('csrftoken')
                                        },
                                        body: JSON.stringify(result.value)
                                    })
                                    .then(response => response.json())
                                    .then(data => {
                                        if (data.status === 'success') {
                                            Swal.fire('Reprogramado', 'La clase ha sido actualizada.', 'success');
                                            // ✅ Actualizar el evento en el calendario dinámicamente
                                            const updatedEvent = calendar.getEventById(info.event.id);
                                            updatedEvent.setProp('title', `${listaMaterias.find(m => m.id == result.value.materia_id).nombre} - ${listaDocentes.find(d => d.id == result.value.docente_id).nombre}`);
                                            updatedEvent.setStart(`${result.value.fecha_inicio}T${result.value.hora_inicio}`);
                                            updatedEvent.setEnd(`${result.value.fecha_inicio}T${result.value.hora_fin}`);
                                            updatedEvent.setExtendedProp('aula', (() => {
                                                const aulaObj = listaAulas.find(aula => aula.id == result.value.aula_id);
                                                return aulaObj ? `${aulaObj.codigo_aula} - ${aulaObj.descripcion}` : 'No especificado';
                                            })());
                                        } else {
                                            Swal.fire('Error', data.message || 'No se pudo reprogramar la clase.', 'error');
                                        }
                                    })
                                    .catch(error => {
                                        console.error('Error:', error);
                                        Swal.fire('Error', 'Ocurrió un error al reprogramar la clase.', 'error');
                                    });
                                }
                            });
                        });
                    }

                    // ✅ Acción para el botón "Registrar Asistencia"
                    document.getElementById('btn-asistencia').addEventListener('click', () => {
                        Swal.fire({
                            title: 'Registrar Asistencia',
                            html: `
                                <form id="asistencia-form" enctype="multipart/form-data">
                                    <label for="foto_clase">Foto de la Clase:</label>
                                    <input id="foto_clase" name="foto_clase" type="file" class="swal2-input" accept="image/*" required>

                                    <label for="foto_lista">Foto de la Lista:</label>
                                    <input id="foto_lista" name="foto_lista" type="file" class="swal2-input" accept="image/*" required>

                                    <label for="foto_selfie">Selfie del Docente:</label>
                                    <input id="foto_selfie" name="foto_selfie" type="file" class="swal2-input" accept="image/*" required>

                                    <label for="comentarios">Comentarios:</label>
                                    <textarea id="comentarios" name="comentarios" class="swal2-textarea" rows="3" placeholder="Opcional"></textarea>
                                </form>
                            `,
                            confirmButtonText: 'Guardar',
                            showCancelButton: true,
                            cancelButtonText: 'Cancelar',
                            preConfirm: () => {
                                const formData = new FormData();
                                const fotoClase = document.getElementById('foto_clase').files[0];
                                const fotoLista = document.getElementById('foto_lista').files[0];
                                const fotoSelfie = document.getElementById('foto_selfie').files[0];
                                const comentarios = document.getElementById('comentarios').value;

                                if (!fotoClase || !fotoLista || !fotoSelfie) {
                                    Swal.showValidationMessage('Debe subir todas las fotos requeridas.');
                                    return false;
                                }

                                formData.append('clase_id', info.event.id);
                                formData.append('foto_clase', fotoClase);
                                formData.append('foto_lista', fotoLista);
                                formData.append('foto_selfie', fotoSelfie);
                                formData.append('comentarios', comentarios);

                                return formData;
                            }
                        }).then((result) => {
                            if (result.isConfirmed) {
                                fetch('/clases/registrar-asistencia/', {
                                    method: 'POST',
                                    headers: {
                                        'X-CSRFToken': getCookie('csrftoken')
                                    },
                                    body: result.value
                                })
                                .then(response => response.json())
                                .then(data => {
                                    if (data.status === 'success') {
                                        Swal.fire('Asistencia Registrada', 'La asistencia fue registrada exitosamente.', 'success');
                                    } else {
                                        Swal.fire('Error', data.message || 'No se pudo registrar la asistencia.', 'error');
                                    }
                                })
                                .catch(error => {
                                    console.error('Error:', error);
                                    Swal.fire('Error', 'Ocurrió un error al registrar la asistencia.', 'error');
                                });
                            }
                        });
                    });
                }
            });
        }
    });

    calendar.render();
    console.log("✅ Calendario cargado correctamente");

    const filterEstado = document.getElementById('filter-estado');

    function applyFilters() {
        const estado = filterEstado.value;
        const now = new Date();

        calendar.getEvents().forEach(event => {
            let mostrar = true;
            if (estado === 'finalizadas') {
                // Mostrar solo si han pasado más de 12 horas desde la hora de fin
                if (event.end) {
                    const endDatePlus12h = new Date(event.end.getTime() + 12 * 60 * 60 * 1000);
                    mostrar = endDatePlus12h < now;
                } else {
                    mostrar = false;
                }
            } else if (estado === 'por-ver') {
                // Mostrar solo si la clase sigue activa (no han pasado 12 horas desde la hora de fin)
                if (event.end) {
                    const endDatePlus12h = new Date(event.end.getTime() + 12 * 60 * 60 * 1000);
                    mostrar = endDatePlus12h >= now;
                } else {
                    mostrar = true;
                }
            }
            event.setProp('display', (!estado || mostrar) ? '' : 'none');
        });
    }

    filterEstado.addEventListener('change', applyFilters);

    // Aplica el filtro al cargar la página
    calendar.on('eventsSet', applyFilters);
});

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

// Todo el código ya usa los campos id, nombre, cedula, codigo_aula, descripcion, etc.
// Si los datos del backend están correctos, el frontend funcionará correctamente.
