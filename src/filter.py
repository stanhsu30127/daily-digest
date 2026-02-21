import anthropic
import json
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

def filter_and_translate(articles):
    articles_text = ""
    for i, article in enumerate(articles):
        articles_text += f"[{i}] {article['title']}\n{article['summary']}\n\n"

    prompt = f"""你是一個新聞編輯助理。以下是今天抓到的新聞列表，請根據以下規則篩選並翻譯：

篩選規則：
1. 核心優先收錄：科技與半導體（VLSI、先進製程、AI硬體、NVIDIA/AMD、自駕車）、地緣政治與財經（美中台日關係、日本政策、匯率、全球供應鏈）
2. 廣度平衡：包含1-2則醫療、科學發現、社會議題的重大突破或高關注度新聞
3. 寧缺勿濫：沒有重大新聞的分類直接跳過

輸出分類：
- 全球頭條：當天最重要的大事
- 科技前線：半導體與AI產業動態
- 金融與政治：亞太地緣政治與市場變動
- 醫療與其他：重大醫學突破或社會焦點

請只回傳 JSON，不要有任何其他文字，所有中文輸出請使用台灣繁體中文，結構如下：
{{
  "全球頭條": [{{"index": 原始index, "title": "中文標題", "summary": "中文摘要"}}],
  "科技前線": [...],
  "金融與政治": [...],
  "醫療與其他": [...]
}}

如果某分類沒有符合的新聞，該分類回傳空 list。

新聞列表：
{articles_text}"""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}]
    )

    response_text = message.content[0].text.replace('```json', '').replace('```', '').strip()
    result = json.loads(response_text)

    for category, filtered_articles in result.items():
        for article in filtered_articles:
            original = articles[article['index']]
            article['link'] = original['link']
            article['source'] = original['source']

    return result