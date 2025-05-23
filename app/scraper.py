import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict, Any
import logging
import json
import os
from pathlib import Path
import feedparser
from dateutil import parser

# Importar scrapers individuales
from .scrapers.redes import get_redes_news
from .scrapers.cinco_dias import get_cinco_dias_news
from .scrapers.computerworld import get_computerworld_news
from .scrapers.silicon import get_silicon_news
from .scrapers.muycomputer import get_muycomputer_news

# Configuración del logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NewsScraper:
    def __init__(self):
        # Headers para simular un navegador
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
        }
        # Directorio para almacenar las noticias
        self.data_dir = Path(__file__).parent / 'data'
        self.data_dir.mkdir(exist_ok=True)

    async def get_elespanol_news(self) -> List[Dict[str, Any]]:
        """
        Obtiene noticias de El Español relacionadas con telecomunicaciones
        """
        try:
            url = 'https://www.elespanol.com/temas/telecomunicaciones/'
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
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
            soup = BeautifulSoup(response.text, 'html.parser')
            
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
        Obtiene noticias de El Economista relacionadas con telecomunicaciones.
        Actualmente deshabilitado debido a protección anti-scraping.
        """
        # TODO: Implementar usando Selenium/Playwright o API oficial cuando esté disponible
        return []

    async def get_cnmc_news(self, target_date: str = None) -> List[Dict]:
        """Get telecom news from CNMC RSS feed."""
        try:
            logger.info('Obteniendo noticias de CNMC...')
            # Fetch RSS feed (filtrado por telecomunicaciones, tag_id=12)
            feed_url = 'https://www.cnmc.es/feed/all?field_tags_target_id=12'
            logger.info(f'URL del feed: {feed_url}')
            feed = feedparser.parse(feed_url)
            logger.info(f'Entradas encontradas en el feed: {len(feed.entries)}')
            news_list = []
            current_date = target_date if target_date else datetime.now().strftime("%Y-%m-%d")
            logger.info(f'Fecha objetivo: {current_date}')
            
            # El feed ya viene filtrado por telecomunicaciones (tag_id=12)
            for entry in feed.entries:
                # Parse publication date
                logger.info(f'Procesando entrada: {entry.title}')
                pub_date = parser.parse(entry.published)
                news_date = pub_date.strftime("%Y-%m-%d")
                logger.info(f'Fecha de publicación: {news_date}')
                
                # Solo incluir noticias de hoy
                if news_date == current_date:
                    logger.info('La noticia es de hoy, incluyéndola...')
                    news = {
                        'title': entry.title,
                        'content': entry.get('description', ''),
                        'url': entry.link,
                        'source': 'CNMC',
                        'category': 'Regulación',  # CNMC es el regulador
                        'date': news_date,
                        'id': entry.guid.split(' at ')[0]  # CNMC usa IDs numéricos
                    }
                    news_list.append(news)
                else:
                    logger.info('La noticia no es de hoy, ignorándola...')

            return news_list
        except Exception as e:
            print(f"Error fetching CNMC news: {str(e)}")
            return []

    def save_news(self, news: List[Dict[str, Any]], date: str = None) -> None:
        """
        Guarda las noticias en un archivo JSON por fecha
        """
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
            
        file_path = self.data_dir / f'news_{date}.json'
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(news, f, ensure_ascii=False, indent=2)
            
    def load_news(self, date: str = None) -> List[Dict[str, Any]]:
        """
        Carga las noticias desde un archivo JSON por fecha
        """
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
            
        file_path = self.data_dir / f'news_{date}.json'
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def list_available_dates(self) -> List[str]:
        """
        Lista las fechas disponibles en el histórico
        """
        dates = []
        for file in self.data_dir.glob('news_*.json'):
            date = file.name.replace('news_', '').replace('.json', '')
            dates.append(date)
        return sorted(dates, reverse=True)

    async def get_all_news(self, date: str = None) -> List[Dict]:
        """Get news from all sources and combine them."""
        current_date = datetime.now().strftime("%Y-%m-%d")

        # If no date is provided or the date is today, scrape fresh news
        if date is None or date == current_date:
            # Medios tradicionales
            expansion_news = await self.get_expansion_news()
            elespanol_news = await self.get_elespanol_news()
            eleconomista_news = await self.get_eleconomista_news()
            
            # Reguladores y organismos oficiales
            cnmc_news = await self.get_cnmc_news()
            redes_news = await get_redes_news()
            
            # Medios especializados
            cinco_dias_news = await get_cinco_dias_news()
            computerworld_news = await get_computerworld_news()
            silicon_news = await get_silicon_news()
            muycomputer_news = await get_muycomputer_news()

            # Combine all news
            all_news = []
            
            # Medios tradicionales
            all_news.extend(expansion_news)
            all_news.extend(elespanol_news)
            all_news.extend(eleconomista_news)
            
            # Reguladores y organismos oficiales
            all_news.extend(cnmc_news)
            all_news.extend(redes_news)
            
            # Medios especializados
            all_news.extend(cinco_dias_news)
            all_news.extend(computerworld_news)
            all_news.extend(silicon_news)
            all_news.extend(muycomputer_news)

            # Save today's news
            self.save_news(all_news, current_date)

            return all_news
        else:
            # Try to load historical news for the specified date
            return self.load_news(date)
