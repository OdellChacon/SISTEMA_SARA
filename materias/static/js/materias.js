document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".btn-delete").forEach(button => {
        button.addEventListener("click", () => {
            const materiaId = button.getAttribute("data-id");
            Swal.fire({
                title: "¿Estás seguro?",
                text: "Esta acción no se puede deshacer.",
                icon: "warning",
                showCancelButton: true,
                confirmButtonColor: "#d33",
                cancelButtonColor: "#3085d6",
                confirmButtonText: "Sí, eliminar",
                cancelButtonText: "Cancelar",
            }).then(result => {
                if (result.isConfirmed) {
                    fetch(`/materias/eliminar/${materiaId}/`, {
                        method: "POST",
                        headers: {
                            "X-CSRFToken": getCSRFToken(),
                        },
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            Swal.fire("¡Eliminado!", "La materia ha sido eliminada.", "success")
                                .then(() => location.reload());
                        } else {
                            Swal.fire("Error", "No se pudo eliminar la materia.", "error");
                        }
                    });
                }
            });
        });
    });
});

function getCSRFToken() {
    return document.querySelector("[name=csrfmiddlewaretoken]").value;
}
