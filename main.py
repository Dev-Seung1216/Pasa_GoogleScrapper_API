from fastapi import FastAPI, HTTPException
from google_play_scraper import Sort, reviews
import uvicorn

app = FastAPI()


@app.get("/")
def home():
    return {"status": "alive", "message": "PASA Google Scraper API"}


@app.get("/scrape/{com.pasa.smartpasa}")
def scrape_reviews(app_id: str, lang: str = 'ko', country: str = 'kr', count: int = 20):
    try:
        result, _ = reviews(
            app_id,
            lang=lang,
            country=country,
            sort=Sort.NEWEST,
            count=count
        )

        # 데이터 정제
        cleaned_data = []
        for r in result:
            cleaned_data.append({
                'id': r['reviewId'],
                'userName': r['userName'],
                'content': r['content'],
                'score': r['score'],
                'at': r['at'].strftime('%Y-%m-%d'),  # 날짜 포맷 통일
                'replyContent': r['replyContent'] if r['replyContent'] else "",
                'repliedAt': r['repliedAt'].strftime('%Y-%m-%d') if r['repliedAt'] else ""
            })

        return {"success": True, "data": cleaned_data}

    except Exception as e:
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
