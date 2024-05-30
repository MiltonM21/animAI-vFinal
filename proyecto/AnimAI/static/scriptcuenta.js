const toggleModeBtn = document.getElementById("toggleModeBtn");

function applyMode(mode) {
    document.body.classList.remove("light-mode", "dark-mode");
    document.body.classList.add(mode);
}

function cambiarModo() {
    var body = document.body;
    if (body.classList.contains("dark-mode")) {
        body.classList.remove("dark-mode");
        body.classList.add("light-mode");
        localStorage.setItem("modo", "light");
    } else {
        body.classList.remove("light-mode");
        body.classList.add("dark-mode");
        localStorage.setItem("modo", "dark");
    }
}

function toggleMode() {
    const isDarkMode = document.body.classList.contains("dark-mode");
    const newMode = isDarkMode ? "light-mode" : "dark-mode";

    localStorage.setItem("mode", newMode);

    applyMode(newMode);

    // Cambiar la imagen del botón después de cambiar el modo
    if (newMode === "dark-mode") {
        document.getElementById("modoIcono").src = "./static/boton_sol.png"; // Ruta a la imagen de botón de modo oscuro
    } else {
        document.getElementById("modoIcono").src = "./static/boton_luna.png"; // Ruta a la imagen de botón de modo claro
    }

    // Cambiar el estilo de los botones según el modo
    cambiarEstiloBotonesCuenta(newMode);
}

toggleModeBtn.addEventListener("click", toggleMode);

// Recuperar el estado del modo al cargar la página
const savedMode = localStorage.getItem("mode");
if (savedMode) {
    applyMode(savedMode);

    // Actualizar la imagen del botón según el estado del modo
    if (savedMode === "dark-mode") {
        document.getElementById("modoIcono").src = "./static/boton_sol.png"; // Ruta a la imagen de botón de modo oscuro
    } else {
        document.getElementById("modoIcono").src = "./static/boton_luna.png"; // Ruta a la imagen de botón de modo claro
    }
}


// Función para cambiar los estilos de los botones según el modo en ambas páginas
function cambiarEstiloBotonesCuenta() {
    const irAConfiguracionesBtn = document.getElementById("irAConfiguracionesBtn");
    const cerrarSesionBtn = document.getElementById("cerrarSesionBtn");
    const toggleModeBtn = document.getElementById("toggleModeBtn");
    const savedMode = localStorage.getItem("mode");

    if (savedMode === "dark-mode") {
        // Si el modo guardado es oscuro, aplica la clase 'btn-dark' a los botones
        irAConfiguracionesBtn.classList.remove("btn-light");
        irAConfiguracionesBtn.classList.add("btn-dark");
        cerrarSesionBtn.classList.remove("btn-light");
        cerrarSesionBtn.classList.add("btn-dark");
        toggleModeBtn.classList.remove("btn-light");
        toggleModeBtn.classList.add("btn-dark");
    } else {
        // Si el modo guardado es claro o no está definido, aplica la clase 'btn-light' a los botones
        irAConfiguracionesBtn.classList.remove("btn-dark");
        irAConfiguracionesBtn.classList.add("btn-light");
        toggleModeBtn.classList.remove("btn-dark");
        toggleModeBtn.classList.add("btn-light");
    }
}

// Llamar a cambiarEstiloBotones al cargar la página
window.addEventListener("load", cambiarEstiloBotonesCuenta);


document.addEventListener("DOMContentLoaded", function() {
    const editarBtn = document.getElementById("editarBtn");
    const guardarBtn = document.getElementById("guardarBtn");
    const inputs = document.querySelectorAll("input");

    // Deshabilitar todos los campos de entrada del formulario, excepto la contraseña
    inputs.forEach(input => {
        if (input.id !== "password") {
            input.setAttribute("readonly", true);
        }
    });

    // Función para habilitar la edición del formulario
    editarBtn.addEventListener("click", function() {
        inputs.forEach(input => {
            input.removeAttribute("readonly");
        });
        editarBtn.style.display = "none";
        guardarBtn.style.display = "block";
    });

    // Función para deshabilitar la edición del formulario y guardar los cambios
    guardarBtn.addEventListener("click", function() {
        inputs.forEach(input => {
            input.setAttribute("readonly", true);
        });
        editarBtn.style.display = "block";
        guardarBtn.style.display = "none";
    });
});
