import feedparser
import requests
from datetime import datetime
from dateutil import parser

# List of AI Blog RSS Feed URLs
RSS_FEEDS = {
    "AI Roadmap Institute Blog": "https://medium.com/feed/ai-roadmap-institute",
    "AI Summer": "https://theaisummer.com/feed.xml",
    "AI Trends": "https://www.aitrends.com/feed/",
    "AIIOT Artificial Intelligence | Internet of Things | Technology": "https://www.aiiottalk.com/feed/",
    "Ankit-AI": "http://ankit-ai.blogspot.com/feeds/posts/default?alt=rss",
    "Another Datum": "https://anotherdatum.com/feeds/all.atom.xml?format=xml",
    "Artificial Intelligence": "https://www.aiplusinfo.com/feed/",
    "Artificial Intelligence Resources": "http://airesources.blogspot.com/feeds/posts/default?alt=rss",
    "Artificial Intelligence with Lex Fridman": "https://lexfridman.com/category/ai/feed/",
    "Artificial Lawyer": "https://www.artificiallawyer.com/feed/",
    "AWS - Machine Learning Blog": "https://aws.amazon.com/blogs/machine-learning/feed/",
    "Big Data Analytics News": "https://bigdataanalyticsnews.com/category/artificial-intelligence/feed/",
    "Chatbots Magazine": "https://chatbotsmagazine.com/feed",
    "Clarifai Blog": "https://www.clarifai.com/blog/rss.xml",
    "Cortana Intelligence and Machine Learning Blog": "https://docs.microsoft.com/en-us/archive/blogs/machinelearning/feed.xml",
    "CyberSEO Pro Blog": "https://www.cyberseo.net/blog/feed/",
    "Dale on AI": "https://daleonai.com/feed.xml",
    "Dan Rose AI": "https://www.danrose.ai/blog?format=rss",
    "DataRobot Blog": "https://www.datarobot.com/blog/feed/",
    "DatumBox": "http://blog.datumbox.com/feed/",
    "DeepCognition.ai": "https://deepcognition.ai/feed/",
    "DeepMind": "https://deepmind.com/blog/feed/basic/",
    "ELEDIA E-AIR": "http://www.eledia.org/e-air/feed/",
    "Find New AI": "https://findnewai.com/feed/",
    "Fusemachines Insights": "https://insights.fusemachines.com/feed/",
    "Great Learning - Artificial Intelligence": "https://www.greatlearning.in/blog/category/artificial-intelligence/feed/",
    "Isentia": "https://www.isentia.com/feed/",
    "KDnuggets": "http://www.kdnuggets.com/feed",
    "Kore.ai": "https://blog.kore.ai/rss.xml",
    "La Biblia de la IA": "https://editorialia.com/feed/",
    "Lorien Pratt": "https://www.lorienpratt.com/category/artificial-intelligence/feed/",
    "Mantra Labs": "https://www.mantralabsglobal.com/blog/feed/",
    "Marketing Artificial Intelligence Institute": "http://www.marketingaiinstitute.com/blog/rss.xml",
    "MarkTechPost": "https://www.marktechpost.com/feed/",
    "MarkTechPost | Artificial Intelligence": "https://www.marktechpost.com/category/technology/artificial-intelligence/feed",
    "MassTLC": "https://www.masstlc.org/category/ai/feed/",
    "Medium - Archie.AI": "https://medium.com/feed/archieai",
    "MetaDevo AI Blog": "http://metadevo.com/feed/",
    "MIT News - Artificial intelligence": "http://news.mit.edu/rss/topic/artificial-intelligence2",
    "MIT Technology Review - Artificial Intelligence": "https://www.technologyreview.com/topic/artificial-intelligence/feed",
    "Nanonets": "https://nanonets.com/blog/rss/",
    "O'Reilly Media - AI & ML": "https://www.oreilly.com/radar/topics/ai-ml/feed/index.xml",
    "Rainbird AI Blog": "https://rainbird.ai/feed/",
    "Robot Writers AI": "https://robotwritersai.com/feed/",
    "RStudio AI Blog": "https://blogs.rstudio.com/ai/index.xml",
    "SAS Blog": "https://blogs.sas.com/content/feed",
    "Singularity Weblog": "https://www.singularityweblog.com/blog/feed/",
    "TechSpective | Artificial Intelligence": "https://techspective.net/category/technology/artificial-intelligence/feed/",
    "The Berkeley Artificial Intelligence Research Blog": "https://bair.berkeley.edu/blog/feed.xml",
    "TOPBOTS": "https://www.topbots.com/feed/",
    "Towards Data Science": "https://towardsdatascience.com/feed",
    "Unite.AI": "https://www.unite.ai/feed/",
    "USM Systems": "https://usmsystems.com/blog/feed/",
    "viAct.ai": "https://www.viact.ai/blog-feed.xml"
}


HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; AI-Blog-Aggregator/1.0)"
}

def parse_date(date_str):
    try:
        dt = parser.parse(date_str)
        # Remove timezone information
        if dt.tzinfo is not None:
            dt = dt.replace(tzinfo=None)
        return dt
    except Exception:
        return datetime.min

def fetch_blog_posts():
    all_posts = []
    
    for source_name, url in RSS_FEEDS.items():
        try:
            print(f"Fetching {source_name}...")
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()

            feed = feedparser.parse(response.content)

            for entry in feed.entries:
                published = entry.get('published', '') or entry.get('updated', '')
                all_posts.append({
                    "title": entry.title,
                    "link": entry.link,
                    "published": parse_date(published),
                    "source": source_name,
                    "summary": entry.summary
                })
        
        except Exception as e:
            print(f"Error fetching {source_name}: {e}")
    
    # Sort posts by already parsed datetime
    all_posts.sort(key=lambda x: x["published"], reverse=True)
    
    return all_posts
