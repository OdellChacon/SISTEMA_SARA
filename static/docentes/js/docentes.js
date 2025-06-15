document.addEventListener("DOMContentLoaded", function () {
    // Filtro en la búsqueda
    document.getElementById("searchInput").addEventListener("keyup", function () {
        let filter = this.value.toLowerCase();
        document.querySelectorAll("table tbody tr").forEach(row => {
            let name = row.cells[2].textContent.toLowerCase();
            row.style.display = name.includes(filter) ? "" : "none";
        });
    });

    // Seleccionar/Deseleccionar todos los checkboxes
    document.getElementById("selectAll").addEventListener("change", function () {
        document.querySelectorAll(".docenteCheckbox").forEach(checkbox => {
            checkbox.checked = this.checked;
        });
    });
});

// Animación de botones
document.addEventListener("DOMContentLoaded", function () {
    function animateButton(buttonId) {
        let button = document.getElementById(buttonId);
        button.addEventListener("click", function () {
            let icon = button.querySelector(".icon");

            // Animación de rebote del botón
            gsap.fromTo(button, { scale: 1 }, { scale: 1.1, duration: 0.2, yoyo: true, repeat: 1 });

            // Animación de giro del icono
            gsap.to(icon, { rotation: 360, duration: 0.5, ease: "power2.out" });

            // Efecto de onda
            let ripple = document.createElement("span");
            ripple.classList.add("ripple");
            button.appendChild(ripple);
            gsap.fromTo(ripple, { scale: 0, opacity: 1 }, { scale: 2, opacity: 0, duration: 0.6, onComplete: () => ripple.remove() });
        });
    }

    animateButton("btnRegistrar");
    animateButton("btnImportar");
    animateButton("btnExportar");
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



/*ESTILOS FORMULARIOS DOCENTES*/
document.addEventListener("DOMContentLoaded", function () {
    function animateButton(buttonId) {
        let button = document.getElementById(buttonId);
        button.addEventListener("click", function () {
            let icon = button.querySelector("i");

            // Animación de rebote
            gsap.fromTo(button, { scale: 1 }, { scale: 1.1, duration: 0.2, yoyo: true, repeat: 1 });

            // Animación del icono
            gsap.to(icon, { rotation: 360, duration: 0.5, ease: "power2.out" });
        });
    }

    animateButton("btnRegistrar");
    animateButton("btnCancelar");
});


function confirmDelete(docenteId) {
    // Muestra el modal
    document.getElementById('deleteModal').classList.remove('hidden');
    
    // Acción de confirmación
    document.getElementById('confirmDeleteBtn').onclick = function() {
        window.location.href = `/eliminar_docente/${docenteId}/`;  // Enlace a la vista para eliminar el docente
    };
    
    // Acción de cancelación
    document.getElementById('cancelDeleteBtn').onclick = function() {
        document.getElementById('deleteModal').classList.add('hidden');
    };
}


document.addEventListener("DOMContentLoaded", function () {
    // Filtro en la búsqueda
    document.getElementById("searchInput").addEventListener("keyup", function () {
        let filter = this.value.toLowerCase();
        document.querySelectorAll("table tbody tr").forEach(row => {
            let name = row.cells[1].textContent.toLowerCase();
            row.style.display = name.includes(filter) ? "" : "none";
        });
    });

    // Seleccionar/Deseleccionar todos los checkboxes
    document.getElementById("selectAll").addEventListener("change", function () {
        document.querySelectorAll(".docenteCheckbox").forEach(checkbox => {
            checkbox.checked = this.checked;
        });
    });

    // Función de confirmación de eliminación
    window.confirmDelete = function (docenteId) {
        const confirmation = window.confirm("¿Estás seguro de eliminar este docente?");
        if (confirmation) {
            // Redirigir a la URL de eliminación
            window.location.href = `/eliminar_docente/${docenteId}/`;  // Acción para eliminar el docente
        }
    };
});


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
    } else {
        modalTitle.textContent = "Seleccione el formato de Exportación";
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

document.addEventListener("DOMContentLoaded", function () {
    // Inicializar DataTable con paginación y búsqueda
    const table = $('#docentesTable').DataTable({
        paging: true, // Habilitar paginación
        pageLength: 10, // Mostrar 10 registros por página
        lengthMenu: [10, 20, 30, 40, 50], // Opciones de registros por página
        scrollX: true, // Habilitar scrollbar horizontal
        language: {
            search: "Buscar:",
            lengthMenu: "Mostrar _MENU_ registros por página",
            zeroRecords: "No se encontraron registros",
            info: "Mostrando página _PAGE_ de _PAGES_",
            infoEmpty: "No hay registros disponibles",
            infoFiltered: "(filtrado de _MAX_ registros totales)",
            paginate: {
                first: "Primero",
                last: "Último",
                next: "Siguiente",
                previous: "Anterior"
            }
        }
    });

    // Filtrar automáticamente al escribir en la barra de búsqueda
    document.getElementById("searchInput").addEventListener("input", function () {
        table.search(this.value).draw();
    });

    // Seleccionar/Deseleccionar todos los checkboxes
    document.getElementById("selectAll").addEventListener("change", function () {
        const checkboxes = document.querySelectorAll(".docenteCheckbox");
        checkboxes.forEach(checkbox => {
            checkbox.checked = this.checked;
        });
        updateSelectedCount();
    });

    // Actualizar contador de seleccionados
    function updateSelectedCount() {
        const selected = document.querySelectorAll(".docenteCheckbox:checked").length;
        const selectedCount = document.getElementById("selectedCount");
        const selectedCountValue = document.getElementById("selectedCountValue");

        selectedCountValue.textContent = selected;
        selectedCount.style.display = selected > 0 ? "flex" : "none";
    }

    // Confirmar eliminación de seleccionados
    window.confirmDeleteSelected = function () {
        const selectedIds = Array.from(document.querySelectorAll(".docenteCheckbox:checked")).map(cb => cb.value);
        if (selectedIds.length === 0) {
            Swal.fire("Atención", "No hay registros seleccionados.", "warning");
            return;
        }

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
                    body: JSON.stringify({ ids: selectedIds })
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
    };

    // Función para obtener el CSRF Token
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