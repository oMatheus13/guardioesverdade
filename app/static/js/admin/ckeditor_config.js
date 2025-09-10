// Adaptador customizado para upload de imagens via API
class CustomUploadAdapter {
    constructor(loader) {
        this.loader = loader;
    }

    upload() {
        return this.loader.file.then(file => new Promise((resolve, reject) => {
            const data = new FormData();
            data.append('upload', file);

            fetch('/api/upload-image-ckeditor', {
                method: 'POST',
                body: data
            })
            .then(response => response.json())
            .then(result => {
                if (result.url) {
                    resolve({ default: result.url });
                } else {
                    reject(result.error || 'Erro ao fazer upload da imagem.');
                }
            })
            .catch(error => {
                reject('Erro de conexão ou no servidor durante o upload.');
            });
        }));
    }

    abort() {
        // Lógica de abortar upload (opcional)
    }
}

// Função que adiciona o adaptador customizado ao editor
function CustomUploadAdapterPlugin(editor) {
    editor.plugins.get('FileRepository').createUploadAdapter = (loader) => {
        return new CustomUploadAdapter(loader);
    };
}

// Função para inicializar o CKEditor em um elemento específico
function initializeCKEditor(elementSelector) {
    ClassicEditor
        .create(document.querySelector(elementSelector), {
            extraPlugins: [CustomUploadAdapterPlugin],
            // Outras configurações do CKEditor aqui (ex: toolbar, etc)
        })
        .catch(error => {
            console.error(`Erro ao inicializar o CKEditor em ${elementSelector}:`, error);
        });
}
