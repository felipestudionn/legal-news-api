"""
Scraper para Red.es
"""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

async def get_redes_news() -> List[Dict]:
    """Obtiene noticias de Red.es"""
    try:
        url = 'https://www.red.es/redes/sala-de-prensa/noticias'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        news_list = []
        articles = soup.find_all('div', class_='noticia-item')
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        for article in articles[:5]:  # Limitamos a 5 noticias
            try:
                link_element = article.find('a')
                if not link_element:
                    continue
                    
                title = link_element.text.strip()
                url = link_element['href']
                if not url.startswith('http'):
                    url = 'https://www.red.es' + url
                
                summary = ''
                summary_element = article.find('p')
                if summary_element:
                    summary = summary_element.text.strip()
                
                news = {
                    'title': title,
                    'url': url,
                    'content': summary,
                    'source': 'Red.es',
                    'category': 'Regulación',
                    'date': current_date
                }
                news_list.append(news)
                
            except Exception as e:
                logger.error(f'Error procesando noticia de Red.es: {str(e)}')
                continue
                
        return news_list
        
    except Exception as e:
        logger.error(f'Error obteniendo noticias de Red.es: {str(e)}')
        return []
