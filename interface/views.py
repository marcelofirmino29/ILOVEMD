import os
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .forms import UploadPDFForm
# Importações da biblioteca docling e outras necessárias
from docling.document_converter import DocumentConverter
from django.conf import settings # Importar settings
from urllib.parse import urljoin # Para juntar URLs de forma segura

# ... (Restante das importações e código da view) ...

def home(request):
    result = None
    form = UploadPDFForm()
    # Inicializa variáveis de contexto fora do POST para garantir que existam
    context = {'form': form, 'result': None, 'markdown_content': None,
               'error_message': None, 'uploaded_filename': None,
               'md_filename': None, 'md_url': None} # Adiciona md_url

    if request.method == 'POST':
        print("\nDEBUG: Recebido request POST.")
        form = UploadPDFForm(request.POST, request.FILES)
        if form.is_valid():
            print("DEBUG: Formulário é VÁLIDO.")
            pdf = form.cleaned_data['pdf_file']
            fs = FileSystemStorage()
            filename = fs.save(pdf.name, pdf) # Nome do PDF salvo
            file_path = fs.path(filename)
            print(f"DEBUG: PDF salvo em: {file_path}")

            # Reseta variáveis para esta tentativa de conversão
            markdown_content = None
            error_message = None
            md_filename = None
            md_url = None # Reseta md_url

            if DocumentConverter:
                try:
                    print(f"DEBUG: TENTANDO criar DocumentConverter")
                    converter = DocumentConverter()
                    print(f"DEBUG: TENTANDO chamar .convert() com '{file_path}'")
                    conversion_result = converter.convert(file_path)
                    print("DEBUG: TENTANDO chamar .export_to_markdown()")
                    markdown_content = conversion_result.document.export_to_markdown()
                    result = markdown_content
                    print("DEBUG: .export_to_markdown() chamado SUCESSO.")

                    # --- Bloco para salvar MD e GERAR URL ---
                    if markdown_content is not None:
                        md_basename = os.path.splitext(filename)[0] + ".md"
                        md_path = os.path.join(fs.location, md_basename) # fs.location é MEDIA_ROOT
                        try:
                            with open(md_path, "w", encoding="utf-8") as f:
                                 f.write(markdown_content)
                            md_filename = md_basename # Guarda o nome base do arquivo MD
                            print(f"DEBUG: Arquivo MD salvo em: {md_path}")

                            # ----> GERAR A URL DE DOWNLOAD <----
                            # Garante que MEDIA_URL termina com /
                            media_url_with_slash = settings.MEDIA_URL if settings.MEDIA_URL.endswith('/') else settings.MEDIA_URL + '/'
                            # Junta a MEDIA_URL com o nome do arquivo MD
                            md_url = urljoin(media_url_with_slash, md_filename)
                            print(f"DEBUG: URL para download do MD: {md_url}")
                            # ------------------------------------

                        except Exception as e_save:
                            error_message = f"Erro ao salvar o arquivo Markdown: {e_save}"
                            if result is None: result = error_message
                            print(f"DEBUG: ERRO ao salvar MD: {e_save}")
                    # --- Fim do bloco ---

                except Exception as e:
                    # ... (bloco de erro da conversão igual) ...
                    error_message = f"Erro durante a conversão com docling: {e}"
                    result = error_message
                    print(f"DEBUG: ERRO ao usar docling: {e}")
                    import traceback
                    print(traceback.format_exc())
            else:
                 # ... (bloco de erro da importação igual) ...
                 error_message = "Erro: Classe 'DocumentConverter' de docling não está disponível."
                 result = error_message
                 print("DEBUG: Pulei a conversão porque a importação falhou.")

            # Opcional: Remover PDF original

            # Atualiza o dicionário de contexto com os resultados
            context.update({
                'form': form, 'result': result, 'markdown_content': markdown_content,
                'error_message': error_message, 'uploaded_filename': filename,
                'md_filename': md_filename, 'md_url': md_url # Passa a URL para o template!
            })
            return render(request, 'interface/home.html', context)
        else:
            # Se o form for inválido, atualiza o form no contexto para mostrar os erros
            context['form'] = form
            print("DEBUG: Formulário é INVÁLIDO.")
            print("DEBUG: Erros do formulário:", form.errors.as_json())

    # Renderiza para GET ou se o form POST for inválido
    return render(request, 'interface/home.html', context)