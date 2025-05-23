"""
Scraper para el Ministerio de Transformación Digital
"""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

async def get_transformacion_digital_news() -> List[Dict]:
    """Obtiene noticias del Ministerio de Transformación Digital"""
    try:
        url = 'https://transformaciondigital.gob.es/es/prensa'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        news_list = []
        articles = soup.find_all('div', class_='views-row')
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        for article in articles[:5]:
            try:
                link_element = article.find('a')
                if not link_element:
                    continue
                    
                title = link_element.text.strip()
                url = link_element['href']
                if not url.startswith('http'):
                    url = 'https://transformaciondigital.gob.es' + url
                
                news = {
                    'title': title,
                    'url': url,
                    'content': '',  # No hay resumen disponible
                    'source': 'Ministerio de Transformación Digital',
                    'category': 'Regulación',
                    'date': current_date
                }
                news_list.append(news)
                
            except Exception as e:
                logger.error(f'Error procesando noticia del Ministerio: {str(e)}')
                continue
                
        return news_list
        
    except Exception as e:
        logger.error(f'Error obteniendo noticias del Ministerio: {str(e)}')
        return []
