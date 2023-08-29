from django.shortcuts import render
from django.http import JsonResponse
import os


def index(request):
    if request.method == 'POST':
        chunk = request.FILES.get('chunk')
        total_chunks = int(request.POST.get('total_chunks'))
        chunk_number = int(request.POST.get('chunk_number'))
        file_name = request.POST.get('file-name')

        # local temporário no diretório da view
        view_dir = os.path.dirname(os.path.abspath(__file__))
        temp_file_path = os.path.join(view_dir+'/chunk_temp/', f'chunk_{chunk_number}.tmp')
        
        print('Chunnnk>>>>>>>>', file_name)
        with open(temp_file_path, 'wb') as temp_file:
            temp_file.write(chunk.read())

        if chunk_number == total_chunks - 1:
            final_file_path = os.path.join(view_dir+'/final_files/', file_name)
            with open(final_file_path, 'wb') as final_file:
                for i in range(total_chunks):
                    chunk_path = os.path.join(view_dir+'/chunk_temp/', f'chunk_{i}.tmp')
                    
                    # Escreve a proxima parte do arquivo no mesmo anterior 
                    with open(chunk_path, 'rb') as chunk_file:
                        final_file.write(chunk_file.read())

                    os.remove(chunk_path)  # Remover os chunks temporários

            return JsonResponse({'message': 'Upload concluído com sucesso.'})

        return JsonResponse({'message': 'Chunk recebido com sucesso.'})

    return render(request, 'index.html')
