from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

def g1_news(request):
    noticias_list = []

    # Faça uma solicitação inicial para a página do G1
    response = requests.get('https://g1.globo.com/')
    content = response.content
    site = BeautifulSoup(content, 'html.parser')

    # Encontre e extraia as notícias da página inicial
    noticias = site.find_all('div', class_='feed-post-body')
    for noticia in noticias:
        titulo = noticia.find('a', class_='feed-post-link')
        if titulo:
            titulo_text = titulo.get_text()
            link = titulo.get('href')
            
            # Encontre a tag <picture>
            picture = noticia.find('picture', class_='bstn-fd-cover-picture')
            
            # Se a tag <picture> for encontrada, encontre o elemento <img> dentro dela
            if picture:
                img = picture.find('img', class_='bstn-fd-picture-image')
                if img:
                    imagem_url = img['src']
                else:
                    imagem_url = None
            else:
                imagem_url = None

            noticias_list.append({
                'titulo': titulo_text,
                'link': link,
                'imagem_url': imagem_url  # Adicione a URL da imagem
            })

    # Observe a URL da próxima página de notícias (se houver)
    next_page_url = site.find('a', class_='load-more-link')
    while next_page_url:
        # Faça uma solicitação para a próxima página
        next_page_response = requests.get(next_page_url['href'])
        next_page_content = next_page_response.content
        next_page_site = BeautifulSoup(next_page_content, 'html.parser')

        # Encontre e extraia as notícias da próxima página
        noticias = next_page_site.find_all('div', class_='feed-post-body')
        for noticia in noticias:
            titulo = noticia.find('a', class_='feed-post-link')
            if titulo:
                titulo_text = titulo.get_text()
                link = titulo.get('href')
                
                # Encontre a tag <picture>
                picture = noticia.find('picture', class_='bstn-fd-cover-picture')
                
                # Se a tag <picture> for encontrada, encontre o elemento <img> dentro dela
                if picture:
                    img = picture.find('img', class_='bstn-fd-picture-image')
                    if img:
                        imagem_url = img['src']
                    else:
                        imagem_url = None
                else:
                    imagem_url = None

                noticias_list.append({
                    'titulo': titulo_text,
                    'link': link,
                    'imagem_url': imagem_url  # Adicione a URL da imagem
                })

        # Observe a URL da próxima página de notícias (se houver)
        next_page_url = next_page_site.find('a', class_='load-more-link')

    # Renderize um modelo com todas as notícias
    return render(request, 'noticiasapp/index.html', {'noticias': noticias_list})
