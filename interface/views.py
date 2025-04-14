# interface/views.py
import os
import shutil # Se usar para limpar imagens depois
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .forms import UploadPDFForm
try:
    from docling.document_converter import DocumentConverter
except ImportError:
    DocumentConverter = None
from django.conf import settings
from urllib.parse import urljoin
import traceback

def home(request):
    form = UploadPDFForm()
    # Contexto inicial para GET
    context = {'form': form, 'results_list': None}

    if request.method == 'POST':
        form = UploadPDFForm(request.POST, request.FILES)
        # Lista para armazenar os resultados de cada arquivo processado
        results_data = []

        if form.is_valid():
            uploaded_files = request.FILES.getlist('pdf_file') # Pega a LISTA de arquivos
            fs = FileSystemStorage()
            # Garante que a URL de mídia termina com / (para urljoin)
            media_url_with_slash = settings.MEDIA_URL if settings.MEDIA_URL.endswith('/') else settings.MEDIA_URL + '/'

            # Processa cada arquivo enviado no loop
            for pdf_file in uploaded_files:
                # Dicionário para guardar o resultado deste arquivo específico
                file_result = {
                    'original_name': pdf_file.name,
                    'saved_pdf_name': None,
                    'md_filename': None,
                    'md_url': None,
                    'markdown_content_preview': None, # Para mostrar prévia no HTML
                    'error_message': None
                }

                filename = None # Nome do PDF salvo no servidor
                file_path = None # Caminho do PDF salvo

                try:
                    # Salva o PDF atual
                    filename = fs.save(pdf_file.name, pdf_file)
                    file_path = fs.path(filename)
                    file_result['saved_pdf_name'] = filename
                    print(f"DEBUG: Processando PDF salvo em: {file_path}")

                    if DocumentConverter:
                        # --- Lógica de conversão (incluindo preparação hipotética de imagens) ---
                        pdf_basename = os.path.splitext(filename)[0]
                        image_save_subdir = f"images_{pdf_basename}"
                        image_save_path = os.path.join(settings.MEDIA_ROOT, image_save_subdir)
                        os.makedirs(image_save_path, exist_ok=True)
                        image_serve_url = urljoin(media_url_with_slash, image_save_subdir + '/')
                        # ----------------------------------------------------------------------

                        print(f"DEBUG: TENTANDO converter {filename}")
                        converter = DocumentConverter()
                        conversion_result = converter.convert(file_path)
                        print(f"DEBUG: TENTANDO exportar {filename} para markdown...")

                        # --- Substitua pelos argumentos REAIS do docling para imagens ---
                        markdown_content_full = conversion_result.document.export_to_markdown(
                            # image_dir=image_save_path,
                            # image_url_prefix=image_serve_url
                        )
                        # ---------------------------------------------------------------
                        print(f"DEBUG: Exportação de {filename} SUCESSO.")

                        if markdown_content_full is not None:
                            # Guarda uma prévia (ex: primeiros 500 caracteres)
                            file_result['markdown_content_preview'] = (markdown_content_full[:500] + '...') if len(markdown_content_full) > 500 else markdown_content_full

                            # Salva o arquivo .md
                            md_basename = os.path.splitext(filename)[0] + ".md"
                            md_path = os.path.join(settings.MEDIA_ROOT, md_basename)
                            try:
                                with open(md_path, "w", encoding="utf-8") as f:
                                    f.write(markdown_content_full) # Salva conteúdo completo
                                file_result['md_filename'] = md_basename
                                file_result['md_url'] = urljoin(media_url_with_slash, md_basename) # Gera URL para download
                                print(f"DEBUG: Arquivo MD salvo: {md_path}")
                                print(f"DEBUG: URL download MD: {file_result['md_url']}")
                            except Exception as e_save:
                                file_result['error_message'] = f"Erro ao salvar {md_basename}: {e_save}"
                                print(f"DEBUG: ERRO ao salvar MD: {e_save}")
                        else:
                            file_result['error_message'] = "Conversão retornou conteúdo vazio."
                    else:
                         file_result['error_message'] = "Erro: Biblioteca 'docling' não está disponível."

                except Exception as e:
                    file_result['error_message'] = f"Erro geral ao processar: {e}"
                    print(f"DEBUG: ERRO ao processar {pdf_file.name}: {e}")
                    print(traceback.format_exc())

                # Adiciona o dicionário de resultado deste arquivo à lista geral
                results_data.append(file_result)

                # Limpeza opcional do PDF original ou pasta de imagens aqui, se desejado

            # --- Fim do loop ---

            # Passa a lista de resultados para o contexto do template
            context.update({
                'form': form,
                'results_list': results_data
            })
            print(f"DEBUG: Processamento de {len(uploaded_files)} arquivo(s) concluído. Renderizando template.")
            # Renderiza a mesma página, agora com a lista de resultados
            return render(request, 'interface/home.html', context)

        else: # Formulário inválido
            context['form'] = form # Passa o form com erros para exibição
            print("DEBUG: Formulário é INVÁLIDO.")
            print("DEBUG: Erros do formulário:", form.errors.as_json())

    # Renderiza para GET ou se o form POST for inválido (sem results_list)
    return render(request, 'interface/home.html', context)