import google.generativeai as genai
import os
import time

# ЖАҢА API Ключіңіз
GOOGLE_API_KEY = "AIzaSyBurBDJiJxFsCyT0ISGuBTN9BnaP6uhIkE" 
genai.configure(api_key=GOOGLE_API_KEY)

def get_bot_response(user_message):
    try:
        model = genai.GenerativeModel('models/gemma-3-4b-it')
        
        shop_info = """
        LUMIÈRE D'OR БҮКІЛ АҚПАРАТЫ:
        - Мекенжай: Алматы қаласы, Достық даңғылы, 105.
        - Телефон/WhatsApp: +7 (707) 123-45-67.
        - Жұмыс уақыты: Күн сайын 09:00-ден 21:00-ге дейін.
        - Жеткізу: Қала ішінде 2 сағатта жеткіземіз. 20 000 теңгеден асса - тегін, әйтпесе 2000 теңге.
        - Байланыс: Инстаграм @lumiere_dor_flowers немесе сайттағы кері байланыс формасы.
        """

        prompt = f"""
        Сен "LUMIÈRE D'OR" дүкенінің көмекшісісің. 
        МЫНА СӨЗДЕРДІ ҒАНА ҚОЛДАНЫП ЖАУАП БЕР, ӨЗІҢНЕН СӨЗ ҚОСПА:

        1. Сәлемдесу: "Сәлеметсіз бе! Lumière d'Or гүл бутигіне қош келдіңіз! Сізге қалай көмектесе аламын?" Алайда бұны әр сұраныс сайын қолдану керек емес, тек пайдаланушы сәлем дегенде ғана. Сәлем деп жазбаса тек сұранысқа жауап бер.
        2. Мекенжай: "Біз Алматы қаласы, Достық даңғылы, 105 мекенжайында орналасқанбыз."
        3. Телефон: "Біздің байланыс нөміріміз: +7 (707) 123-45-67."
        4. Жеткізу: "Алматы қаласы бойынша 2 сағат ішінде жеткіземіз. 20 000 теңгеден жоғары тапсырысқа жеткізу тегін."

        Клиент сұрағы: {user_message}
        Жауапты қатесіз, таза қазақ тілінде жаз.
        """
        
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(temperature=0.1)
        )
        return response.text
    except Exception as e:
        return "Кешіріңіз, қазір техникалық ақау болып тұр. +7 (707) 123-45-67 нөміріне жазыңызшы."
    

def save_chat(user_msg, bot_msg):
    print(f"Chat Log - User: {user_msg} | Bot: {bot_msg}")