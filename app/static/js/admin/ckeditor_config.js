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

            language: 'pt-br',

            mediaEmbed: {
                previewsInData: true  // Mostra a pré-visualização do vídeo dentro do editor
            },

            heading: {
                options: [
                    { model: 'paragraph', title: 'Parágrafo', class: 'ck-heading_paragraph' },
                    { model: 'heading2', view: 'h2', title: 'Título 2', class: 'ck-heading_heading2' },
                    { model: 'heading3', view: 'h3', title: 'Título 3', class: 'ck-heading_heading3' },
                    { model: 'heading4', view: 'h4', title: 'Título 4', class: 'ck-heading_heading4' }
                ]
            },

            image: {
                toolbar: [
                    'imageTextAlternative',
                    'imageStyle:inline',
                    'imageStyle:block',
                    'imageStyle:side'
                ]
            }
            
        })
        .catch(error => {
            console.error(`Erro ao inicializar o CKEditor em ${elementSelector}:`, error);
        });
}
