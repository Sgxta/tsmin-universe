document.addEventListener("DOMContentLoaded", () => {
    const menuBtn = document.getElementById("menuBtn");
    const navLinks = document.getElementById("navLinks");

    if (menuBtn && navLinks) {
        menuBtn.addEventListener("click", () => {
            navLinks.classList.toggle("show");
        });
    }

    const reservaPanel = document.querySelector("[data-reserva-panel]");

    if (reservaPanel) {
        const precio = parseFloat(reservaPanel.dataset.precio || "0");
        const inputs = reservaPanel.querySelectorAll(".seat input");
        const cantidadAsientos = document.getElementById("cantidadAsientos");
        const totalReserva = document.getElementById("totalReserva");

        function actualizarResumen() {
            let seleccionados = 0;

            inputs.forEach((input) => {
                const label = input.closest(".seat");

                if (input.checked) {
                    seleccionados++;
                    label.classList.add("selected");
                } else {
                    label.classList.remove("selected");
                }
            });

            const total = seleccionados * precio;

            if (cantidadAsientos) {
                cantidadAsientos.textContent = seleccionados;
            }

            if (totalReserva) {
                totalReserva.textContent = `$${total.toFixed(2)}`;
            }
        }

        inputs.forEach((input) => {
            input.addEventListener("change", actualizarResumen);
        });

        actualizarResumen();
    }
});