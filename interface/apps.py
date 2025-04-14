# interface/apps.py

from django.apps import AppConfig
# --- Adicione estas importações ---
import os
import shutil
import sys
from django.conf import settings
# ----------------------------------

class InterfaceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'interface'

    # --- Adicione este método ---
    def ready(self):
        # Lógica para limpar a pasta de mídia

        # Verifica se estamos rodando o comando 'runserver' E se DEBUG é True
        is_runserver = any(arg == 'runserver' for arg in sys.argv)

        if is_runserver and settings.DEBUG:
            media_root = settings.MEDIA_ROOT
            print(f"--- Verificando limpeza do diretório de mídia: {media_root} ---")

            # Verifica se o diretório MEDIA_ROOT realmente existe
            if os.path.isdir(media_root):
                print(f"--- Iniciando limpeza de {media_root} (DEBUG=True, runserver) ---")
                # Itera sobre todos os arquivos e subdiretórios dentro de MEDIA_ROOT
                for filename in os.listdir(media_root):
                    file_path = os.path.join(media_root, filename)
                    try:
                        # Ignora arquivos/pastas ocultos (ex: .gitkeep se você usar)
                        if filename.startswith('.'):
                            print(f"   Ignorando: {filename}")
                            continue

                        # Se for um arquivo ou link, remove
                        if os.path.isfile(file_path) or os.path.islink(file_path):
                            os.unlink(file_path)
                            print(f"   Removido arquivo: {filename}")
                        # Se for um diretório, remove recursivamente
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                            print(f"   Removido diretório: {filename}")
                    except Exception as e:
                        # Informa se houver erro ao tentar remover algo
                        print(f'   ERRO ao remover {file_path}. Razão: {e}')
                print(f"--- Limpeza de {media_root} concluída ---")
            else:
                # Informa caso a pasta não exista
                print(f"--- Diretório de mídia {media_root} não encontrado. Pulando limpeza. ---")
        # else:
            # print("--- Limpeza de mídia não executada (Não é runserver ou DEBUG=False) ---")
    # --- Fim do método ready ---