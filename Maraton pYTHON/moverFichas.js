$(document).ready(function() {
    const coloresFichas = ['red', 'blue', 'green', 'yellow']; // Colores para hasta 4 fichas
    const tablero = $('#tablero');

    // Agregar fichas al tablero
    coloresFichas.forEach((color, index) => {
        const fichaTemplate = $('#template-ficha').html()
            .replace('COLOR', color)
            .replace('ID', index);
        tablero.append(fichaTemplate);
    });

    // Habilitar movimiento de fichas
    $('.ficha').on('dragstart', function(event) {
        event.originalEvent.dataTransfer.setData("text/plain", event.target.id);
    });

    $('#tablero').on('dragover', function(event) {
        event.preventDefault(); // Permitir soltar la ficha
    });

    $('#tablero').on('drop', function(event) {
        event.preventDefault();
        const idFicha = event.originalEvent.dataTransfer.getData("text/plain");
        const ficha = $('#' + idFicha);
        const tableroOffset = $(this).offset();
        // Mover la ficha al lugar donde se soltó
        ficha.css('left', event.originalEvent.pageX - tableroOffset.left - ficha.width() / 2 + 'px');
        ficha.css('top', event.originalEvent.pageY - tableroOffset.top - ficha.height() / 2 + 'px');
    });
});
