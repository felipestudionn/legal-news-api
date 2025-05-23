"""
Scraper para ComputerWorld España
"""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

async def get_computerworld_news() -> List[Dict]:
    """Obtiene noticias de ComputerWorld sobre tecnología"""
    try:
        url = 'https://www.computerworld.es/tecnologia'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        news_list = []
        articles = soup.find_all(['div', 'article'], class_=['noticia', 'post'])
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        for article in articles[:5]:
            try:
                link_element = article.find('a')
                if not link_element:
                    continue
                
                title = link_element.text.strip()
                url = link_element['href']
                if not url.startswith('http'):
                    url = 'https://www.computerworld.es' + url
                
                summary = ''
                summary_element = article.find(['p', 'div'], class_='entradilla')
                if summary_element:
                    summary = summary_element.text.strip()
                
                news = {
                    'title': title,
                    'url': url,
                    'content': summary,
                    'source': 'ComputerWorld',
                    'category': 'Tecnología',
                    'date': current_date
                }
                news_list.append(news)
                
            except Exception as e:
                logger.error(f'Error procesando noticia de ComputerWorld: {str(e)}')
                continue
                
        return news_list
        
    except Exception as e:
        logger.error(f'Error obteniendo noticias de ComputerWorld: {str(e)}')
        return []
