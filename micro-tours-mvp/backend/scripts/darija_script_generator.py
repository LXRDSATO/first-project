import openai
import re
import logging
from backend.config.settings import OPENAI_API_KEY

# TTS hacks for Darija pronunciation
DARija_TTS_HACKS = [
    (r"\bzbda\b", "zebda"),
    (r"\blmakla\b", "lemakla"),
    (r"\bkhobz\b", "khobez"),
    (r"\b9hwa\b", "kahwa"),
    (r"\bma\b", "maa"),
    (r"\bsh\b", "ch"),
    # Add more as needed
]

TEMPLATES = {
    "cafe": "مرحبا بكم ف {name}! هاد القهوة معروفة ف {city} بجوها الزوين و المنظر ديالها. تقدر تجي تشرب 9hwa مع صحابك و تستمتع بالهدوء. العنوان: {address}.",
    "monument": "كتعرفو {name}؟ هاد المعلمة التاريخية ف {city} عندها قصة كبيرة و كتشهد على تاريخ المغرب. متنساش تزورها و تاخد تصاور!",
    "souk": "سوق {name} ف {city} هو المكان لي تلقى فيه كلشي: lmakla, zbda, khobz و حتى الحوايج التقليدية. جرب تمشى فيه و عيش الأجواء المغربية!",
    "garden": "حديقة {name} ف {city} مكان زوين للراحة و الاسترخاء. تقدر تجي مع العائلة و تدوز نهار زوين وسط الطبيعة."
}

class DarijaScriptGenerator:
    def __init__(self, api_key=None):
        self.api_key = api_key or OPENAI_API_KEY
        openai.api_key = self.api_key
        self.logger = logging.getLogger("microtours.darija")

    def tts_hacks(self, text):
        for pattern, replacement in DARija_TTS_HACKS:
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        return text

    def generate_script(self, spot, category="cafe", city="المغرب"):
        template = TEMPLATES.get(category, TEMPLATES["cafe"])
        prompt = template.format(
            name=spot.get("name", "المكان"),
            city=city,
            address=spot.get("address", "")
        )
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "أنت صانع محتوى مغربي. اكتب نص قصير (30-60 ثانية) عن هذا المكان بأسلوب دارجة مغربية، مع أرقام عربية وكلمات فرنسية عند الحاجة. كن ودودا ومرحا."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=180,
                temperature=0.8
            )
            script = response.choices[0].message.content.strip()
            return self.tts_hacks(script)
        except Exception as e:
            self.logger.exception("OpenAI script generation failed")
            return self.tts_hacks(prompt)
