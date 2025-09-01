from config import CONFIGS
from build_knowledge_base import Crawler

for cfg in CONFIGS:
    crawler = Crawler(
        api=cfg["api"],
        output_path=cfg["output_path"],
        params=cfg["params"]
    )
    crawler.make_presence_known()
    crawler.crawl_over_all()