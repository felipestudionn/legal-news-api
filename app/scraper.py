import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict, Any
import logging

# Configuración del logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NewsScraper:
    def __init__(self):
        # Headers para simular un navegador
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    async def get_elespanol_news(self) -> List[Dict[str, Any]]:
        """
        Obtiene noticias de El Español relacionadas con telecomunicaciones
        """
        try:
            url = 'https://www.elespanol.com/temas/telecomunicaciones/'
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')
            
            news_list = []
            articles = soup.find_all('article')
            
            for article in articles[:5]:
                try:
                    title_element = article.find('h2') or article.find('h3')
                    if not title_element:
                        continue
                        
                    title = title_element.text.strip()
                    link = title_element.find('a')['href']
                    if not link.startswith('http'):
                        link = 'https://www.elespanol.com' + link
                        
                    excerpt = ''
                    excerpt_element = article.find('p')
                    if excerpt_element:
                        excerpt = excerpt_element.text.strip()
                    
                    news_list.append({
                        'title': title,
                        'content': excerpt,
                        'url': link,
                        'source': 'El Español',
                        'category': 'Telecomunicaciones',
                        'date': datetime.now().strftime('%Y-%m-%d')
                    })
                except Exception as e:
                    logger.error(f'Error procesando artículo de El Español: {str(e)}')
                    continue
            
            return news_list
        except Exception as e:
            logger.error(f'Error obteniendo noticias de El Español: {str(e)}')
            return []

    async def get_expansion_news(self) -> List[Dict[str, Any]]:
        """
        Obtiene noticias de Expansión relacionadas con tecnología y telecomunicaciones
        """
        try:
            url = 'https://www.expansion.com/empresas/tecnologia.html'
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')
            
            news_list = []
            articles = soup.find_all('article', class_='news-item')
            
            for article in articles[:5]:  # Limitamos a 5 noticias
                try:
                    title = article.find('h2').text.strip()
                    link = article.find('h2').find('a')['href']
                    excerpt = article.find('p', class_='news-item-excerpt').text.strip() if article.find('p', class_='news-item-excerpt') else ''
                    
                    news_list.append({
                        'title': title,
                        'content': excerpt,
                        'url': link,
                        'source': 'Expansión',
                        'category': 'Negocios',
                        'date': datetime.now().strftime('%Y-%m-%d')
                    })
                except Exception as e:
                    logger.error(f'Error procesando artículo de Expansión: {str(e)}')
                    continue
            
            return news_list
        except Exception as e:
            logger.error(f'Error obteniendo noticias de Expansión: {str(e)}')
            return []

    async def get_eleconomista_news(self) -> List[Dict[str, Any]]:
        """
        Obtiene noticias de El Economista relacionadas con telecomunicaciones
        """
        try:
            url = 'https://www.eleconomista.es/noticias/telecomunicaciones'
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')
            
            news_list = []
            articles = soup.find_all('article')
            
            for article in articles[:5]:
                try:
                    title_element = article.find('h2') or article.find('h3')
                    if not title_element:
                        continue
                        
                    title = title_element.text.strip()
                    link = title_element.find('a')['href']
                    if not link.startswith('http'):
                        link = 'https://www.eleconomista.es' + link
                        
                    excerpt = ''
                    excerpt_element = article.find('p')
                    if excerpt_element:
                        excerpt = excerpt_element.text.strip()
                    
                    news_list.append({
                        'title': title,
                        'content': excerpt,
                        'url': link,
                        'source': 'El Economista',
                        'category': 'Telecomunicaciones',
                        'date': datetime.now().strftime('%Y-%m-%d')
                    })
                except Exception as e:
                    logger.error(f'Error procesando artículo de El Economista: {str(e)}')
                    continue
            
            return news_list
        except Exception as e:
            logger.error(f'Error obteniendo noticias de El Economista: {str(e)}')
            return []

    async def get_all_news(self) -> List[Dict[str, Any]]:
        """
        Obtiene y combina noticias de todas las fuentes
        """
        expansion_news = await self.get_expansion_news()
        elespanol_news = await self.get_elespanol_news()
        eleconomista_news = await self.get_eleconomista_news()
        
        # Combinamos y añadimos IDs
        all_news = expansion_news + elespanol_news + eleconomista_news
        for i, news in enumerate(all_news):
            news['id'] = str(i + 1)
        
        return all_news
