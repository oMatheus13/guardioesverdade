// Script para ativação do modal
document.addEventListener('DOMContentLoaded', function () {
    var confirmDeleteModal = document.getElementById('confirmDeleteModal');
    confirmDeleteModal.addEventListener('show.bs.modal', function (event) {
        // Botão que acionou o modal
        var button = event.relatedTarget;
        // Extrai a URL de ação do atributo data-bs-action
        var actionUrl = button.getAttribute('data-bs-action');
        // Encontra o formulário dentro do modal
        var deleteForm = document.getElementById('deleteForm');
        // Extrai o tipo do item do atributo item-tipo
        var itemTipo = button.getAttribute('item-tipo');
        // Atualiza o texto do título do item no modal
        itemTipo = itemTipo.charAt(0).toUpperCase() + itemTipo.slice(1); // Capitaliza a primeira letra
        document.getElementById('itemTipo').textContent = itemTipo;
        // Extrai o nome do item do atributo item-nome
        var itemNome = button.getAttribute('item-nome');
        // Atualiza o texto do título do evento no modal
        document.getElementById('itemNome').textContent = `'${itemNome}'`;
        // Atualiza o atributo 'action' do formulário com a URL correta
        deleteForm.setAttribute('action', actionUrl);
    });
});