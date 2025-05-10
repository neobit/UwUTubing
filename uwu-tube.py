import yt_dlp
import os
import platform
import sys
import concurrent.futures
import subprocess
import urllib.request
import zipfile

FFMPEG_DOWNLOAD_URL = 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip'

def clear_terminal():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def get_video_title(url):
    ydl_opts = {'quiet': True, 'no_warnings': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info.get('title', 'Unknown title')

def download_raw_audio(url, folder, format_choice):
    filename = ''
    ydl_opts = {
        'outtmpl': f'{folder}/%(title)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        'format': 'bestaudio/best' if format_choice == 'mp3' else 'bestvideo+bestaudio/mp4'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url)
        filename = ydl.prepare_filename(info)
        print(f"✅ Download concluído: {os.path.basename(filename)}")
    return filename

def convert_file(input_file, format_choice, ffmpeg_path):
    output_file = os.path.splitext(input_file)[0] + f'.{format_choice}'
    cmd = []
    if format_choice == 'mp3':
        cmd = [ffmpeg_path, '-y', '-i', input_file, '-vn', '-ab', '192k', '-ar', '44100', '-hide_banner', output_file]
    elif format_choice == 'mp4':
        cmd = [ffmpeg_path, '-y', '-i', input_file, '-c:v', 'libx264', '-c:a', 'aac', '-hide_banner', output_file]
    try:
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        os.remove(input_file)
        print(f"🎵 Conversão concluída: {os.path.basename(output_file)}")
    except Exception as e:
        print(f"❌ Erro ao converter {input_file}: {e}")

def download_and_extract_ffmpeg(bin_folder):
    print('⬇️ Baixando ffmpeg.zip...')
    zip_path = os.path.join(bin_folder, 'ffmpeg.zip')
    urllib.request.urlretrieve(FFMPEG_DOWNLOAD_URL, zip_path)
    print('📦 Extraindo ffmpeg...')
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(bin_folder)
    os.remove(zip_path)
    # Encontrar o caminho do ffmpeg.exe extraído
    for root, dirs, files in os.walk(bin_folder):
        if 'ffmpeg.exe' in files:
            extracted_path = os.path.join(root, 'ffmpeg.exe')
            final_path = os.path.join(bin_folder, 'ffmpeg.exe')
            os.rename(extracted_path, final_path)
            break
    print('✅ ffmpeg pronto!')

def find_ffmpeg():
    exe_dir = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__)
    bin_folder = os.path.join(exe_dir, 'bin')
    ffmpeg_path = os.path.join(bin_folder, 'ffmpeg.exe')
    if not os.path.isdir(bin_folder):
        os.makedirs(bin_folder, exist_ok=True)
    if not os.path.isfile(ffmpeg_path):
        download_and_extract_ffmpeg(bin_folder)
    return ffmpeg_path

def main():
    links = []
    titles = []
    ffmpeg_path = find_ffmpeg()

    print('Cole o link e aperte enter para incluir na lista, ou digite "done" e aperte enter para continuar.')
    
    while True:
        user_input = input('> ').strip()
        if user_input.lower() == 'done':
            break
        if not user_input:
            print('⚠️ Entrada vazia! Cole um link válido.')
            continue
        if user_input in links:
            print('⚠️ Link duplicado detectado! Ele já está na lista.')
            continue
        try:
            title = get_video_title(user_input)
            if not title or title == 'Unknown title':
                raise ValueError('Link inválido ou não encontrado.')
            links.append(user_input)
            titles.append(title)
            clear_terminal()
            print('Links adicionados:')
            for idx, t in enumerate(titles, 1):
                print(f'[{idx}] {t}')
            print('\nCole o próximo link ou digite "done" para continuar.')
        except Exception as e:
            print(f'⚠️ Erro ao processar o link: {e}')
    
    if not links:
        print('Nenhum link foi adicionado. Encerrando.')
        return

    format_choice = ''
    while format_choice not in ['mp3', 'mp4']:
        format_choice = input('Escolha o formato (mp3/mp4): ').strip().lower()
    
    folder = format_choice
    os.makedirs(folder, exist_ok=True)

    print(f'\n🎬 Baixando e convertendo {len(links)} vídeos...\n')

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as download_executor, \
         concurrent.futures.ThreadPoolExecutor(max_workers=3) as convert_executor:
        future_to_url = {download_executor.submit(download_raw_audio, url, folder, format_choice): url for url in links}
        
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                input_file = future.result()
                convert_executor.submit(convert_file, input_file, format_choice, ffmpeg_path)
            except Exception as e:
                print(f'❌ Erro no download de {url}: {e}')

    print('\n🎉 Todos os downloads e conversões foram finalizados! Os arquivos estão na pasta ./{}/'.format(folder))

if __name__ == '__main__':
    main()
