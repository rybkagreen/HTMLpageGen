from typing import Dict, Any, List, Optional
from bs4 import BeautifulSoup
import re


class SEOService:
    def __init__(self):
        pass
    
    def analyze_html(self, html: str) -> Dict[str, Any]:
        """
        Analyze HTML for SEO optimization opportunities
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        analysis = {
            "title": self._analyze_title(soup),
            "meta_description": self._analyze_meta_description(soup),
            "headings": self._analyze_headings(soup),
            "images": self._analyze_images(soup),
            "links": self._analyze_links(soup),
            "content": self._analyze_content(soup),
            "score": 0,
            "issues": [],
            "recommendations": []
        }
        
        # Calculate overall score
        analysis["score"] = self._calculate_seo_score(analysis)
        
        return analysis
    
    def _analyze_title(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Analyze page title"""
        title_tag = soup.find('title')
        
        if not title_tag:
            return {
                "exists": False,
                "length": 0,
                "text": "",
                "issues": ["Missing title tag"]
            }
        
        title_text = title_tag.get_text().strip()
        length = len(title_text)
        
        issues = []
        if length == 0:
            issues.append("Empty title tag")
        elif length < 30:
            issues.append("Title too short (should be 30-60 characters)")
        elif length > 60:
            issues.append("Title too long (should be 30-60 characters)")
        
        return {
            "exists": True,
            "length": length,
            "text": title_text,
            "issues": issues
        }
    
    def _analyze_meta_description(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Analyze meta description"""
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        
        if not meta_desc:
            return {
                "exists": False,
                "length": 0,
                "text": "",
                "issues": ["Missing meta description"]
            }
        
        desc_text = meta_desc.get('content', '').strip()
        length = len(desc_text)
        
        issues = []
        if length == 0:
            issues.append("Empty meta description")
        elif length < 120:
            issues.append("Meta description too short (should be 120-160 characters)")
        elif length > 160:
            issues.append("Meta description too long (should be 120-160 characters)")
        
        return {
            "exists": True,
            "length": length,
            "text": desc_text,
            "issues": issues
        }
    
    def _analyze_headings(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Analyze heading structure"""
        headings = {f'h{i}': [] for i in range(1, 7)}
        
        for i in range(1, 7):
            tags = soup.find_all(f'h{i}')
            headings[f'h{i}'] = [tag.get_text().strip() for tag in tags]
        
        issues = []
        if not headings['h1']:
            issues.append("Missing H1 tag")
        elif len(headings['h1']) > 1:
            issues.append("Multiple H1 tags found")
        
        return {
            "structure": headings,
            "h1_count": len(headings['h1']),
            "total_headings": sum(len(h) for h in headings.values()),
            "issues": issues
        }
    
    def _analyze_images(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Analyze images for SEO"""
        images = soup.find_all('img')
        
        total_images = len(images)
        missing_alt = 0
        empty_alt = 0
        
        for img in images:
            alt = img.get('alt')
            if alt is None:
                missing_alt += 1
            elif alt.strip() == '':
                empty_alt += 1
        
        issues = []
        if missing_alt > 0:
            issues.append(f"{missing_alt} images missing alt attribute")
        if empty_alt > 0:
            issues.append(f"{empty_alt} images with empty alt attribute")
        
        return {
            "total": total_images,
            "missing_alt": missing_alt,
            "empty_alt": empty_alt,
            "issues": issues
        }
    
    def _analyze_links(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Analyze internal and external links"""
        links = soup.find_all('a', href=True)
        
        internal_links = []
        external_links = []
        
        for link in links:
            href = link['href']
            if href.startswith('http'):
                external_links.append(href)
            else:
                internal_links.append(href)
        
        return {
            "total": len(links),
            "internal": len(internal_links),
            "external": len(external_links),
            "issues": []
        }
    
    def _analyze_content(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Analyze content for SEO"""
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        text = soup.get_text()
        word_count = len(text.split())
        
        issues = []
        if word_count < 300:
            issues.append("Content too short (should be at least 300 words)")
        
        return {
            "word_count": word_count,
            "character_count": len(text),
            "issues": issues
        }
    
    def _calculate_seo_score(self, analysis: Dict[str, Any]) -> int:
        """Calculate overall SEO score (0-100)"""
        score = 100
        
        # Title analysis
        if not analysis["title"]["exists"] or analysis["title"]["issues"]:
            score -= 15
        
        # Meta description analysis
        if not analysis["meta_description"]["exists"] or analysis["meta_description"]["issues"]:
            score -= 15
        
        # Headings analysis
        if analysis["headings"]["issues"]:
            score -= 10
        
        # Images analysis
        if analysis["images"]["issues"]:
            score -= 10
        
        # Content analysis
        if analysis["content"]["issues"]:
            score -= 10
        
        return max(0, score)
    
    def generate_structured_data(self, content_type: str, data: Dict[str, Any]) -> str:
        """
        Generate JSON-LD structured data
        """
        structured_data_templates = {
            "article": {
                "@context": "https://schema.org",
                "@type": "Article",
                "headline": data.get("title", ""),
                "description": data.get("description", ""),
                "author": {
                    "@type": "Person",
                    "name": data.get("author", "")
                },
                "datePublished": data.get("date_published", ""),
                "image": data.get("image", "")
            },
            "webpage": {
                "@context": "https://schema.org",
                "@type": "WebPage",
                "name": data.get("title", ""),
                "description": data.get("description", ""),
                "url": data.get("url", "")
            }
        }
        
        template = structured_data_templates.get(content_type, structured_data_templates["webpage"])
        
        import json
        return json.dumps(template, indent=2)
