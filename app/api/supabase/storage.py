import time

from werkzeug.utils import secure_filename

from flask import current_app, flash
from supabase import Client
from typing import Optional


class SupabaseStorage:
    """
    Gerencia e interage com o armazenamento de arquivos no Supabase Storage.
    """

    def __init__(self, supabase_client: Client, bucket_name: str):
        self.client = supabase_client
        self.bucket_name = bucket_name
        self.public_url_prefix = f"{self.client.supabase_url}/storage/v1/object/public/{self.bucket_name}"

    
    def _generate_unique_filename(self, filename: str) -> str:
        """ Gera um nome de arquivo único usando timestamp para evitar colisões. """

        safe_filename = secure_filename(filename)
        return f"{int(time.time())}_{safe_filename}"


    def upload(self, file_storage) -> Optional[str]:
        """
        Faz o upload de um arquivo para o bucket do Supabase e retorna a url pública.

        :param file_storage: Objeto FileStorage do Flask (ex: form.imagem.data).
        :return: URL pública do arquivo ou None se falhar.
        """

        if not file_storage or not file_storage.filename:
            return None
        

        try:
            unique_filename = self._generate_unique_filename(file_storage.filename)
            file_bytes = file_storage.read()

            # Faz o upload do arquivo para o Supabase Storage
            self.client.storage.from_(self.bucket_name).upload(
                path=unique_filename,
                file=file_bytes,
                file_options={"content-type": file_storage.mimetype}
            )

            # Retorna a URL pública do arquivo
            return f"{self.public_url_prefix}/{unique_filename}"
        
        except Exception as e:
            flash(f"Erro ao fazer upload do arquivo: {e}", "danger")
            current_app.logger.error(f"Erro ao fazer upload do arquivo para o Supabase: {e}")
            return None

    
    def delete(self, file_url: Optional[str]) -> bool:
        """
        Exclui um arquivo do bucket do Supabase com base na sua URL pública.
        
        :param file_url: URL pública do arquivo a ser excluído.
        :return: True se a exclusão foi bem-sucedida, False caso contrário.
        """

        if not file_url:
            current_app.logger.warning("URL do arquivo não fornecida para exclusão.")
            return True  # Nada a excluir
        
        try:
            # Extrai o nome do arquivo da URL
            filename = file_url.split("/")[-1]

            self.client.storage.from_(self.bucket_name).remove([filename])
            return True
        
        except Exception as e:
            current_app.logger.error(f"Erro ao excluir arquivo do Supabase ({file_url}): {e}")
            return False
        
    
    def update(self, old_file_url: Optional[str], new_file_storage) -> Optional[str]:
        """
        Atualiza um arquivo: deleta o antigo (se existir) e faz o upload do novo.

        :param old_file_url: URL pública do arquivo antigo.
        :param new_file_storage: Objeto FileStorage do Flask para o novo arquivo.
        :return: URL pública do novo arquivo, a URL antiga se o novo upload falhar, ou None.
        """

        if new_file_storage and new_file_storage.filename:
            # Deleta o arquivo antigo primeiro
            if old_file_url:
                self.delete(old_file_url)

            return self.upload(new_file_storage)
        
        # Se nenhum arquivo foi enviado, mantém o antigo
        return old_file_url
    