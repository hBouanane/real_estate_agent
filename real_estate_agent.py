"""
Real Estate Agency Agent - Moroccan Darija
Built with LangGraph, LangChain (modern pattern)
Uses: MessagesState + ToolNode + create_react_agent
"""

import re
import os
from difflib import SequenceMatcher
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

# ==================== MODEL ====================

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7,
    max_tokens=2048,
)

model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.7,
)

# ==================== PROPERTY DATABASE ====================

PROPERTIES = [
    {
        "id": 1,
        "type": "شقة",
        "location": "مراكش - جليز",
        "price": "1,350,000 درهم",
        "bedrooms": 2,
        "area": "85م²",
        "desc": "شقة عصرية مع شرفة في قلب جليز"
    },
    {
        "id": 2,
        "type": "شقة",
        "location": "مراكش - الحي الشتوي",
        "price": "2,500,000 درهم",
        "bedrooms": 3,
        "area": "140م²",
        "desc": "شقة فاخرة في إقامة راقية مع مسبح"
    },
    {
        "id": 3,
        "type": "شقة",
        "location": "مراكش - ماجوريل",
        "price": "1,100,000 درهم",
        "bedrooms": 2,
        "area": "78م²",
        "desc": "شقة هادئة بالقرب من حديقة ماجوريل"
    },
    {
        "id": 4,
        "type": "شقة",
        "location": "مراكش - أكدال",
        "price": "1,600,000 درهم",
        "bedrooms": 3,
        "area": "110م²",
        "desc": "شقة بإطلالة على جبال الأطلس"
    },
    {
        "id": 5,
        "type": "شقة",
        "location": "مراكش - جليز",
        "price": "1,850,000 درهم",
        "bedrooms": 3,
        "area": "125م²",
        "desc": "شقة واسعة بتشطيبات رخامية"
    },
    {
        "id": 6,
        "type": "شقة",
        "location": "مراكش - فيكتور هوغو",
        "price": "2,100,000 درهم",
        "bedrooms": 3,
        "area": "130م²",
        "desc": "شقة ممتازة في شارع هادئ وآمن"
    },
    {
        "id": 7,
        "type": "شقة",
        "location": "مراكش - الحي الشتوي",
        "price": "3,200,000 درهم",
        "bedrooms": 4,
        "area": "180م²",
        "desc": "بانتهاوس فاخر مع تراس كبير"
    },
    {
        "id": 8,
        "type": "شقة",
        "location": "مراكش - أكدال",
        "price": "1,450,000 درهم",
        "bedrooms": 2,
        "area": "95م²",
        "desc": "شقة ممتازة للعائلات بالقرب من المزار مول"
    },
    {
        "id": 9,
        "type": "شقة",
        "location": "مراكش - ماجوريل",
        "price": "1,250,000 درهم",
        "bedrooms": 2,
        "area": "82م²",
        "desc": "شقة بتصميم حديث ومطبخ مجهز"
    },
    {
        "id": 10,
        "type": "شقة",
        "location": "مراكش - جليز",
        "price": "950,000 درهم",
        "bedrooms": 1,
        "area": "60م²",
        "desc": "شقة استثمارية ممتازة للكراء السياحي"
    },
    {
        "id": 11,
        "type": "شقة",
        "location": "مراكش - الحي الشتوي",
        "price": "1,950,000 درهم",
        "bedrooms": 2,
        "area": "100م²",
        "desc": "شقة راقية قريبة من فنادق الخمس نجوم"
    },
    {
        "id": 12,
        "type": "شقة",
        "location": "مراكش - أكدال",
        "price": "1,750,000 درهم",
        "bedrooms": 3,
        "area": "115م²",
        "desc": "شقة مع حديقة صغيرة في الطابق الأرضي"
    },
    {
        "id": 13,
        "type": "شقة",
        "location": "مراكش - جليز",
        "price": "2,300,000 درهم",
        "bedrooms": 4,
        "area": "150م²",
        "desc": "شقة عائلية كبيرة في تقاطع رئيسي"
    },
    {
        "id": 14,
        "type": "شقة",
        "location": "مراكش - فيكتور هوغو",
        "price": "1,650,000 درهم",
        "bedrooms": 2,
        "area": "90م²",
        "desc": "شقة مشمسة طوال اليوم بفضل واجهتين"
    },
    {
        "id": 15,
        "type": "شقة",
        "location": "مراكش - ماجوريل",
        "price": "1,400,000 درهم",
        "bedrooms": 3,
        "area": "105م²",
        "desc": "شقة مجددة بالكامل بلمسة تقليدية عصرية"
    },
    {
        "id": 16,
        "type": "شقة",
        "location": "مراكش - الحي الشتوي",
        "price": "2,800,000 درهم",
        "bedrooms": 3,
        "area": "160م²",
        "desc": "شقة فاخرة مجهزة بنظام المنزل الذكي"
    },
    {
        "id": 17,
        "type": "شقة",
        "location": "مراكش - جليز",
        "price": "1,550,000 درهم",
        "bedrooms": 2,
        "area": "92م²",
        "desc": "شقة ممتازة في شارع محمد الخامس"
    },
    {
        "id": 18,
        "type": "شقة",
        "location": "مراكش - أكدال",
        "price": "2,000,000 درهم",
        "bedrooms": 3,
        "area": "135م²",
        "desc": "شقة دوبلكس رائعة في إقامة سياحية"
    },
    {
        "id": 19,
        "type": "شقة",
        "location": "مراكش - ماجوريل",
        "price": "1,150,000 درهم",
        "bedrooms": 2,
        "area": "75م²",
        "desc": "شقة مثالية للشباب في حي راقٍ"
    },
    {
        "id": 20,
        "type": "شقة",
        "location": "مراكش - جليز",
        "price": "1,700,000 درهم",
        "bedrooms": 3,
        "area": "118م²",
        "desc": "شقة قريبة من محطة القطار"
    },
    {
        "id": 21,
        "type": "شقة",
        "location": "مراكش - المحاميد",
        "price": "350,000 درهم",
        "bedrooms": 2,
        "area": "60م²",
        "desc": "شقة اقتصادية في موقع جيد"
    },
    {
        "id": 22,
        "type": "شقة",
        "location": "مراكش - المسيرة",
        "price": "450,000 درهم",
        "bedrooms": 2,
        "area": "70م²",
        "desc": "شقة في حي حيوي قريب من المدارس"
    },
    {
        "id": 23,
        "type": "شقة",
        "location": "مراكش - أبواب مراكش",
        "price": "550,000 درهم",
        "bedrooms": 3,
        "area": "85م²",
        "desc": "شقة عائلية في إقامة محروسة"
    },
    {
        "id": 24,
        "type": "شقة",
        "location": "مراكش - الازدهار",
        "price": "750,000 درهم",
        "bedrooms": 2,
        "area": "80م²",
        "desc": "شقة بتشطيبات جيدة في حي هادئ"
    },
    {
        "id": 25,
        "type": "شقة",
        "location": "مراكش - الداوديات",
        "price": "600,000 درهم",
        "bedrooms": 2,
        "area": "75م²",
        "desc": "شقة قريبة من الكليات، مثالية للطلبة"
    },
    {
        "id": 26,
        "type": "شقة",
        "location": "مراكش - المحاميد",
        "price": "250,000 درهم",
        "bedrooms": 1,
        "area": "50م²",
        "desc": "شقة اقتصادية نظيفة ومصبوغة حديثاً"
    },
    {
        "id": 27,
        "type": "شقة",
        "location": "مراكش - المسيرة 2",
        "price": "520,000 درهم",
        "bedrooms": 3,
        "area": "90م²",
        "desc": "شقة واسعة صالحة لعائلة كبيرة"
    },
    {
        "id": 28,
        "type": "شقة",
        "location": "مراكش - مبروكة",
        "price": "650,000 درهم",
        "bedrooms": 2,
        "area": "78م²",
        "desc": "شقة حديثة البناء بإقامة جديدة"
    },
    {
        "id": 29,
        "type": "شقة",
        "location": "مراكش - تاركة",
        "price": "850,000 درهم",
        "bedrooms": 2,
        "area": "95م²",
        "desc": "شقة راقية في منطقة تاركة"
    },
    {
        "id": 30,
        "type": "شقة",
        "location": "مراكش - العزوزية",
        "price": "320,000 درهم",
        "bedrooms": 2,
        "area": "55م²",
        "desc": "شقة اقتصادية بإطلالة غير مجروحة"
    },
    {
        "id": 31,
        "type": "شقة",
        "location": "مراكش - المحاميد 9",
        "price": "480,000 درهم",
        "bedrooms": 2,
        "area": "72م²",
        "desc": "شقة متوسطة ممتازة ومجهزة جزئياً"
    },
    {
        "id": 32,
        "type": "شقة",
        "location": "مراكش - أبواب مراكش",
        "price": "500,000 درهم",
        "bedrooms": 2,
        "area": "68م²",
        "desc": "شقة بإقامة بها مسبح وأمن 24/7"
    },
    {
        "id": 33,
        "type": "شقة",
        "location": "مراكش - الداوديات",
        "price": "680,000 درهم",
        "bedrooms": 3,
        "area": "90م²",
        "desc": "شقة مجددة في حي عريق وهادئ"
    },
    {
        "id": 34,
        "type": "شقة",
        "location": "مراكش - الازدهار",
        "price": "820,000 درهم",
        "bedrooms": 3,
        "area": "95م²",
        "desc": "شقة بواجهتين مشمسة جداً"
    },
    {
        "id": 35,
        "type": "شقة",
        "location": "مراكش - سيدي يوسف بن علي",
        "price": "380,000 درهم",
        "bedrooms": 2,
        "area": "65م²",
        "desc": "شقة تقليدية في حي شعبي أصيل"
    },
    {
        "id": 36,
        "type": "شقة",
        "location": "مراكش - المسيرة 1",
        "price": "470,000 درهم",
        "bedrooms": 2,
        "area": "74م²",
        "desc": "شقة قريبة من محطة الحافلات"
    },
    {
        "id": 37,
        "type": "شقة",
        "location": "مراكش - الشريفية",
        "price": "700,000 درهم",
        "bedrooms": 2,
        "area": "82م²",
        "desc": "شقة ممتازة في طريق أمزميز"
    },
    {
        "id": 38,
        "type": "شقة",
        "location": "مراكش - مبروكة",
        "price": "580,000 درهم",
        "bedrooms": 2,
        "area": "70م²",
        "desc": "شقة مريحة للبيع المستعجل"
    },
    {
        "id": 39,
        "type": "شقة",
        "location": "مراكش - العزوزية",
        "price": "400,000 درهم",
        "bedrooms": 2,
        "area": "60م²",
        "desc": "شقة محفظة جاهزة للتسليم"
    },
    {
        "id": 40,
        "type": "شقة",
        "location": "مراكش - أبواب مراكش",
        "price": "600,000 درهم",
        "bedrooms": 3,
        "area": "88م²",
        "desc": "شقة نظيفة بتشطيبات ممتازة"
    },
    {
        "id": 41,
        "type": "فيلا",
        "location": "مراكش - النخيل",
        "price": "12,500,000 درهم",
        "bedrooms": 6,
        "area": "1500م²",
        "desc": "فيلا فخمة وسط واحة النخيل مع مسبح"
    },
    {
        "id": 42,
        "type": "فيلا",
        "location": "مراكش - طريق أوريكا",
        "price": "8,000,000 درهم",
        "bedrooms": 5,
        "area": "1000م²",
        "desc": "فيلا عصرية بإطلالة على جبال الأطلس"
    },
    {
        "id": 43,
        "type": "فيلا",
        "location": "مراكش - طريق أمزميز",
        "price": "9,500,000 درهم",
        "bedrooms": 5,
        "area": "1200م²",
        "desc": "فيلا راقية بجوار ملاعب الجولف"
    },
    {
        "id": 44,
        "type": "فيلا",
        "location": "مراكش - النخيل",
        "price": "25,000,000 درهم",
        "bedrooms": 8,
        "area": "3000م²",
        "desc": "قصر بتصميم عربي أندلسي"
    },
    {
        "id": 45,
        "type": "فيلا",
        "location": "مراكش - طريق فاس",
        "price": "7,200,000 درهم",
        "bedrooms": 4,
        "area": "900م²",
        "desc": "فيلا بتصميم مودرن مع واجهات زجاجية"
    },
    {
        "id": 46,
        "type": "فيلا",
        "location": "مراكش - طريق كازا",
        "price": "6,500,000 درهم",
        "bedrooms": 4,
        "area": "800م²",
        "desc": "فيلا ممتازة في إقامة مغلقة وآمنة"
    },
    {
        "id": 47,
        "type": "فيلا",
        "location": "مراكش - طريق أوريكا",
        "price": "14,000,000 درهم",
        "bedrooms": 6,
        "area": "2000م²",
        "desc": "فيلا سياحية مرخصة كدار ضيافة"
    },
    {
        "id": 48,
        "type": "فيلا",
        "location": "مراكش - النخيل",
        "price": "18,500,000 درهم",
        "bedrooms": 7,
        "area": "2500م²",
        "desc": "فيلا كلاسيكية مع مسبح مدفأ وحمام بلدي"
    },
    {
        "id": 49,
        "type": "فيلا",
        "location": "مراكش - طريق أمزميز",
        "price": "11,000,000 درهم",
        "bedrooms": 5,
        "area": "1400م²",
        "desc": "فيلا رائعة مع حديقة مصممة باحترافية"
    },
    {
        "id": 50,
        "type": "فيلا",
        "location": "مراكش - طريق أوريكا",
        "price": "9,000,000 درهم",
        "bedrooms": 5,
        "area": "1100م²",
        "desc": "فيلا مفروشة بأثاث فاخر مستورد"
    },
    {
        "id": 51,
        "type": "فيلا",
        "location": "مراكش - تاركة",
        "price": "4,500,000 درهم",
        "bedrooms": 4,
        "area": "400م²",
        "desc": "فيلا جميلة مع حديقة ومسبح"
    },
    {
        "id": 52,
        "type": "فيلا",
        "location": "مراكش - الشريفية",
        "price": "3,800,000 درهم",
        "bedrooms": 4,
        "area": "350م²",
        "desc": "فيلا عصرية في مجمع سكني هادئ"
    },
    {
        "id": 53,
        "type": "فيلا",
        "location": "مراكش - مبروكة",
        "price": "3,200,000 درهم",
        "bedrooms": 3,
        "area": "300م²",
        "desc": "فيلا ممتازة بثمن شقة كبيرة"
    },
    {
        "id": 54,
        "type": "فيلا",
        "location": "مراكش - تاركة",
        "price": "5,200,000 درهم",
        "bedrooms": 5,
        "area": "450م²",
        "desc": "فيلا واسعة مع قبو كامل وغرفة خدم"
    },
    {
        "id": 55,
        "type": "فيلا",
        "location": "مراكش - أبواب مراكش",
        "price": "2,800,000 درهم",
        "bedrooms": 3,
        "area": "250م²",
        "desc": "شبه فيلا بتصميم عصري"
    },
    {
        "id": 56,
        "type": "فيلا",
        "location": "مراكش - تاركة",
        "price": "6,000,000 درهم",
        "bedrooms": 5,
        "area": "500م²",
        "desc": "فيلا زاوية مشمسة ومستقلة"
    },
    {
        "id": 57,
        "type": "فيلا",
        "location": "مراكش - المسيرة 3",
        "price": "2,500,000 درهم",
        "bedrooms": 4,
        "area": "200م²",
        "desc": "فيلا اقتصادية مجددة في المسيرة"
    },
    {
        "id": 58,
        "type": "فيلا",
        "location": "مراكش - مبروكة",
        "price": "3,600,000 درهم",
        "bedrooms": 4,
        "area": "320م²",
        "desc": "فيلا بتصميم كلاسيكي، بناء متين"
    },
    {
        "id": 59,
        "type": "فيلا",
        "location": "مراكش - تاركة",
        "price": "4,800,000 درهم",
        "bedrooms": 4,
        "area": "420م²",
        "desc": "فيلا مع مسبح خاص وكراج لسيارتين"
    },
    {
        "id": 60,
        "type": "فيلا",
        "location": "مراكش - الشريفية",
        "price": "3,500,000 درهم",
        "bedrooms": 3,
        "area": "310م²",
        "desc": "فيلا مجهزة بالطاقة الشمسية"
    },
    {
        "id": 61,
        "type": "رياض",
        "location": "مراكش - المدينة القديمة",
        "price": "2,500,000 درهم",
        "bedrooms": 5,
        "area": "180م²",
        "desc": "رياض تقليدي جميل قريب من ساحة جامع الفنا"
    },
    {
        "id": 62,
        "type": "رياض",
        "location": "مراكش - القصبة",
        "price": "4,200,000 درهم",
        "bedrooms": 6,
        "area": "220م²",
        "desc": "رياض مجدد يعمل كدار ضيافة"
    },
    {
        "id": 63,
        "type": "رياض",
        "location": "مراكش - المواسين",
        "price": "3,800,000 درهم",
        "bedrooms": 5,
        "area": "200م²",
        "desc": "رياض تاريخي مع نقوش خشبية أصلية"
    },
    {
        "id": 64,
        "type": "رياض",
        "location": "مراكش - رياض الزيتون",
        "price": "5,500,000 درهم",
        "bedrooms": 7,
        "area": "280م²",
        "desc": "رياض فخم مع مسبح وتراس بانورامي"
    },
    {
        "id": 65,
        "type": "رياض",
        "location": "مراكش - دار الباشا",
        "price": "8,000,000 درهم",
        "bedrooms": 8,
        "area": "400م²",
        "desc": "رياض كبير يمكن استغلاله كفندق بوتيك"
    },
    {
        "id": 66,
        "type": "رياض",
        "location": "مراكش - باب دكالة",
        "price": "1,800,000 درهم",
        "bedrooms": 4,
        "area": "120م²",
        "desc": "رياض صغير مثالي كسكن ثانوي"
    },
    {
        "id": 67,
        "type": "رياض",
        "location": "مراكش - المدينة القديمة",
        "price": "3,000,000 درهم",
        "bedrooms": 5,
        "area": "160م²",
        "desc": "رياض مع إمكانية وصول السيارة"
    },
    {
        "id": 68,
        "type": "رياض",
        "location": "مراكش - القصبة",
        "price": "6,500,000 درهم",
        "bedrooms": 6,
        "area": "300م²",
        "desc": "رياض فاخر بالقرب من قبور السعديين"
    },
    {
        "id": 69,
        "type": "رياض",
        "location": "مراكش - المواسين",
        "price": "2,200,000 درهم",
        "bedrooms": 4,
        "area": "140م²",
        "desc": "رياض يحتاج إصلاحات (فرصة استثمارية)"
    },
    {
        "id": 70,
        "type": "رياض",
        "location": "مراكش - رياض الزيتون",
        "price": "4,800,000 درهم",
        "bedrooms": 6,
        "area": "240م²",
        "desc": "رياض مصنف ومرخص سياحياً"
    },
    {
        "id": 71,
        "type": "استوديو",
        "location": "مراكش - جليز",
        "price": "650,000 درهم",
        "bedrooms": 1,
        "area": "45م²",
        "desc": "استوديو ممتاز للاستثمار السياحي (Airbnb)"
    },
    {
        "id": 72,
        "type": "استوديو",
        "location": "مراكش - أكدال",
        "price": "580,000 درهم",
        "bedrooms": 1,
        "area": "40م²",
        "desc": "استوديو في إقامة سياحية مع مسبح"
    },
    {
        "id": 73,
        "type": "استوديو",
        "location": "مراكش - الداوديات",
        "price": "350,000 درهم",
        "bedrooms": 1,
        "area": "35م²",
        "desc": "استوديو مثالي للطلبة قرب جامعة القاضي عياض"
    },
    {
        "id": 74,
        "type": "استوديو",
        "location": "مراكش - الازدهار",
        "price": "450,000 درهم",
        "bedrooms": 1,
        "area": "42م²",
        "desc": "استوديو جديد بتشطيبات حديثة"
    },
    {
        "id": 75,
        "type": "استوديو",
        "location": "مراكش - ماجوريل",
        "price": "750,000 درهم",
        "bedrooms": 1,
        "area": "50م²",
        "desc": "استوديو فاخر مفروش في منطقة راقية"
    },
    {
        "id": 76,
        "type": "استوديو",
        "location": "مراكش - جليز",
        "price": "600,000 درهم",
        "bedrooms": 1,
        "area": "38م²",
        "desc": "استوديو ببالكون مشمس في قلب جليز"
    },
    {
        "id": 77,
        "type": "استوديو",
        "location": "مراكش - الحي الشتوي",
        "price": "950,000 درهم",
        "bedrooms": 1,
        "area": "55م²",
        "desc": "استوديو بريميوم في أغلى أحياء مراكش"
    },
    {
        "id": 78,
        "type": "استوديو",
        "location": "مراكش - المحاميد",
        "price": "220,000 درهم",
        "bedrooms": 1,
        "area": "30م²",
        "desc": "استوديو اقتصادي للسكن أو الكراء"
    },
    {
        "id": 79,
        "type": "استوديو",
        "location": "مراكش - فيكتور هوغو",
        "price": "800,000 درهم",
        "bedrooms": 1,
        "area": "48م²",
        "desc": "استوديو عصري مع مطبخ أمريكي مجهز"
    },
    {
        "id": 80,
        "type": "استوديو",
        "location": "مراكش - الحي الشتوي",
        "price": "1,100,000 درهم",
        "bedrooms": 1,
        "area": "60م²",
        "desc": "استوديو واسع وفخم للباحثين عن الرفاهية"
    },
    {
        "id": 81,
        "type": "بقعة أرضية",
        "location": "مراكش - طريق أوريكا",
        "price": "1,500,000 درهم",
        "bedrooms": 0,
        "area": "10000م²",
        "desc": "هكتار أرض زراعية لبناء ضيعة"
    },
    {
        "id": 82,
        "type": "بقعة أرضية",
        "location": "مراكش - تاركة",
        "price": "2,200,000 درهم",
        "bedrooms": 0,
        "area": "500م²",
        "desc": "بقعة مجهزة لبناء فيلا سكنية"
    },
    {
        "id": 83,
        "type": "بقعة أرضية",
        "location": "مراكش - النخيل",
        "price": "6,000,000 درهم",
        "bedrooms": 0,
        "area": "10000م²",
        "desc": "أرض لبناء قصر أو مشروع سياحي"
    },
    {
        "id": 84,
        "type": "مزرعة",
        "location": "مراكش - طريق فاس",
        "price": "4,500,000 درهم",
        "bedrooms": 3,
        "area": "20000م²",
        "desc": "ضيعة فلاحية منتجة للزيتون مع منزل"
    },
    {
        "id": 85,
        "type": "مزرعة",
        "location": "مراكش - طريق أمزميز",
        "price": "8,000,000 درهم",
        "bedrooms": 4,
        "area": "30000م²",
        "desc": "مزرعة فاخرة مع فيلا ومسبح"
    },
    {
        "id": 86,
        "type": "محل تجاري",
        "location": "مراكش - جليز",
        "price": "3,500,000 درهم",
        "bedrooms": 0,
        "area": "80م²",
        "desc": "محل في شارع رئيسي مزدحم"
    },
    {
        "id": 87,
        "type": "محل تجاري",
        "location": "مراكش - المسيرة",
        "price": "900,000 درهم",
        "bedrooms": 0,
        "area": "45م²",
        "desc": "محل في سوق نشط للتجارة العامة"
    },
    {
        "id": 88,
        "type": "مكتب",
        "location": "مراكش - جليز",
        "price": "1,200,000 درهم",
        "bedrooms": 0,
        "area": "70م²",
        "desc": "مكتب أعمال مجهز في عمارة إدارية"
    },
    {
        "id": 89,
        "type": "محل تجاري",
        "location": "مراكش - سيدي غانم",
        "price": "2,800,000 درهم",
        "bedrooms": 0,
        "area": "200م²",
        "desc": "صالة عرض (Showroom) في الحي الصناعي"
    },
    {
        "id": 90,
        "type": "مكتب",
        "location": "مراكش - الحي الشتوي",
        "price": "1,900,000 درهم",
        "bedrooms": 0,
        "area": "90م²",
        "desc": "مكتب فخم لشركة متعددة الجنسيات"
    },
    {
        "id": 91,
        "type": "شقة للكراء",
        "location": "مراكش - جليز",
        "price": "6,000 درهم/شهر",
        "bedrooms": 2,
        "area": "80م²",
        "desc": "شقة مفروشة بالكامل للكراء الطويل"
    },
    {
        "id": 92,
        "type": "شقة للكراء",
        "location": "مراكش - المحاميد",
        "price": "2,000 درهم/شهر",
        "bedrooms": 2,
        "area": "60م²",
        "desc": "شقة فارغة للكراء السنوي"
    },
    {
        "id": 93,
        "type": "استوديو للكراء",
        "location": "مراكش - أكدال",
        "price": "4,500 درهم/شهر",
        "bedrooms": 1,
        "area": "45م²",
        "desc": "استوديو مفروش راقي بإقامة مع مسبح"
    },
    {
        "id": 94,
        "type": "شقة للكراء",
        "location": "مراكش - الحي الشتوي",
        "price": "12,000 درهم/شهر",
        "bedrooms": 3,
        "area": "140م²",
        "desc": "شقة فخمة للإيجار قريبة من المنارة مول"
    },
    {
        "id": 95,
        "type": "شقة للكراء",
        "location": "مراكش - المسيرة",
        "price": "2,500 درهم/شهر",
        "bedrooms": 2,
        "area": "70م²",
        "desc": "شقة نظيفة غير مفروشة في حي هادئ"
    },
    {
        "id": 96,
        "type": "استوديو للكراء",
        "location": "مراكش - الداوديات",
        "price": "1,800 درهم/شهر",
        "bedrooms": 1,
        "area": "35م²",
        "desc": "استوديو للطلبة قريب من كلية السملالية"
    },
    {
        "id": 97,
        "type": "شقة للكراء",
        "location": "مراكش - ماجوريل",
        "price": "7,500 درهم/شهر",
        "bedrooms": 2,
        "area": "90م²",
        "desc": "شقة مفروشة بأثاث عصري ممتاز"
    },
    {
        "id": 98,
        "type": "شقة للكراء",
        "location": "مراكش - تاركة",
        "price": "4,000 درهم/شهر",
        "bedrooms": 3,
        "area": "100م²",
        "desc": "شقة عائلية فارغة بإقامة محروسة"
    },
    {
        "id": 99,
        "type": "شقة للكراء",
        "location": "مراكش - الازدهار",
        "price": "3,500 درهم/شهر",
        "bedrooms": 2,
        "area": "85م²",
        "desc": "شقة نصف مفروشة"
    },
    {
        "id": 100,
        "type": "شقة للكراء",
        "location": "مراكش - فيكتور هوغو",
        "price": "8,000 درهم/شهر",
        "bedrooms": 3,
        "area": "120م²",
        "desc": "شقة كبيرة وراقية للإيجار السنوي"
    },
    {
        "id": 101,
        "type": "شقة للكراء",
        "location": "مراكش - جليز",
        "price": "5,000 درهم/شهر",
        "bedrooms": 2,
        "area": "75م²",
        "desc": "شقة فارغة في قلب المدينة"
    },
    {
        "id": 102,
        "type": "شقة للكراء",
        "location": "مراكش - المحاميد",
        "price": "1,800 درهم/شهر",
        "bedrooms": 1,
        "area": "50م²",
        "desc": "شقة صغيرة لشخص واحد أو زوجين"
    },
    {
        "id": 103,
        "type": "استوديو للكراء",
        "location": "مراكش - جليز",
        "price": "4,000 درهم/شهر",
        "bedrooms": 1,
        "area": "40م²",
        "desc": "استوديو مفروش، إنترنت متوفر"
    },
    {
        "id": 104,
        "type": "شقة للكراء",
        "location": "مراكش - الحي الشتوي",
        "price": "15,000 درهم/شهر",
        "bedrooms": 4,
        "area": "180م²",
        "desc": "شقة VIP بخدمات فندقية"
    },
    {
        "id": 105,
        "type": "شقة للكراء",
        "location": "مراكش - مبروكة",
        "price": "3,000 درهم/شهر",
        "bedrooms": 2,
        "area": "78م²",
        "desc": "شقة مشمسة في طابق ثانٍ بإقامة جديدة"
    },
    {
        "id": 106,
        "type": "شقة للكراء",
        "location": "مراكش - ماجوريل",
        "price": "6,500 درهم/شهر",
        "bedrooms": 2,
        "area": "82م²",
        "desc": "شقة مفروشة بلمسات تقليدية جميلة"
    },
    {
        "id": 107,
        "type": "شقة للكراء",
        "location": "مراكش - الشريفية",
        "price": "4,500 درهم/شهر",
        "bedrooms": 2,
        "area": "90م²",
        "desc": "شقة في إقامة مع ملاعب ومسابح"
    },
    {
        "id": 108,
        "type": "شقة للكراء",
        "location": "مراكش - أبواب مراكش",
        "price": "2,800 درهم/شهر",
        "bedrooms": 3,
        "area": "85م²",
        "desc": "شقة فارغة واسعة للعائلات"
    },
    {
        "id": 109,
        "type": "شقة للكراء",
        "location": "مراكش - أكدال",
        "price": "6,000 درهم/شهر",
        "bedrooms": 2,
        "area": "95م²",
        "desc": "شقة مفروشة تطل على شارع محمد السادس"
    },
    {
        "id": 110,
        "type": "فيلا للكراء",
        "location": "مراكش - النخيل",
        "price": "35,000 درهم/شهر",
        "bedrooms": 5,
        "area": "1200م²",
        "desc": "فيلا فخمة للإيجار السنوي مفروشة بالكامل"
    },
    {
        "id": 111,
        "type": "فيلا للكراء",
        "location": "مراكش - تاركة",
        "price": "15,000 درهم/شهر",
        "bedrooms": 4,
        "area": "400م²",
        "desc": "فيلا فارغة للإيجار الطويل مع حديقة"
    },
    {
        "id": 112,
        "type": "رياض للكراء",
        "location": "مراكش - المدينة القديمة",
        "price": "12,000 درهم/شهر",
        "bedrooms": 4,
        "area": "150م²",
        "desc": "رياض مفروش للإيجار السنوي"
    },
    {
        "id": 113,
        "type": "مكتب للكراء",
        "location": "مراكش - جليز",
        "price": "8,000 درهم/شهر",
        "bedrooms": 0,
        "area": "70م²",
        "desc": "مكتب في مبنى تجاري بشارع محمد الخامس"
    },
    {
        "id": 114,
        "type": "فيلا للكراء",
        "location": "مراكش - طريق أوريكا",
        "price": "25,000 درهم/شهر",
        "bedrooms": 5,
        "area": "1000م²",
        "desc": "فيلا بمسبح خاص للعائلات أو موظفين أجانب"
    },
    {
        "id": 115,
        "type": "محل تجاري للكراء",
        "location": "مراكش - المسيرة",
        "price": "5,000 درهم/شهر",
        "bedrooms": 0,
        "area": "40م²",
        "desc": "محل للإيجار للأنشطة التجارية"
    },
    {
        "id": 116,
        "type": "فيلا للكراء",
        "location": "مراكش - الشريفية",
        "price": "12,000 درهم/شهر",
        "bedrooms": 3,
        "area": "300م²",
        "desc": "فيلا عصرية مفروشة للإيجار السنوي"
    },
    {
        "id": 117,
        "type": "رياض للكراء",
        "location": "مراكش - القصبة",
        "price": "18,000 درهم/شهر",
        "bedrooms": 6,
        "area": "250م²",
        "desc": "رياض كبير للإيجار لمشروع ضيافة"
    },
    {
        "id": 118,
        "type": "مكتب للكراء",
        "location": "مراكش - الحي الشتوي",
        "price": "15,000 درهم/شهر",
        "bedrooms": 0,
        "area": "100م²",
        "desc": "مكتب فاخر للشركات الكبرى"
    },
    {
        "id": 119,
        "type": "فيلا للكراء",
        "location": "مراكش - طريق أمزميز",
        "price": "30,000 درهم/شهر",
        "bedrooms": 5,
        "area": "1500م²",
        "desc": "فيلا راقية مفروشة مع خدمة إنترنت سريع"
    },
    {
        "id": 120,
        "type": "فيلا للكراء",
        "location": "مراكش - النخيل",
        "price": "45,000 درهم/شهر",
        "bedrooms": 6,
        "area": "2000م²",
        "desc": "فيلا قصراوية لكبار الشخصيات والسفراء"
    },
]

# ==================== SMART SEARCH HELPERS ====================


def _price_to_num(price_str: str) -> int:
    """Extract numeric value from price string like '1,200,000 درهم' or '5,000 درهم/شهر'."""
    nums = re.findall(r"[\d,]+", price_str)
    if not nums:
        return 0
    return int(nums[0].replace(",", ""))


def _fuzzy_score(query: str, text: str) -> float:
    if not query:
        return 0.0
    q, t = query.lower().strip(), text.lower().strip()
    if q in t:
        return 1.0
    return SequenceMatcher(None, q, t).ratio()


def _parse_budget(budget_str: str) -> int | None:
    if not budget_str:
        return None
    multipliers = {
        "مليون": 1_000_000,
        "مليار": 1_000_000_000,
        "ألف": 1_000,
        "k": 1_000,
        "m": 1_000_000
    }
    for word, mult in multipliers.items():
        if word in budget_str:
            nums = re.findall(r"[\d.]+", budget_str)
            if nums:
                return int(float(nums[0]) * mult)
    nums = re.findall(r"\d+", budget_str.replace(",", ""))
    return int(nums[0]) if nums else None


def _score_property(p: dict, location: str, property_type: str,
                    max_budget: int | None, bedrooms: int | None) -> float:
    score = 0.0
    price_num = _price_to_num(
        p["price"])  # ← always derive from string, no KeyError ever

    if location:
        score += _fuzzy_score(location, p["location"]) * 40
    if property_type:
        score += _fuzzy_score(property_type, p["type"]) * 30
    if max_budget and price_num > 0:
        if price_num <= max_budget:
            score += 20 * (1 - price_num / max_budget * 0.5)
        else:
            score -= min(20, ((price_num / max_budget) - 1) * 20)
    if bedrooms and p.get("bedrooms", 0) > 0:
        diff = abs(p["bedrooms"] - bedrooms)
        score += max(0, 10 - diff * 4)

    return score


# ==================== TOOLS ====================


@tool
def search_properties(
    location: str = "",
    property_type: str = "",
    max_budget: str = "",
    bedrooms: int = 0,
) -> str:
    """
    Search available properties by location, type, budget, and bedrooms.
    Examples:
      - location='مراكش', property_type='فيلا', max_budget='3 مليون'
      - location='جليز', bedrooms=3
      - property_type='شقة للكراء', max_budget='5000'
    """
    budget_num = _parse_budget(max_budget)
    bed = bedrooms if bedrooms > 0 else None
    has_filters = any([location, property_type, max_budget, bedrooms])

    scored = [(p, _score_property(p, location, property_type, budget_num, bed))
              for p in PROPERTIES]

    if has_filters:
        scored = [(p, s) for p, s in scored if s > 0]

    scored.sort(key=lambda x: x[1], reverse=True)
    top = scored[:5]

    if not top:
        return "مافيه عقارات مطابقة لمعاييرك دابا. جرب تبدل الموقع أو الميزانية."

    output = f"🔍 أفضل {len(top)} عقار(ات) مناسب(ة) ليك:\n\n"
    for rank, (p, s) in enumerate(top, 1):
        output += (f"{rank}. 🏠 {p['type']} — {p['location']}\n"
                   f"   💰 السعر: {p['price']}\n"
                   f"   🛏  الغرف: {p['bedrooms']} | 📐 المساحة: {p['area']}\n"
                   f"   ℹ️  {p['desc']}\n"
                   f"   ⭐ درجة التطابق: {s:.0f}/100\n\n")
    return output


@tool
def schedule_visit(property_id: int, client_name: str,
                   preferred_date: str) -> str:
    """Schedule a property visit for a client. Use this when a client wants to see a property."""
    return (f"✅ تم تسجيل الزيارة بنجاح!\n"
            f"   العميل: {client_name}\n"
            f"   العقار رقم: {property_id}\n"
            f"   التاريخ المقترح: {preferred_date}\n"
            f"سنتصل بك قريباً لتأكيد الموعد.")


@tool
def get_mortgage_estimate(property_price: int,
                          down_payment_percent: int = 20,
                          years: int = 20) -> str:
    """Calculate a rough monthly mortgage estimate for a property. Use when client asks about financing."""
    annual_rate = 0.045  # 4.5% typical Moroccan mortgage rate
    monthly_rate = annual_rate / 12
    loan = property_price * (1 - down_payment_percent / 100)
    n = years * 12
    monthly = loan * (monthly_rate *
                      (1 + monthly_rate)**n) / ((1 + monthly_rate)**n - 1)
    down = property_price * down_payment_percent / 100

    return (f"💳 تقدير التمويل العقاري:\n"
            f"   ثمن العقار: {property_price:,} درهم\n"
            f"   المقدم ({down_payment_percent}%): {down:,.0f} درهم\n"
            f"   القرض: {loan:,.0f} درهم\n"
            f"   المدة: {years} سنة\n"
            f"   القسط الشهري التقريبي: {monthly:,.0f} درهم")


# ==================== AGENT ====================

SYSTEM_PROMPT = """أنت وكيل عقاري محترف ومتخصص في السوق العقاري المغربي.
تتحدث دائماً بالدارجة المغربية بطريقة طبيعية وودودة ومهنية.

don't generate paragraphs like a chatbot. be a real agent talking to a real client.

قواعد مهمة جداً:
1. عندما تستدعي أداة search_properties وترجع نتائج، COPY AND PASTE the EXACT tool output in your response. NEVER summarize it. NEVER say "لقيت لك عقارات" without showing them.
2. ALWAYS show the full list with prices, locations, and descriptions exactly as returned by the tool.
3. لا تطلب معلومات إضافية إذا كان لديك ما يكفي للبحث. ابحث أولاً ثم اعرض النتائج.
4. إذا ذكر العميل أي معلومة (موقع، نوع، ميزانية، عدد غرف)، استخدمها فوراً للبحث.
5. بعد عرض النتائج الكاملة، يمكنك سؤال العميل إذا أراد تضييق البحث أو زيارة أحد العقارات.
6. إذا قال العميل "ماعجبونيش" أو "عندك غيرهم"، ابحث بمعايير مختلفة وقدم نتائج جديدة.

مهامك: مساعدة العملاء في إيجاد العقار المناسب، تقديم العقارات المتاحة، تنظيم الزيارات، وتقديم تقديرات التمويل.
"""

tools = [search_properties, schedule_visit, get_mortgage_estimate]

agent = create_react_agent(
    model=model,
    tools=tools,
    prompt=SYSTEM_PROMPT,
    checkpointer=MemorySaver(),
)

# ==================== RUNNER ====================


def chat(message: str, thread_id: str = "default") -> str:
    """Send a message to the agent and get a response."""
    config = {"configurable": {"thread_id": thread_id}}
    result = agent.invoke(
        {"messages": [HumanMessage(content=message)]},
        config=config,
    )
    content = result["messages"][-1].content

    # Gemini sometimes returns a list of content blocks instead of a plain string
    if isinstance(content, list):
        return "".join(
            block["text"] if isinstance(block, dict) else str(block)
            for block in content
            if not isinstance(block, dict) or block.get("type") == "text")

    return content


# ==================== DEMO ====================


def demo():
    print("=" * 55)
    print("🏠  وكيل العقارات - الدارجة المغربية  🏠")
    print("=" * 55)

    conversations = [
        ("سلام، بغيت نشري شقة في الدار البيضاء", "conv_1"),
        ("كم غادي يكون القسط الشهري لشقة بمليون درهم؟", "conv_1"),
        ("بغيت نزور العقار رقم 1، اسمي كريم", "conv_1"),
    ]

    for msg, thread in conversations:
        print(f"\n👤 العميل: {msg}")
        response = chat(msg, thread_id=thread)
        print(f"🤖 الوكيل: {response}")
        print("-" * 55)


if __name__ == "__main__":
    # Set before running:
    # export GOOGLE_API_KEY="your-gemini-api-key"
    demo()
