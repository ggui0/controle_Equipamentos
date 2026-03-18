$(document).ready(function() {
    $('#tabelaEquipamentos').DataTable({
        pageLength: 25,
        scrollX: true,
        dom: 'Bfrtip',
        buttons: [
            { extend: 'excelHtml5', text: 'Excel' },
            { extend: 'pdfHtml5', text: 'PDF' },
            { extend: 'print', text: 'Imprimir' }
        ],
        language: {
            url: "https://cdn.datatables.net/plug-ins/1.13.6/i18n/pt-BR.json"
        }
    });
});