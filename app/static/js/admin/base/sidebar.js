// static/js/admin/base/sidebar.js
document.addEventListener('DOMContentLoaded', function() {
    const body = document.body;
    const sidebar = document.getElementById('admin-sidebar');

    document.querySelectorAll('[data-behavior]').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const behavior = this.getAttribute('data-behavior');
            
            // Limpa todos os estados de comportamento do body
            body.classList.remove('sidebar-expanded', 'sidebar-collapsed', 'sidebar-hoverable');

            // Adiciona apenas o estado atual
            if (behavior === 'expanded') {
                body.classList.add('sidebar-expanded');
            } else if (behavior === 'collapsed') {
                body.classList.add('sidebar-collapsed');
            } else { // 'hover' é o padrão
                body.classList.add('sidebar-hoverable');
            }
        });
    });

    // Define o comportamento padrão ao carregar a página
    document.querySelector('[data-behavior="hover"]').click();
});