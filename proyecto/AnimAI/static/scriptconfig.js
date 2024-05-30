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
    cambiarEstiloBotonesConfig(newMode);
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

// Cambiar el texto de la imagen al hacer clic en el botón de cambio de modo
toggleModeBtn.addEventListener("click", function () {
    const imagenTitulo = document.getElementById("imagenTitulo");
    const imagenModo = document.getElementById("imagenModo");

    if (imagenTitulo.textContent === "DEMOSTRACION DEL MODO OSCURO") {
        imagenTitulo.textContent = "DEMOSTRACION DEL MODO CLARO";
        imagenModo.src = "./static/mode_claro.png";
    } else {
        imagenTitulo.textContent = "DEMOSTRACION DEL MODO OSCURO";
        imagenModo.src = "./static/mode_oscuro.png";
    }
});


// Función para cambiar los estilos de los botones según el modo en ambas páginas
function cambiarEstiloBotonesConfig() {
    const irAInicioBtn = document.getElementById("irAInicioBtn");
    const toggleModeBtn = document.getElementById("toggleModeBtn");
    const historialBtn = document.getElementById("historialBtn");
    const savedMode = localStorage.getItem("mode");

    if (savedMode === "dark-mode") {
        // Si el modo guardado es oscuro, aplica la clase 'btn-dark' a los botones
        irAInicioBtn.classList.remove("btn-light");
        irAInicioBtn.classList.add("btn-dark");
        toggleModeBtn.classList.remove("btn-light");
        toggleModeBtn.classList.add("btn-dark");
        historialBtn.classList.remove("btn-light");
        historialBtn.classList.add("btn-dark");
    } else {
        // Si el modo guardado es claro o no está definido, aplica la clase 'btn-light' a los botones
        irAInicioBtn.classList.remove("btn-dark");
        irAInicioBtn.classList.add("btn-light");
        toggleModeBtn.classList.remove("btn-dark");
        toggleModeBtn.classList.add("btn-light");
        historialBtn.classList.remove("btn-dark");
        historialBtn.classList.add("btn-light");
    }
}

// Llamar a cambiarEstiloBotones al cargar la página
window.addEventListener("load", cambiarEstiloBotonesConfig);
