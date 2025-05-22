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

    async def get_xataka_news(self) -> List[Dict[str, Any]]:
        """
        Obtiene noticias de Xataka relacionadas con tecnología y telecomunicaciones
        """
        try:
            url = 'https://www.xataka.com/categoria/telecomunicaciones'
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')
            
            news_list = []
            articles = soup.find_all('article', class_='recent-abstract')
            
            for article in articles[:5]:  # Limitamos a 5 noticias
                try:
                    title = article.find('h2').text.strip()
                    link = article.find('h2').find('a')['href']
                    excerpt = article.find('div', class_='abstract-excerpt').text.strip()
                    
                    news_list.append({
                        'title': title,
                        'content': excerpt,
                        'url': link,
                        'source': 'Xataka',
                        'category': 'Tecnología',
                        'date': datetime.now().strftime('%Y-%m-%d')
                    })
                except Exception as e:
                    logger.error(f'Error procesando artículo de Xataka: {str(e)}')
                    continue
            
            return news_list
        except Exception as e:
            logger.error(f'Error obteniendo noticias de Xataka: {str(e)}')
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

    async def get_all_news(self) -> List[Dict[str, Any]]:
        """
        Obtiene y combina noticias de todas las fuentes
        """
        xataka_news = await self.get_xataka_news()
        expansion_news = await self.get_expansion_news()
        
        # Combinamos y añadimos IDs
        all_news = xataka_news + expansion_news
        for i, news in enumerate(all_news):
            news['id'] = str(i + 1)
        
        return all_news
