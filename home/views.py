from django.shortcuts import render
from django.http import JsonResponse
import tempfile
import os
from django.conf import settings


def index(request):
    if request.method == 'POST':
        chunk = request.FILES.get('chunk')
        total_chunks = int(request.POST.get('total_chunks'))
        chunk_number = int(request.POST.get('chunk_number'))

        # Salvar o chunk em um local temporário no diretório da view
        view_dir = os.path.dirname(os.path.abspath(__file__))
        temp_file_path = os.path.join(view_dir, f'chunk_{chunk_number}.tmp')

        with open(temp_file_path, 'wb') as temp_file:
            temp_file.write(chunk.read())

        if chunk_number == total_chunks - 1:
            # Todos os chunks foram enviados
            final_file_path = os.path.join(view_dir, 'final_file.mp4')
            with open(final_file_path, 'wb') as final_file:
                for i in range(total_chunks):
                    chunk_path = os.path.join(view_dir, f'chunk_{i}.tmp')

                    with open(chunk_path, 'rb') as chunk_file:
                        final_file.write(chunk_file.read())

                    os.remove(chunk_path)  # Remover os chunks temporários

            return JsonResponse({'message': 'Upload concluído com sucesso.'})

        return JsonResponse({'message': 'Chunk recebido com sucesso.'})

    return render(request, 'index.html')
