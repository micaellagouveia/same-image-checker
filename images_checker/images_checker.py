import os
import shutil
import filecmp
import requests
import mmap
import hashlib

from requests.exceptions import RequestException
from PIL import Image

class CompareImageError(Exception):
    pass

class CalculateImageHashException(Exception):
    pass


def sha256sum(filename):
    h  = hashlib.sha256()
    with open(filename, 'rb') as f:
        with mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ) as mm:
            h.update(mm)
    return h.hexdigest()

def download_image_from_url(link: str, filename: str) -> Image:

    # filename = link.split('/')[-1]

    # Nome único
    # unique_filename = '/tmp/' + uuid.uuid4().hex[:7] + '-' + filename
    unique_filename = filename

    with requests.get(link, stream=True) as req:
        with open(unique_filename, 'wb') as file:
            shutil.copyfileobj(req.raw, file)

    return unique_filename

def is_same_image(link_1: str, link_2: str) -> bool:
    try:
        import threading
        threads = []

        file_1 = '/tmp/file_1'
        file_2 = '/tmp/file_2'

        for link, filename in [(link_1, file_1), (link_2, file_2)]:
            thread = threading.Thread(
                target=download_image_from_url, 
                args=(link, filename)
            )
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

    except RequestException as exc:
        raise CompareImageError("Falha na requisição da url")
    except OSError as exc:
        raise CompareImageError("Falha no download do arquivo da imagem")

    try:
        result = filecmp.cmp(file_1, file_2)

    except FileNotFoundError as exc:
        raise CompareImageError("Falha na comparação dos arquivos das imagens")

    return result


def calculate_image_hash(url: str, file_name: str) -> str:
    try:
        download_image_from_url(url, file_name)
    except RequestException as exc:
        raise CalculateImageHashException("Falha na requisição da url")
    
    return sha256sum(file_name)


def delete_image(path: str):
    try:
        os.remove(path)
    except FileNotFoundError as exc:
        return False
    return True

if __name__ == '__main__':

    link_1 = 'https://www.collinsdictionary.com/images/full/dog_230497594.jpg'
    link_2 = 'https://www.collinsdictionary.com/images/full/dog_230497594.jpg'
    # link_2 = 'https://www.specialdog.com.br/assets/imgs/cao.png'

    if is_same_image(link_1, link_2):
        print("Mesma imagem")
    
    else:
        print("Imagens diferentes")
