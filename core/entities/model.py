from sqlalchemy.ext.declarative import declarative_base
from abc import ABC, abstractmethod
import os
from typing import Dict, Any
from openai import OpenAI
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')

Base = declarative_base()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


class BaseModel(ABC):
    @property
    @abstractmethod
    def cost(self) -> int:
        pass
        
    @abstractmethod
    def predict(self, input_data: dict) -> dict:
        pass

class CheapModel(BaseModel):
    def __init__(self):
        pass
        
    @property
    def cost(self) -> int:
        return 10

    def predict(self, text: str) -> dict:
        hate = ["hate", "loath", "don't like", "abhor", "despise", "terrible", "awful"]
        like = ["like", "adore", "love", "awesome", "interesting", "perfect"]
        answer = "neutral"
        for word in hate:
            if word in text.lower():
                answer = "negative"
        for word in like:
            if word in text.lower():
                answer = "positive"
        return {
            "label": answer
        }
    


class MediumModel(BaseModel):
    def __init__(self):
        pass

    def predict(self, text: str) -> Dict[str, Any]:
        print('here1')
        sia = SentimentIntensityAnalyzer()
        sentiment = sia.polarity_scores(text)
        
        if sentiment['compound'] >= 0.05:
            answer = "positive"
        elif sentiment['compound'] <= -0.05:
            answer = "negative"
        else:
            answer = "neutral"
        print('ans medium', answer)
        return {"label": answer}

    @property
    def cost(self) -> int:
        return 20

class ExpensiveModel(BaseModel):
    def __init__(self):
        pass

    def predict(self, text: str) -> Dict[str, Any]:
        client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
        )

        completion = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
            "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
        },
        extra_body={},
        model="deepseek/deepseek-prover-v2:free",
        messages=[
            {
            "role": "user",
            "content": f"Do sentiment analysis of provided text. Return only one word: neutral/positive/negative.\n Text: {text} "
            }
        ]
        )
        if "positive" in completion.choices[0].message.content: answer = "positive"
        elif "negative" in completion.choices[0].message.content: answer = "negative"
        else: answer = "neutral"
        return {"label": answer}

    @property
    def cost(self) -> int:
        return 30