document.addEventListener("DOMContentLoaded", function () {
    // Confirmar eliminación de un docente
    window.confirmDelete = function (docenteId) {
        Swal.fire({
            title: "¿Estás seguro?",
            text: "Esta acción no se puede deshacer.",
            icon: "warning",
            showCancelButton: true,
            confirmButtonColor: "#d33",
            cancelButtonColor: "#3085d6",
            confirmButtonText: "Sí, eliminar",
            cancelButtonText: "Cancelar"
        }).then((result) => {
            if (result.isConfirmed) {
                fetch(`/docentes/eliminar/${docenteId}/`, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": getCSRFToken(),
                        "Content-Type": "application/json"
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        Swal.fire("Eliminado", "El docente ha sido eliminado.", "success")
                            .then(() => location.reload());
                    } else {
                        Swal.fire("Error", "No se pudo eliminar el docente.", "error");
                    }
                })
                .catch(error => {
                    console.error("Error:", error);
                    Swal.fire("Error", "Ocurrió un problema al eliminar.", "error");
                });
            }
        });
    };

    // Obtener el CSRF Token
    function getCSRFToken() {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            let cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                let cookie = cookies[i].trim();
                if (cookie.startsWith("csrftoken=")) {
                    cookieValue = decodeURIComponent(cookie.split("=")[1]);
                    break;
                }
            }
        }
        return cookieValue;
    }

    const selectAllCheckbox = document.getElementById("selectAll");
    const docenteCheckboxes = document.querySelectorAll(".docenteCheckbox");
    const selectionControls = document.getElementById("selectionControls");
    const selectedCount = document.getElementById("selectedCount");
    const deleteSelectedButton = document.getElementById("deleteSelected");
    const selectAllRecordsButton = document.getElementById("selectAllRecords");
    let allSelectedIds = new Set();
    let allSelected = false;

    // Seleccionar/Deseleccionar todos los registros visibles
    selectAllCheckbox.addEventListener("change", () => {
        if (selectAllCheckbox.checked) {
            docenteCheckboxes.forEach(checkbox => {
                checkbox.checked = true;
                allSelectedIds.add(checkbox.value);
            });
        } else {
            docenteCheckboxes.forEach(checkbox => {
                checkbox.checked = false;
            });
            allSelectedIds.clear();
        }
        updateSelectionControls();
    });

    // Actualizar el conjunto de IDs seleccionados al cambiar un checkbox individual
    docenteCheckboxes.forEach(checkbox => {
        checkbox.addEventListener("change", () => {
            if (checkbox.checked) {
                allSelectedIds.add(checkbox.value);
            } else {
                allSelectedIds.delete(checkbox.value);
            }
            updateSelectionControls();
        });
    });

    // Actualizar controles de selección
    function updateSelectionControls() {
        const selectedCountValue = allSelectedIds.size;
        if (selectedCountValue > 0) {
            selectionControls.classList.remove("hidden");
            selectedCount.textContent = `${selectedCountValue} seleccionados`;
        } else {
            selectionControls.classList.add("hidden");
            selectedCount.textContent = `0 seleccionados`;
        }
        selectAllCheckbox.checked = docenteCheckboxes.length > 0 && Array.from(docenteCheckboxes).every(checkbox => checkbox.checked);
    }

    // Seleccionar/Deseleccionar todos los registros (incluidos los no visibles)
    selectAllRecordsButton.addEventListener("click", () => {
        if (!allSelected) {
            // Seleccionar todos
            fetch("/docentes/obtener_todos_los_ids/")
                .then(response => response.json())
                .then(data => {
                    if (data.ids) {
                        allSelectedIds = new Set(data.ids);
                        docenteCheckboxes.forEach(checkbox => {
                            checkbox.checked = true;
                        });
                        updateSelectionControls();
                        selectAllRecordsButton.textContent = "Deseleccionar todos"; // Cambiar texto del botón
                        allSelected = true;
                    }
                })
                .catch(error => {
                    console.error("Error al obtener los IDs:", error);
                });
        } else {
            // Deseleccionar todos
            docenteCheckboxes.forEach(checkbox => {
                checkbox.checked = false;
            });
            allSelectedIds.clear(); // Vaciar el conjunto
            updateSelectionControls();
            selectAllRecordsButton.textContent = "Seleccionar todos"; // Cambiar texto del botón
            allSelected = false;

            // Asegurarse de desmarcar el checkbox del encabezado
            selectAllCheckbox.checked = false;
        }
    });

    // Eliminar registros seleccionados
    deleteSelectedButton.addEventListener("click", () => {
        if (allSelectedIds.size > 0) {
            Swal.fire({
                title: "¿Estás seguro?",
                text: "Esta acción eliminará los registros seleccionados.",
                icon: "warning",
                showCancelButton: true,
                confirmButtonColor: "#d33",
                cancelButtonColor: "#3085d6",
                confirmButtonText: "Sí, eliminar",
                cancelButtonText: "Cancelar"
            }).then((result) => {
                if (result.isConfirmed) {
                    fetch("/docentes/eliminar_seleccionados/", {
                        method: "POST",
                        headers: {
                            "X-CSRFToken": getCSRFToken(),
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({ ids: Array.from(allSelectedIds) })
                    })
                        .then(response => response.json())
                        .then(data => {
                            if (data.success) {
                                Swal.fire("Eliminados", "Los registros seleccionados han sido eliminados.", "success")
                                    .then(() => location.reload());
                            } else {
                                Swal.fire("Error", "No se pudieron eliminar los registros seleccionados.", "error");
                            }
                        })
                        .catch(error => {
                            console.error("Error:", error);
                            Swal.fire("Error", "Ocurrió un problema al eliminar.", "error");
                        });
                }
            });
        }
    });

    // Obtener el CSRF Token
    function getCSRFToken() {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            let cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                let cookie = cookies[i].trim();
                if (cookie.startsWith("csrftoken=")) {
                    cookieValue = decodeURIComponent(cookie.split("=")[1]);
                    break;
                }
            }
        }
        return cookieValue;
    }
});

// Comprobar si el modo oscuro estaba activado previamente en localStorage
let isDarkMode = localStorage.getItem("darkMode") === "enabled";

function applyTheme() {
    const body = document.getElementById("body");
    if (isDarkMode) {
        form.classList.add("dark");
        body.classList.add("dark");
    } else {
        form.classList.remove("dark");
        body.classList.remove("dark");
    }
}

// Aplicar el tema correcto al cargar la página
document.addEventListener("DOMContentLoaded", applyTheme);


function confirmDelete(docenteId) {
    Swal.fire({
        title: "¿Estás seguro?",
        text: "Esta acción no se puede deshacer.",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#d33",
        cancelButtonColor: "#3085d6",
        confirmButtonText: "Sí, eliminar",
        cancelButtonText: "Cancelar"
    }).then((result) => {
        if (result.isConfirmed) {
            fetch(`/docentes/eliminar/${docenteId}/`, {
                method: "POST",  // Cambiado de DELETE a POST para evitar problemas con CSRF
                headers: {
                    "X-CSRFToken": getCSRFToken(),  // ✅ Asegurar el CSRF Token
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ id: docenteId })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    Swal.fire("Eliminado", "El docente ha sido eliminado.", "success")
                        .then(() => location.reload());
                } else {
                    Swal.fire("Error", "No se pudo eliminar el docente.", "error");
                }
            })
            .catch(error => {
                console.error("Error:", error);
                Swal.fire("Error", "Ocurrió un problema al eliminar.", "error");
            });
        }
    });
}

// ✅ Función para obtener el CSRF Token
function getCSRFToken() {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        let cookies = document.cookie.split(";");
        for (let i = 0; cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.startsWith("csrftoken=")) {
                cookieValue = decodeURIComponent(cookie.split("=")[1]);
                break;
            }
        }
    }
    return cookieValue;
}


// Función para abrir el modal
function openModal(action) {
    const modal = document.getElementById("modalFormat");
    const modalTitle = document.getElementById("modalTitle");

    if (action === "import") {
        modalTitle.textContent = "Seleccione el formato de Importación";
        modal.setAttribute("data-action", "import");
    } else if (action === "export") {
        modalTitle.textContent = "Seleccione el formato de Exportación";
        modal.setAttribute("data-action", "export");
    }

    modal.classList.remove("hidden");
}

// Función para cerrar el modal
function closeModal() {
    const modal = document.getElementById("modalFormat");
    modal.classList.add("hidden");
}

// Cerrar modal al presionar "Cancelar"
document.querySelector(".btn-cancel").addEventListener("click", closeModal);

// Cerrar modal si se hace clic fuera de él
document.getElementById("modalFormat").addEventListener("click", (event) => {
    if (event.target === document.getElementById("modalFormat")) {
        closeModal();
    }
});

// Manejar la selección del formato y abrir el explorador de archivos
document.querySelectorAll(".btn-format").forEach(button => {
    button.addEventListener("click", function () {
        const format = this.getAttribute("data-format");
        const fileInput = document.getElementById("fileInput");

        // Configurar el atributo "accept" del input de archivo según el formato seleccionado
        let acceptTypes = "";
        switch (format) {
            case "csv":
                acceptTypes = ".csv";
                break;
            case "excel":
                acceptTypes = ".xls,.xlsx";
                break;
            case "sql":
                acceptTypes = ".sql";
                break;
            case "json":
                acceptTypes = ".json";
                break;
            case "xml":
                acceptTypes = ".xml";
                break;
            case "pdf":
                acceptTypes = ".pdf";
                break;
        }
        fileInput.setAttribute("accept", acceptTypes);

        // Abrir el explorador de archivos
        fileInput.click();

        // Manejar el evento de cambio del input de archivo
        fileInput.onchange = function () {
            if (fileInput.files.length > 0) {
                const selectedFile = fileInput.files[0];
                console.log("Archivo seleccionado:", selectedFile.name);

                // Aquí puedes agregar lógica para manejar la subida del archivo
                // Por ejemplo, enviar el archivo al servidor mediante fetch o un formulario
            }
        };

        // Cerrar el modal después de seleccionar el formato
        closeModal();
    });
});

function handleAction(format) {
    const modal = document.getElementById("modalFormat");
    const action = modal.getAttribute("data-action");

    if (action === "import") {
        const input = document.createElement("input");
        input.type = "file";
        input.accept = getAcceptFormat(format);
        input.onchange = () => handleImport(input.files[0]);
        input.click();
    } else if (action === "export") {
        const exportUrl = `/docentes/exportar/${format}/all/`;
        window.location.href = exportUrl;
    }
}

function getAcceptFormat(format) {
    const formats = {
        csv: ".csv",
        excel: ".xls,.xlsx",
        sql: ".sql",
        json: ".json",
        xml: ".xml",
        pdf: ".pdf"
    };
    return formats[format] || "";
}

function handleImport(file) {
    const form = new FormData();
    form.append("csrfmiddlewaretoken", getCSRFToken());
    form.append("file", file);

    fetch("/docentes/importar/", {
        method: "POST",
        body: form
    })
    .then(response => {
        if (response.ok) {
            location.reload();
        } else {
            response.text().then(text => alert("Error al importar el archivo: " + text));
        }
    })
    .catch(error => {
        alert("Hubo un error al procesar el archivo: " + error.message);
    });
}

// Mostrar el modal con la información del docente
function mostrarDocente(docenteId) {
    // Obtener el modal y el contenedor de información
    const modal = document.getElementById("modalDocente");
    const docenteInfo = document.getElementById("docenteInfo");

    // Realizar una solicitud AJAX para obtener la información del docente
    fetch(`/docentes/detalle/${docenteId}/`)
        .then(response => response.json())
        .then(data => {
            // Cargar la información del docente en el modal
            docenteInfo.innerHTML = `
                <p><strong>Nombre:</strong> ${data.nombre}</p>
                <p><strong>Apellido:</strong> ${data.apellido}</p>
                <p><strong>Cédula:</strong> ${data.cedula}</p>
                <p><strong>Teléfono:</strong> ${data.telefono}</p>
                <p><strong>Estado:</strong> ${data.activo ? "Activo" : "Inactivo"}</p>
            `;
            // Mostrar el modal
            modal.classList.remove("hidden");
        })
        .catch(error => {
            console.error("Error al obtener la información del docente:", error);
        });
}

// Cerrar el modal
function cerrarModal() {
    const modal = document.getElementById("modalDocente");
    modal.classList.add("hidden");
}

// Implementación de la barra de búsqueda dinámica en el servidor (AJAX)
const searchInput = document.getElementById('searchInput');
const tableBody = document.querySelector('#docentesTable tbody');

if (searchInput) {
    searchInput.addEventListener('input', () => {
        const searchTerm = searchInput.value.trim();

        if (searchTerm.length > 0) {
            fetch(`/docentes/buscar/?q=${encodeURIComponent(searchTerm)}`)
                .then(response => response.json())
                .then(data => {
                    tableBody.innerHTML = ''; // Limpiar la tabla
                    if (data.results.length > 0) {
                        data.results.forEach(docente => {
                            const row = `
                                <tr>
                                    <td><input type="checkbox" class="docenteCheckbox" value="${docente.id}"></td>
                                    <td>${docente.id}</td>
                                    <td class="nombre-docente">${docente.nombre}</td>
                                    <td class="apellido-docente">${docente.apellido}</td>
                                    <td class="cedula-docente">${docente.cedula}</td>
                                    <td>${docente.activo ? 'Activo' : 'Inactivo'}</td>
                                    <td>
                                        <a href="/docentes/detalle/${docente.id}" class="btn btn-view" title="Ver">
                                            <i class="bx bx-show"></i>
                                        </a>
                                        <a href="/docentes/editar/${docente.id}" class="btn btn-edit" title="Editar">
                                            <i class="bx bx-edit"></i>
                                        </a>
                                        <button class="btn btn-delete" onclick="confirmarEliminacion(${docente.id})" title="Eliminar">
                                            <i class="bx bx-trash"></i>
                                        </button>
                                    </td>
                                </tr>
                            `;
                            tableBody.insertAdjacentHTML('beforeend', row);
                        });
                    } else {
                        tableBody.innerHTML = '<tr><td colspan="7" class="text-center">No se encontraron resultados</td></tr>';
                    }
                    // Reasignar eventos a los nuevos checkboxes si es necesario
                })
                .catch(error => {
                    console.error('Error al buscar:', error);
                });
        } else {
            location.reload(); // Recargar la página si el término está vacío
        }
    });
}