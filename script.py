import os
import sys
import subprocess
import urllib.request

def process_file(url, audio_bit, vid_quality, output_name):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    req = urllib.request.Request(url, headers=headers)
    input_file =  f"{output_name}.in"
    output_dir = "out"
    
    os.makedirs(output_dir, exist_ok=True)
    # Pobierz rozmiar pliku
    with urllib.request.urlopen(req) as response:
        total_size = int(response.getheader('Content-Length').strip())
        bytes_downloaded = 0
        chunk_size = 1024  # Rozmiar fragmentu
        last_percent_reported = 0  # Do śledzenia ostatniego pokazanego procentu

        # Otwórz plik do zapisu
        with open(input_file, 'wb') as f:
            while True:
                # Odczytaj fragmenty danych
                chunk = response.read(chunk_size)
                if not chunk:
                    break
                f.write(chunk)
                bytes_downloaded += len(chunk)
                
                # Oblicz aktualny procent pobranego pliku
                percent_downloaded = bytes_downloaded / total_size * 100

                # Wyświetl postęp tylko co 5% lub po pobraniu co najmniej 3 MB
                if int(percent_downloaded) >= last_percent_reported + 5 or bytes_downloaded - (last_percent_reported / 100 * total_size) >= 3 * 1024 * 1024:
                    last_percent_reported = int(percent_downloaded)
                    print(f"Pobrano: {bytes_downloaded} / {total_size} bajtów ({percent_downloaded:.2f}%)", flush=True)
                    
    print(f"\nPobrano plik: {input_file}", flush=True)
        
    # Wyciągnij nazwę pliku bez rozszerzenia
    file_name_without_ext = os.path.splitext(os.path.basename(input_file))[0]
    output_file = os.path.join(output_dir, f"{file_name_without_ext}.mp4")  # Wynikowy plik w formacie .mp4

    # Wykonaj konwersję wideo za pomocą ffmpeg
    print(f"Processing {input_file}...", flush=True)
    subprocess.run(['ffmpeg', '-i', input_file, '-c:v', 'libx265', '-tag:v', 'hvc1', 
                '-preset', 'veryslow', '-crf', vid_quality, 
                '-c:a', 'aac', '-b:a', audio_bit, 
                output_file])
    
    print(f"Processed file saved as: {output_file}", flush=True)
    return output_file  # Zwróć ścieżkę do pliku wyjściowego

# Pobieranie danych wejściowych z linii poleceń
if __name__ == "__main__":
    d_url = sys.argv[1]  # URL podany przez użytkownika
    a_bit = sys.argv[2]  # Bitrate audio podany przez użytkownika
    vid_q = sys.argv[3]  # Jakość wideo podana przez użytkownika
    out_n = sys.argv[4]  # Nazwa pliku wyjściowego

    # Uruchom przetwarzanie pliku
    process_file(d_url, a_bit, vid_q, out_n)