# -*- coding: utf-8 -*-
"""
35-Maktab Kasbga yo'naltirish va diagnostika metodikalari
1. 5-6-sinflar: «Mening qiziqishlarim va kelajakdagi kasbim» (15 ta savol)
2. 7-8-sinflar: «Qobiliyat va intilishlarni aniqlash metodikasi» (45 ta savol, 9 ta shkala)
3. 9-11-sinflar: «Qiziqishlar xaritasi» (Golomshtok - Rezapkina, 50 ta savol, 10 ta soha)
4. Qo'shimcha: «Tashkilotchilik qobiliyatini aniqlash testi» (20 ta savol)
"""

# ==============================================================================
# 1. 5-6-SINF SO'ROVNOMASI
# ==============================================================================
SURVEY_5_6 = {
    "uz": {
        "title": "«Mening qiziqishlarim va kelajakdagi kasbim»",
        "subtitle": "5–6-sinf o‘quvchilari uchun so‘rovnoma",
        "description": "Ushbu so'rovnoma sizning qiziqishlaringiz, sevimli mashg'ulotlaringiz va kelajakdagi orzularingizni aniqlashga yordam beradi. To‘g‘ri yoki noto‘g‘ri javob yo‘q, o‘z fikringizni erkin bildiring.",
        "questions": [
            {
                "id": "q1",
                "text": "1. Maktabda qaysi fanlarni o‘rganish sizga ko‘proq yoqadi?",
                "type": "checkbox",
                "options": [
                    "Matematika", "Ona tili va adabiyot", "Tarix", "Chet tili (Ingliz/Rus tili)",
                    "Informatika / IT", "Biologiya (Tabiat)", "Kimyo", "Fizika",
                    "Musiqa", "Tasviriy san’at", "Jismoniy tarbiya"
                ],
                "has_other": True
            },
            {
                "id": "q2",
                "text": "2. Bo‘sh vaqtingizda nimalar bilan shug‘ullanishni yoqtirasiz?",
                "type": "checkbox",
                "options": [
                    "Kitob o‘qish", "Sport bilan shug'ullanish", "Rasm chizish",
                    "Qo‘shiq aytish / cholg‘u chalish", "Kompyuter va IT bilan ishlash",
                    "Video montaj / dizayn", "Tabiat va hayvonlarni parvarishlash",
                    "Pazandachilik / hunar (tikish, yasash)"
                ],
                "has_other": True
            },
            {
                "id": "q3",
                "text": "3. O‘zingizda qaysi qobiliyat kuchliroq deb o‘ylaysiz?",
                "type": "checkbox",
                "options": [
                    "Hisoblash va mantiqiy fikrlash", "Chiroyli va ta'sirli gapirish",
                    "Rasm / chizma chizish", "Texnika va kompyuterga qiziqish",
                    "Musiqa va ijodkorlik", "Sport va chaqqonlik",
                    "Tashkilotchilik va boshqarish", "Boshqalarni tinglash va yordam berish",
                    "Hali aniq bilmayman"
                ]
            },
            {
                "id": "q4",
                "text": "4. Yangi narsani o‘rganishda qaysi usul sizga ko‘proq yoqadi?",
                "type": "checkbox",
                "options": [
                    "Kitob/qo'llanma o‘qib o‘rganish", "Amalda bajarib ko‘rish",
                    "Video darslar orqali", "Ustoz yoki kattalardan so‘rab",
                    "Do‘stlar bilan birgalikda", "Tajriba qilib (sinab) ko‘rish"
                ]
            },
            {
                "id": "q5",
                "text": "5. Quyidagi sohalardan qaysi biri sizga eng qiziq?",
                "type": "checkbox",
                "options": [
                    "Kompyuter / IT / Dasturlash", "Tibbiyot va shifokorlik",
                    "Texnika va muhandislik", "San’at va ijod", "Sport",
                    "Ta’lim va pedagogika (O'qituvchilik)", "Huquq va davlat xizmati",
                    "Biznes va tadbirkorlik", "Tabiat va ekologiya", "Media / jurnalistika"
                ]
            },
            {
                "id": "q6",
                "text": "6. Kelajakda qaysi kasb yoki kasblarga qiziqasiz? (Eng ko'p 3 ta)",
                "type": "text_triplet",
                "labels": ["1-kasb (Asosiy tanlovingiz)", "2-kasb (Qo'shimcha qiziqish)", "3-kasb (Yana bitta variant)"]
            },
            {
                "id": "q7",
                "text": "7. Bu kasbga qiziqishingizga nima sabab bo‘lgan?",
                "type": "checkbox",
                "options": [
                    "Bu kasb menga juda yoqadi", "Tanishim / oila a'zom shu kasbda ishlaydi",
                    "Bolaligimdan orzu qilaman", "Daromadi yaxshi deb o‘ylayman",
                    "Odamlarga yordam berishni xohlayman", "Hali aniq bilmayman"
                ],
                "has_other": True
            },
            {
                "id": "q8",
                "text": "8. Siz kelajakda ko‘proq qanday ishni bajarishni xohlaysiz?",
                "type": "checkbox",
                "options": [
                    "Odamlar bilan ishlash (muloqot, yordam)", "Kompyuter bilan ishlash",
                    "Texnika va qurilmalar bilan ishlash", "Hayvonlar va tabiat qo'ynida",
                    "Bolalar bilan ishlash (o'qitish)", "Ijodiy ishlar (rasm, dizayn, musiqa)",
                    "Mustaqil ishlash", "Katta jamoa bilan birgalikda ishlash"
                ]
            },
            {
                "id": "q9",
                "text": "9. Qaysi to‘garak yoki klub sizni ko‘proq qiziqtiradi?",
                "type": "checkbox",
                "options": [
                    "IT / Robototexnika / Dasturlash", "Xorijiy tillar (Ingliz, Rus, Nemis)",
                    "Debat va notiqlik", "Sport to'garaklari (Futbol, shaxmat, kurash)",
                    "Musiqa / Cholg'u", "Teatr va sahna san'ati",
                    "Rasm / Dizayn", "Kitobxonlik klubi", "Ekologiya va tabiatshunoslik"
                ],
                "has_other": True
            },
            {
                "id": "q10",
                "text": "10. Maktabda yangi to‘garak ochilsa, qaysi yo‘nalishda bo‘lishini xohlardingiz?",
                "type": "textarea",
                "placeholder": "Masalan: 3D dizayn, robototexnika, suzish, kiberxavfsizlik..."
            },
            {
                "id": "q11",
                "text": "11. O‘zingizni kelajakda qanday inson sifatida tasavvur qilasiz?",
                "type": "checkbox",
                "options": [
                    "Yaxshi mutaxassis", "Muvaffaqiyatli tadbirkor", "Kashfiyotchi olim",
                    "Ijodkor (san'atkor)", "Chempion sportchi", "Mas'uliyatli rahbar",
                    "Mehribon o‘qituvchi / murabbiy"
                ],
                "has_other": True
            },
            {
                "id": "q12",
                "text": "12. Sizga kasb tanlashda kimning maslahati ko‘proq ta’sir qiladi?",
                "type": "checkbox",
                "options": [
                    "Ota-onam va yaqinlarim", "O‘qituvchim", "Sinfdoshlarim va do‘stlarim",
                    "Maktab maslahatchisi", "Psixolog", "O‘zim mustaqil tanlayman"
                ],
                "has_other": True
            },
            {
                "id": "q13",
                "text": "13. Kelajakdagi kasbingiz haqida ko'proq ma’lumot olishni xohlaysizmi?",
                "type": "radio_with_followup",
                "options": ["Ha", "Yo‘q", "Hali o‘ylab ko‘rmaganman"],
                "followup_prompt": "Agar «Ha» bo‘lsa, aynan qaysi kasb haqida ma'lumot olishni xohlaysiz?"
            },
            {
                "id": "q14",
                "text": "14. Siz maktab hayotini yaxshilash uchun qanday yangi g‘oya yoki tashabbus taklif qilgan bo‘lardingiz?",
                "type": "textarea",
                "placeholder": "O'z taklif va fikrlaringizni yozing..."
            },
            {
                "id": "q15",
                "text": "15. O‘zingiz haqingizda biz bilishimiz kerak deb hisoblagan boshqa qiziqishingiz, qobiliyatingiz yoki orzuingiz bormi?",
                "type": "textarea",
                "placeholder": "Qo'shimcha fikr va orzularingiz..."
            }
        ]
    },
    "ru": {
        "title": "«Мои интересы и будущая профессия»",
        "subtitle": "Анкета для учащихся 5–6 классов",
        "description": "Этот опрос поможет выявить ваши интересы, способности, любимые занятия и профессиональные склонности. Правильных или неправильных ответов нет, отвечайте искренне.",
        "questions": [
            {
                "id": "q1",
                "text": "1. Какие предметы в школе вам больше всего нравится изучать?",
                "type": "checkbox",
                "options": [
                    "Математика", "Родной язык и литература", "История", "Иностранные языки",
                    "Информатика / IT", "Биология (Природоведение)", "Химия", "Физика",
                    "Музыка", "Изобразительное искусство", "Физкультура"
                ],
                "has_other": True
            },
            {
                "id": "q2",
                "text": "2. Чем вы любите заниматься в свободное время?",
                "type": "checkbox",
                "options": [
                    "Чтение книг", "Занятия спортом", "Рисование",
                    "Пение / игра на музыкальных инструментах", "Работа на компьютере и IT",
                    "Видеомонтаж / графический дизайн", "Природа и домашние животные",
                    "Кулинария / рукоделие (шитье, поделки)"
                ],
                "has_other": True
            },
            {
                "id": "q3",
                "text": "3. Какие способности, по вашему мнению, у вас развиты сильнее?",
                "type": "checkbox",
                "options": [
                    "Счет и логическое мышление", "Грамотная и выразительная речь",
                    "Рисование / черчение", "Интерес к технике и компьютерам",
                    "Музыка и творчество", "Спорт и ловкость",
                    "Организаторские способности и лидерство", "Умение слушать и помогать людям",
                    "Пока точно не знаю"
                ]
            },
            {
                "id": "q4",
                "text": "4. Какой способ изучения нового вам нравится больше всего?",
                "type": "checkbox",
                "options": [
                    "Чтение книг / инструкций", "Практическое выполнение",
                    "Просмотр видеоуроков", "Спросить у учителя или старших",
                    "Вместе с друзьями", "Проводить опыты и эксперименты"
                ]
            },
            {
                "id": "q5",
                "text": "5. Какая из следующих сфер вам наиболее интересна?",
                "type": "checkbox",
                "options": [
                    "Компьютеры / IT / Программирование", "Медицина и здоровье",
                    "Техника и инженерия", "Искусство и творчество", "Спорт",
                    "Образование и педагогика", "Юриспруденция и госслужба",
                    "Бизнес и предпринимательство", "Природа и экология", "Медиа / журналистика"
                ]
            },
            {
                "id": "q6",
                "text": "6. Какие профессии вас привлекают в будущем? (До 3 вариантов)",
                "type": "text_triplet",
                "labels": ["1-я профессия (Основной выбор)", "2-я профессия (Дополнительный интерес)", "3-я профессия (Запасной вариант)"]
            },
            {
                "id": "q7",
                "text": "7. Что повлияло на ваш интерес к этой профессии?",
                "type": "checkbox",
                "options": [
                    "Мне очень нравится эта работа", "Знакомый или родственник работает в этой сфере",
                    "Мечтаю об этом с детства", "Считаю, что это высокооплачиваемая профессия",
                    "Хочу помогать людям", "Пока точно не знаю"
                ],
                "has_other": True
            },
            {
                "id": "q8",
                "text": "8. Какую работу вы предпочли бы выполнять в будущем?",
                "type": "checkbox",
                "options": [
                    "Работа с людьми (общение, помощь)", "Работа с компьютером",
                    "Работа с техникой и приборами", "На природе и с животными",
                    "Работа с детьми (обучение)", "Творческая работа (дизайн, музыка, сцена)",
                    "Самостоятельная работа", "Работа в большой дружной команде"
                ]
            },
            {
                "id": "q9",
                "text": "9. Какой кружок или клуб вас больше всего интересует?",
                "type": "checkbox",
                "options": [
                    "IT / Робототехника / Программирование", "Иностранные языки",
                    "Дебаты и ораторское искусство", "Спортивные секции",
                    "Музыка / инструменты", "Театр и сценическое искусство",
                    "Рисование / дизайн", "Клуб книголюбов", "Экология и биология"
                ],
                "has_other": True
            },
            {
                "id": "q10",
                "text": "10. Если в школе откроется новый кружок, в каком направлении вы хотели бы его видеть?",
                "type": "textarea",
                "placeholder": "Например: 3D-моделирование, робототехника, плавание, кибербезопасность..."
            },
            {
                "id": "q11",
                "text": "11. Каким человеком вы видите себя в будущем?",
                "type": "checkbox",
                "options": [
                    "Высококлассный специалист", "Успешный предприниматель", "Ученый-исследователь",
                    "Творческая личность", "Спортсмен-чемпион", "Ответственный руководитель",
                    "Заботливый учитель / наставник"
                ],
                "has_other": True
            },
            {
                "id": "q12",
                "text": "12. Чей совет больше всего влияет на ваш выбор профессии?",
                "type": "checkbox",
                "options": [
                    "Родители и близкие", "Учитель", "Одноклассники и друзья",
                    "Школьный консультант", "Психолог", "Выбираю полностью самостоятельно"
                ],
                "has_other": True
            },
            {
                "id": "q13",
                "text": "13. Хотите ли вы получить больше информации о своей будущей профессии?",
                "type": "radio_with_followup",
                "options": ["Да", "Нет", "Пока не думал(а) об этом"],
                "followup_prompt": "Если «Да», то о какой именно профессии вы хотите узнать больше?"
            },
            {
                "id": "q14",
                "text": "14. Какую идею или инициативу вы предложили бы для улучшения школьной жизни?",
                "type": "textarea",
                "placeholder": "Ваши идеи и предложения..."
            },
            {
                "id": "q15",
                "text": "15. Есть ли у вас другие увлечения, таланты или мечты, о которых нам следует знать?",
                "type": "textarea",
                "placeholder": "Дополнительные мысли и пожелания..."
            }
        ]
    }
}

# ==============================================================================
# 2. 7-8-SINF: QOBILIYAT VA INTILISHLARNI ANIQLASH METODIKASI (45 TA SAVOL)
# ==============================================================================
SURVEY_7_8 = {
    "uz": {
        "title": "«O‘quvchilarning qiziqishlari, qobiliyatlari va intilishlarini aniqlash metodikasi»",
        "subtitle": "7–8-sinf o‘quvchilari uchun diagnostika",
        "description": "Ushbu metodika 9 ta soha bo‘yicha sizning yetakchi qobiliyatlaringiz va qiziqishlaringizni aniqlaydi. 45 ta savolning har biriga o‘zingizga to‘g‘ri kelsa «Ha», to‘g‘ri kelmasa «Yo‘q» tugmasini tanlang.",
        "scales": [
            {"id": "sport", "name": "Жисмоний (спорт)", "items": [1, 10, 19, 28, 37]},
            {"id": "tashkilot", "name": "Ташкилотчилик", "items": [2, 11, 20, 29, 38]},
            {"id": "matematik", "name": "Математик", "items": [3, 12, 21, 30, 39]},
            {"id": "texnika", "name": "Конструкторлик-техника", "items": [4, 13, 22, 31, 40]},
            {"id": "artistik", "name": "Тасвирий (артистик / саҳна)", "items": [5, 14, 23, 32, 41]},
            {"id": "kommunikativ", "name": "Коммуникатив (мулоқот)", "items": [6, 15, 24, 33, 42]},
            {"id": "musiqiy", "name": "Мусиқий", "items": [7, 16, 25, 34, 43]},
            {"id": "tasviriy", "name": "Бадиий-тасвирий (санъат)", "items": [8, 17, 26, 35, 44]},
            {"id": "filologik", "name": "Филологик (тил, адабиёт, журналистика)", "items": [9, 18, 27, 36, 45]}
        ],
        "groups": [
            {
                "title": "Болалигингдан сен жуда яхши кўриб бажарадиган ишларинг:",
                "start": 1,
                "end": 9
            },
            {
                "title": "Сенга ҳозир ёқадими:",
                "start": 10,
                "end": 18
            },
            {
                "title": "Катта қониқиш ҳосил қиласанми:",
                "start": 19,
                "end": 27
            },
            {
                "title": "Сени кўпроқ жалб этади:",
                "start": 28,
                "end": 36
            },
            {
                "title": "Сенга узоқ вақт шуғулланиш ёқади:",
                "start": 37,
                "end": 45
            }
        ],
        "questions": [
            "Узоқ вақт ҳаракатли ўйинлар ўйнаш?",
            "Ҳар-хил ўйинларни ўйлаб топиш?",
            "Шашка, шахмат ўйнаш?",
            "Ичида нима борлигини билиш учун ўйинчоқларни синдириш / очиб кўриш?",
            "Шеър ўқиш ёки қўшиқ айтиш?",
            "Бегоналар билан гаплашиш ёки саволлар бериш?",
            "Мусиқа тинглаш ва рақсга тушиш?",
            "Расм чизиш ёки бошқалар чизаётганда томоша қилиш?",
            "Эртак тинглаш, ўзинг эртак ёки воқеалар ўйлаб топиш?",
            "Жисмоний тарбия дарсларида ёки спорт мактабларида, сексияларда шуғулланиш?",
            "Ўз ихтиёринг билан бирор бир ишни ташкиллаштириш масъулиятини олиш?",
            "Математик вазифаларни ечишда болаларга ёрдам бериш?",
            "Буюк кашфиётлар ҳақида ўқиш?",
            "Бадиий ҳаваскорлик тўгаракларида қатнашиш?",
            "Муаммоларни ҳал қилишда одамларга ёрдам бериш?",
            "Санъат ҳақида бирор бир янгиликларни ўқиш ёки билиш?",
            "Тасвирий санъат тўгаракларида шуғулланиш?",
            "Эркин мавзуда иншо ёзиш?",
            "Спорт мусобақаларида қатнашишдан?",
            "Одамларга ишни тақсимлаб бериш малаканг борлигидан?",
            "Мураккаб математик масалаларни еча олишингдан?",
            "Электр ва радио асбобларни тузата олишингдан?",
            "Саҳнада ўзингни эркин тута олишингдан?",
            "Одамлар билан мулоқот қилишингдан?",
            "Янги мусиқий асбоблар ва мусиқа асарлари билан танишлигингдан?",
            "Бадиий кўргазмаларга ташриф буюрганингда?",
            "Бирор бир кўрган ёки ўқиган воқеалардан?",
            "Узоқ муддатли жисмоний машқлар?",
            "Сенинг ташаббусинг ва қатъиятлигинг талаб қилинадиган ишлар?",
            "Математик топишмоқларни ечиш?",
            "Бирор-бир буюмнинг моделини тайёрлаш?",
            "Спектаклни саҳналаштиришда иштирок этиш?",
            "Одамларга ёрдам бериш, ҳамдард бўлиш?",
            "Бирор-бир мусиқа асбобини чалиш?",
            "Қалам ёки бўёқларда расм чизиш?",
            "Шеър, ҳикоя ёзиш ёки кундалик юритиш?",
            "Спорт ёки жисмоний меҳнат билан?",
            "Ғайрат билан меҳнат қилиш?",
            "Чизмачилик билан шуғулланиш ёки шахмат ўйнаш?",
            "Механизм ва асбоблар билан ишлаш?",
            "Беморлар, ўзингдан кичиклар ҳақида ғамхўрлик қилиш?",
            "Севимли китоб қаҳрамонлари тақдири ҳақида ўйлаш?",
            "Мусиқий асарларни ижро этиш?",
            "Расм чизиш, лойдан бирор бир нарса ясаш?",
            "Маъруза қилишга тайёрланиш?"
        ]
    },
    "ru": {
        "title": "«Методика определения интересов, способностей и стремлений учащихся»",
        "subtitle": "Диагностика для учащихся 7–8 классов",
        "description": "Методика позволяет определить ведущие интересы и способности по 9 шкалам. Отвечайте на каждый из 45 вопросов «Да» или «Нет».",
        "scales": [
            {"id": "sport", "name": "Физические (спортивные)", "items": [1, 10, 19, 28, 37]},
            {"id": "tashkilot", "name": "Организаторские", "items": [2, 11, 20, 29, 38]},
            {"id": "matematik", "name": "Математические", "items": [3, 12, 21, 30, 39]},
            {"id": "texnika", "name": "Конструирование и техника", "items": [4, 13, 22, 31, 40]},
            {"id": "artistik", "name": "Изобразительный (артистический)", "items": [5, 14, 23, 32, 41]},
            {"id": "kommunikativ", "name": "Коммуникативный (общение)", "items": [6, 15, 24, 33, 42]},
            {"id": "musiqiy", "name": "Музыкальный", "items": [7, 16, 25, 34, 43]},
            {"id": "tasviriy", "name": "Художественный (изоискусство)", "items": [8, 17, 26, 35, 44]},
            {"id": "filologik", "name": "Филологический (литература, журналистика)", "items": [9, 18, 27, 36, 45]}
        ],
        "groups": [
            {"title": "Чем вы любили заниматься в детстве:", "start": 1, "end": 9},
            {"title": "Тебе это нравится сейчас:", "start": 10, "end": 18},
            {"title": "Вы очень довольны:", "start": 19, "end": 27},
            {"title": "Что вас привлекает больше всего:", "start": 28, "end": 36},
            {"title": "Вас долго привлекает:", "start": 37, "end": 45}
        ],
        "questions": [
            "Играть подвижные игры?",
            "Придумывать разные игры?",
            "Играть в шахматы, шашки?",
            "Разбивать игрушки, чтобы узнать, что внутри?",
            "Читать стихи или петь?",
            "Разговаривать с незнакомцами или задавать вопросы?",
            "Слушать музыку и танцевать?",
            "Рисовать или смотреть, как рисуют другие?",
            "Слушать сказку, придумывать свою сказку или рассказ?",
            "Заниматься в классах физкультуры или спортшколах, секциях?",
            "Взять на себя ответственность за организацию дела на общественных началах?",
            "Помогать детям решать математические задачи?",
            "Читать о великих открытиях?",
            "Участвовать в кружках художественной самодеятельности?",
            "Помогать людям решать проблемы?",
            "Читать или узнавать новости об искусстве?",
            "Заниматься в кружках изящных искусств?",
            "Писать эссе на свободную тему?",
            "От участия в спортивных соревнованиях?",
            "Потому что у вас есть возможность распределять работу людям?",
            "Можешь решать сложные математические задачи?",
            "Можешь отремонтировать электрическое и радиооборудование?",
            "От способности чувствовать себя свободно на сцене?",
            "От общения с людьми?",
            "Много знаешь о музыкальных инструментах и музыкальных произведениях?",
            "От посещения художественных выставок?",
            "От разных событиях которые видели или читали?",
            "Долгосрочные физические упражнения?",
            "Вещи, требующие вашей инициативы и настойчивости?",
            "Решать математические головоломки?",
            "Изготовление модели предмета?",
            "Участвовать в постановке спектакля?",
            "Помогать людям, сопереживать?",
            "Играть на каком-нибудь музыкальном инструменте?",
            "Рисование карандашами или красками?",
            "Поэзия, написание рассказов или ведение дневника?",
            "Спорт или физический труд?",
            "Работать усердно с энтузиазмом?",
            "Рисовать или играть в шахматы?",
            "Работать с механизмами и инструментами?",
            "Забота о малышах и уход за больными?",
            "Задумываться о судьбах любимых книжных героев?",
            "Исполнять музыкальные произведения?",
            "Рисование, лепка из глины?",
            "Подготовка к выступлению с докладом?"
        ]
    }
}

# ==============================================================================
# 3. 9-11-SINF: QIZIQISHLAR XARITASI (GOLOMSHTOK - REZAPKINA, 50 TA SAVOL)
# ==============================================================================
SURVEY_9_11 = {
    "uz": {
        "title": "«Qiziqishlar xaritasi» metodikasi",
        "subtitle": "9–10–11-sinf o‘quvchilari uchun kasbiy qiziqishlar diagnostikasi",
        "description": "A.E. Golomshtokning G.V. Rezapkina tomonidan modifikatsiya qilingan mashhur metodikasi. 10 ta kasbiy soha bo‘yicha sizning intilishingizni baholaydi. Har bir fikrga «Ha» yoki «Yo‘q» deb javob bering.",
        "spheres": [
            {"id": "fiz_mat", "name": "Физика ва математика", "items": [1, 11, 21, 31, 41]},
            {"id": "kim_bio", "name": "Кимё ва биология", "items": [2, 12, 22, 32, 42]},
            {"id": "radio_el", "name": "Радиотехника ва электроника", "items": [3, 13, 23, 33, 43]},
            {"id": "mex_kon", "name": "Механика ва конструкторлик", "items": [4, 14, 24, 34, 44]},
            {"id": "geo_geol", "name": "География ва геология", "items": [5, 15, 25, 35, 45]},
            {"id": "adab_san", "name": "Адабиёт ва санъат", "items": [6, 16, 26, 36, 46]},
            {"id": "tar_siyos", "name": "Тарих ва сиёсат", "items": [7, 17, 27, 37, 47]},
            {"id": "ped_tib", "name": "Педагогика ва тиббиёт", "items": [8, 18, 28, 38, 48]},
            {"id": "biz_uy", "name": "Тадбиркорлик ва уй рўзғор", "items": [9, 19, 29, 39, 49]},
            {"id": "sport_harbiy", "name": "Спорт ва ҳарбий соҳа", "items": [10, 20, 30, 40, 50]}
        ],
        "questions": [
            "Математика ва физика соҳасидаги янгиликлардан хабардор бўлиш.",
            "Ўсимликлар ва ҳайвонлар ҳаёти ҳақида кўрсатувлар томоша қилиш.",
            "Электр асбоб-ускуналарининг тузилишига қизиқиш.",
            "Техникага оид илмий-оммабоп журналларни ўқиш.",
            "Турли миллатга мансуб инсонларнинг турмуш тарзига қизиқиш.",
            "Театр, концерт ва кўргазмаларга бориб туриш.",
            "Мамлакатимиз ва чет давлатлардаги воқеа-ҳодисаларга қизиқиш.",
            "Тиббиёт ходимларининг фаолиятига қизиқиш.",
            "Уйда, мактабда ва синфда саранжом-саришталикка риоя қилиш.",
            "Уруш воқеалари ва жанглар тарихи ҳақида китоблар ўқиш, фильмлар томоша қилиш.",
            "Математик масалаларни ечиш.",
            "Кимё ва биология соҳасидаги янгиликларга қизиқиш.",
            "Маиший электротехника асбобларини таъмирлаш.",
            "Фан-техника ютуқларига оид кўргазмаларга бориб туриш.",
            "Ўрганилмаган жойларда бўлиш, саёҳатларга бориш.",
            "Янги китоблар, фильмлар ҳамда концертлар ҳақидаги мақолаларни ўқиш.",
            "Мактабдаги жамоат ишларида фаол қатнашиш.",
            "Синфдошларига ўқув материалларини ўзлаштиришга кўмаклашиш.",
            "Уй рўзғор ишларини мустақил бажариш.",
            "Кун тартибига, соғлом турмуш тарзига риоя қилиш.",
            "Физикадан тажриба ўтказиш.",
            "Ҳайвонларни ва ўсимликларни парвариш қилиш.",
            "Электроника ва радиотехника соҳасига оид адабиётларни ўқиш.",
            "Соат механизмларини ва велосипед қисмларини йиғиш ва таъмирлаш.",
            "Тошлар ва минераллардан коллекция тўплаш.",
            "Шеър, эртак ва ҳикоялар ёзиш, кундалик юритиш.",
            "Таниқли сиёсатшунослар ҳаёти ва ижодига қизиқиш, тарихий китобларни ўқиш.",
            "Кичик ёшдаги ўқувчиларни дарс тайёрлашига ёрдамлашиш, улар билан ўйнаш.",
            "Озиқ-овқат маҳсулотларини сотиб олиш, сарф-харажатларни ҳисоблаш.",
            "Ҳарбий ўйинлар ўйнаш.",
            "Дарсдан ташқари физика ва математика фанларидан қўшимча шуғулланиш.",
            "Табиат ҳодисаларини тушунтириш ва изоҳлаш.",
            "Компьютер қисмларини йиғиш ва таъмирлаш.",
            "Компьютерда чизмалар, схемалар, графиклар чизиш.",
            "Геологик ва географик экспедицияларда иштирок этиш.",
            "Ўқиган китоблари ва кўрган фильмлар ҳақида дўстларига сўзлаб бериш.",
            "Мамлакатимиз ва чет давлатлардаги сиёсий воқеаларни кузатиш.",
            "Ёш болалар ва яқинлари бемор бўлганда уларни парваришлаш.",
            "Даромад келтирадиган бизнес-режаларни тузиш.",
            "Жисмоний тарбия ва спорт билан шуғулланиш.",
            "Физика-математика фан олимпиадаларида қатнашиш.",
            "Кимё ва биологиядан лаборатория тажрибаларини ўтказиш.",
            "Электр асбоб-ускуналарнинг ишлаш тартибини тушуниш.",
            "Турли механизмларнинг қай йўсинда ишлашига қизиқиш.",
            "Географик ва геологик хариталар билан ишлаш.",
            "Саҳна кўринишлари ва концертларда иштирок этиш.",
            "Бошқа давлатларнинг сиёсати ва иқтисодиётига қизиқиш.",
            "Инсонларнинг хулқ-атвори ва организмининг тузилишини ўрганиш.",
            "Оила бюджетини режалаштиришда иштирок этиш.",
            "Спорт мусобақаларида қатнашиш."
        ]
    },
    "ru": {
        "title": "«Карта интересов» (по А.Е. Голомштоку, мод. Г.В. Резапкиной)",
        "subtitle": "Диагностика профессиональных интересов для учащихся 9–10–11 классов",
        "description": "Методика исследует ваши склонности по 10 профессиональным направлениям. На каждый из 50 вопросов ответьте «Да» или «Нет».",
        "spheres": [
            {"id": "fiz_mat", "name": "Физика и математика", "items": [1, 11, 21, 31, 41]},
            {"id": "kim_bio", "name": "Химия и биология", "items": [2, 12, 22, 32, 42]},
            {"id": "radio_el", "name": "Радиотехника и электроника", "items": [3, 13, 23, 33, 43]},
            {"id": "mex_kon", "name": "Механика и конструирование", "items": [4, 14, 24, 34, 44]},
            {"id": "geo_geol", "name": "География и геология", "items": [5, 15, 25, 35, 45]},
            {"id": "adab_san", "name": "Литература и искусство", "items": [6, 16, 26, 36, 46]},
            {"id": "tar_siyos", "name": "История и политика", "items": [7, 17, 27, 37, 47]},
            {"id": "ped_tib", "name": "Педагогика и медицина", "items": [8, 18, 28, 38, 48]},
            {"id": "biz_uy", "name": "Предпринимательство и домоводство", "items": [9, 19, 29, 39, 49]},
            {"id": "sport_harbiy", "name": "Спорт и военное дело", "items": [10, 20, 30, 40, 50]}
        ],
        "questions": [
            "Узнавать об открытиях в области физики и математики.",
            "Смотреть передачи о жизни растений и животных.",
            "Выяснять устройство электроприборов.",
            "Читать научно-популярные технические журналы.",
            "Смотреть передачи о жизни людей в разных странах.",
            "Бывать на выставках, концертах, спектаклях.",
            "Обсуждать и анализировать события в стране и за рубежом.",
            "Наблюдать за работой медсестры, врача.",
            "Создавать уют и порядок в доме, классе, школе.",
            "Читать книги и смотреть фильмы о войнах и сражениях.",
            "Заниматься математическими расчетами и вычислениями.",
            "Узнавать об открытиях в области химии и биологии.",
            "Ремонтировать бытовые электроприборы.",
            "Посещать технические выставки, знакомиться с достижениями науки и техники.",
            "Ходить в походы, бывать в новых неизведанных местах.",
            "Читать отзывы и статьи о книгах, фильмах, концертах.",
            "Участвовать в общественной жизни школы, города.",
            "Объяснять одноклассникам учебный материал.",
            "Самостоятельно выполнять работу по хозяйству.",
            "Соблюдать режим, вести здоровый образ жизни.",
            "Проводить опыты по физике.",
            "Ухаживать за животными и растениями.",
            "Читать статьи об электронике и радиотехнике.",
            "Собирать и ремонтировать часы, замки, велосипеды.",
            "Коллекционировать камни, минералы.",
            "Вести дневник, сочинять стихи и рассказы.",
            "Читать биографии известных политиков, книги по истории.",
            "Играть с детьми, помогать делать уроки младшим.",
            "Закупать продукты для дома, вести учет расходов.",
            "Участвовать в военных играх, походах.",
            "Заниматься физикой и математикой сверх школьной программы.",
            "Замечать и объяснять природные явления.",
            "Собирать и ремонтировать компьютеры.",
            "Строить чертежи, схемы, графики, в том числе на компьютере.",
            "Участвовать в географических, геологических экспедициях.",
            "Рассказывать друзьям о прочитанных книгах, увиденных фильмах и спектаклях.",
            "Следить за политической жизнью в стране и за рубежом.",
            "Ухаживать за маленькими детьми или близкими, если они заболели.",
            "Искать и находить способы зарабатывания денег.",
            "Заниматься физической культурой и спортом.",
            "Участвовать в физико-математических олимпиадах.",
            "Выполнять лабораторные опыты по химии и биологии.",
            "Разбираться в принципах работы электроприборов.",
            "Разбираться в принципах работы различных механизмов.",
            "«Читать» географические и геологические карты.",
            "Участвовать в спектаклях, концертах.",
            "Изучать политику и экономику других стран.",
            "Изучать причины поведения людей, строение человеческого организма.",
            "Вкладывать заработанные деньги в домашний бюджет.",
            "Участвовать в спортивных соревнованиях."
        ]
    }
}

# ==============================================================================
# 4. TASHKILOTCHILIK QOBILIYATINI ANIQLASH TESTI (20 TA SAVOL)
# ==============================================================================
SURVEY_TASHKILOT = {
    "uz": {
        "title": "«Tashkilotchilik qobiliyatini aniqlash testi»",
        "subtitle": "Liderlik va jamoani boshqarish salohiyati",
        "description": "Savollarni diqqat bilan o‘qing, uzoq o‘ylamasdan o‘zingizga mos bo‘lgan javobni tanlang: A) Ha, B) Ba’zan, C) Yo‘q.",
        "questions": [
            "O‘rtoqlaringiz har doim ham sizning fikringizga qo‘shilishadimi?",
            "Turli vaziyatlardan chiqish yo‘llarini topa olasizmi?",
            "Sizga jamoatchilik ishlari bilan shug‘ullanish yoqadimi?",
            "Agar maqsadlaringizni amalga oshirish yo‘lida qiyinchilikka duch kelsangiz ulardan voz kechasizmi?",
            "Siz har xil o‘yin va xursandchilik tadbirlarini o‘ylab topishni va tashkil etishni yoqtirasizmi?",
            "Siz ko‘p hollarda bugun bajarilishi kerak bo‘lgan ishlarni boshqa kunga ko‘chirasizmi?",
            "Siz o‘rtoqlaringiz uchun turli qiziqarli tadbirlarni tashkil eta olasizmi?",
            "Sizni o‘rtoqlaringiz bilan kelishmay qolishingiz ularning bergan va’dalarini bajarmasligi oqibatida bo‘lmasligi rostmi?",
            "Siz ko‘p hollarda topshiriqlarni bajarishda tashabbus ko‘rsatasizmi?",
            "Notanish vaziyatlarga yaxshi ko‘nikib ketmasligingiz rostmi?",
            "Boshlagan ishingizni tugata olmasangiz asabiylashasizmi?",
            "O‘rtoqlaringiz bilan ko‘p muloqot sizni charchatib qo‘yishi rostmi?",
            "O‘rtoqlaringiz uchun ularga tegishli muammolarni yechishda ko‘pincha tashabbus ko‘rsatasizmi?",
            "O‘zingizni haqligingizni isbotlash siz uchun unchalik muhim emasmi?",
            "Maktabdagi (sinfdagi) jamoat ishlarida qatnashasizmi?",
            "Agar do‘stlaringiz tomonidan Sizning fikringiz yoki qaroringiz qabul qilinmasa ularni himoya qilishga harakat qilmasligingiz rostmi?",
            "O‘rtoqlaringiz uchun har xil tadbirlarni tashkil etish uchun chin dildan kirishasizmi?",
            "Uchrashuvlarga siz ko‘pincha kechikasizmi?",
            "Siz ko‘pincha hammaning diqqat markazida bo‘lasizmi?",
            "Siz o‘zingizni notanish jamoada noqulay tutishingiz rostmi?"
        ]
    },
    "ru": {
        "title": "«Тест на определение организаторских способностей»",
        "subtitle": "Диагностика лидерских качеств и навыков управления",
        "description": "Внимательно прочитайте вопросы и выберите наиболее подходящий вариант: A) Да, B) Иногда, C) Нет.",
        "questions": [
            "Ваши друзья с вами всегда согласны?",
            "Можете ли вы найти выход из сложных ситуаций?",
            "Вам нравится общественная работа?",
            "Если у вас возникнут трудности с достижением ваших целей, откажетесь ли вы от них?",
            "Вам нравится организовывать различные игры и веселые мероприятия?",
            "Часто ли вы переносите работу, которую необходимо выполнить сегодня?",
            "Можете ли вы организовать различные интересные мероприятия для своих друзей?",
            "Правда ли, что ваше несогласие с друзьями не связано с тем, что они не выполняют своих обещаний?",
            "Вы часто проявляете инициативу при выполнении заданий?",
            "Правда ли, что вы с трудом привыкаете к незнакомым ситуациям?",
            "Вы расстраиваетесь, если не можете закончить начатое дело?",
            "Правда ли, что длительное общение с друзьями может быть утомительным?",
            "Вы часто проявляете инициативу для решения проблем своих друзей?",
            "Разве вам не важно доказать, что вы правы?",
            "Участвуете ли вы в школьных (классных) общественных делах?",
            "Правда ли, что вы не пытаетесь отстаивать свое мнение, если друзья с вами не согласны?",
            "Вы с искренним желанием беретесь за организацию различных мероприятий для друзей?",
            "Вы часто опаздываете на встречи?",
            "Вы часто находитесь в центре внимания?",
            "Правда ли, что вы чувствуете себя некомфортно в незнакомом коллективе?"
        ]
    }
}

# ==============================================================================
# NATIJALARNI HISOBLASH (SKORING) VA TAVSIYALAR
# ==============================================================================

def score_test_7_8(answers, lang="uz"):
    """
    answers: dict where key is "1".."45" and value is True/False ("ha"/"yoq")
    Returns: dict of scores per scale, top scale, and recommendations
    """
    spec = SURVEY_7_8["uz" if lang == "uz" else "ru"]
    scales = spec["scales"]
    scores = {}
    top_scale = None
    max_score = -1

    for sc in scales:
        cnt = 0
        for item_idx in sc["items"]:
            ans = answers.get(str(item_idx))
            if ans is True or ans == "ha" or ans == "yes" or ans == "да":
                cnt += 1
        scores[sc["id"]] = {
            "name": sc["name"],
            "score": cnt,
            "max": 5,
            "percent": round((cnt / 5) * 100)
        }
        if cnt > max_score:
            max_score = cnt
            top_scale = sc

    # Tavsiya
    rec_map_uz = {
        "sport": "Jismoniy tarbiya, sport seksiyalari (futbol, shaxmat, kurash), murabbiylik va harbiy yo‘nalish.",
        "tashkilot": "Liderlik, tadbirkorlik, jamoatchilik ishlari, boshqaruv va loyihalarni boshqarish.",
        "matematik": "Aniq fanlar, dasturlash (IT), iqtisodiyot, matematika to‘garagi, mantiqiy olimpiadalar.",
        "texnika": "Robototexnika, modellashtirish, elektrotexnika, muhandislik to‘garaklari.",
        "artistik": "Teatr to‘garagi, notiqlik, sahna san’ati, teleboshlovchilik.",
        "kommunikativ": "Psixologiya, pedagogika, chet tillari, debat klubi, ijtimoiy soha.",
        "musiqiy": "Musiqa maktabi, vokal, cholg‘u asboblari, ovoz rejissyorligi.",
        "tasviriy": "Tasviriy san’at, arxitektura, grafik dizayn, amaliy san’at.",
        "filologik": "Ona tili va adabiyot, xorijiy tillar, jurnalistika, ijodiy yozuvchilik klubi."
    }
    rec = rec_map_uz.get(top_scale["id"] if top_scale else "matematik", "Umumiy qobiliyatlarni rivojlantirish to‘garaklari.")

    return {
        "type": "7-8-sinf",
        "scores": scores,
        "top_id": top_scale["id"] if top_scale else "",
        "top_name": top_scale["name"] if top_scale else "",
        "top_score": max_score,
        "recommendation": rec
    }

def score_test_9_11(answers, lang="uz"):
    """
    answers: dict where key is "1".."50" and value is True/False ("ha"/"yoq")
    """
    spec = SURVEY_9_11["uz" if lang == "uz" else "ru"]
    spheres = spec["spheres"]
    scores = {}
    sorted_spheres = []

    for sp in spheres:
        cnt = 0
        for item_idx in sp["items"]:
            ans = answers.get(str(item_idx))
            if ans is True or ans == "ha" or ans == "yes" or ans == "да":
                cnt += 1
        level = "Sust"
        if cnt >= 4:
            level = "Yorqin ifodalangan"
        elif cnt >= 3:
            level = "O‘rtacha"

        item_res = {
            "id": sp["id"],
            "name": sp["name"],
            "score": cnt,
            "max": 5,
            "percent": round((cnt / 5) * 100),
            "level": level
        }
        scores[sp["id"]] = item_res
        sorted_spheres.append(item_res)

    sorted_spheres.sort(key=lambda x: x["score"], reverse=True)
    top1 = sorted_spheres[0] if sorted_spheres else None
    top2 = sorted_spheres[1] if len(sorted_spheres) > 1 else None

    # Tavsiya kasblar
    kasb_map = {
        "fiz_mat": "Dasturchi, IT muhandis, ma'lumotlar tahlilchisi (Data Scientist), matematik, moliya tahlilchisi.",
        "kim_bio": "Shifokor, farmatsevt, biotexnolog, agronom, ekolog, genetik.",
        "radio_el": "Elektronika muhandisi, telekommunikatsiya mutaxassisi, robototexnik, tizim ma'muri.",
        "mex_kon": "Muhandis-konstruktor, arxitektor, mexanik, texnolog, 3D modellashtiruvchi.",
        "geo_geol": "Geolog, kartograf, meteorolog, sayyohlik/turizm menejeri, gidrograf.",
        "adab_san": "Jurnalist, yozuvchi, tarjimon, aktyor, rejissyor, grafik dizayner, san'atshunos.",
        "tar_siyos": "Huquqshunos, diplomat, siyosatshunos, tarixchi, davlat boshqaruvi mutaxassisi.",
        "ped_tib": "O‘qituvchi, psixolog, defektolog, shifokor, tarbiyachi, ijtimoiy xodim.",
        "biz_uy": "Tadbirkor, marketolog, menejer, buxgalter, iqtisodchi, restavrator/oshpaz.",
        "sport_harbiy": "Professional sportchi, harbiy ofitser, sport murabbiyi, bojxona xodimi, favqulodda vaziyatlar xodimi."
    }

    rec = ""
    if top1:
        rec += f"Yetakchi soha: {top1['name']} ({top1['score']}/5 ball). Tavsiya etiladigan kasblar: {kasb_map.get(top1['id'], '')}"
    if top2 and top2['score'] >= 3:
        rec += f" Qo‘shimcha yo‘nalish: {top2['name']} ({top2['score']}/5 ball)."

    return {
        "type": "9-11-sinf",
        "scores": scores,
        "sorted": sorted_spheres[:3],
        "top_id": top1["id"] if top1 else "",
        "top_name": top1["name"] if top1 else "",
        "top_score": top1["score"] if top1 else 0,
        "recommendation": rec
    }

def score_test_tashkilot(answers, lang="uz"):
    """
    answers: dict where key is "1".."20" and value is "A", "B", "C"
    Tashkilotchilik kaliti:
    Har bir 'A' (ha) uchun 1 ball, 'B' (ba'zan) uchun 0.5 ball, teskari savollarga mos hisoblash.
    """
    # Ijobiy savollar: 1, 2, 3, 5, 7, 9, 13, 15, 17, 19
    # Salbiy/teskari savollar: 4, 6, 8, 10, 11, 12, 14, 16, 18, 20
    positive_items = {1, 2, 3, 5, 7, 9, 13, 15, 17, 19}
    negative_items = {4, 6, 8, 10, 11, 12, 14, 16, 18, 20}

    total_score = 0.0
    for i in range(1, 21):
        ans = (answers.get(str(i)) or "").upper().strip()
        if i in positive_items:
            if ans == "A":
                total_score += 1.0
            elif ans == "B":
                total_score += 0.5
        elif i in negative_items:
            if ans == "C":
                total_score += 1.0
            elif ans == "B":
                total_score += 0.5

    total_score = round(total_score, 1)

    if total_score >= 15:
        level = "Yuqori daraja" if lang == "uz" else "Высокий уровень"
        desc = "O‘quvchida tashkilotchilik va liderlik qobiliyati juda yuqori rivojlangan. Jamoani boshqara oladi, tashabbuskor va qaror qabul qilishda mustaqil."
    elif total_score >= 13:
        level = "O‘rtacha daraja" if lang == "uz" else "Средний уровень"
        desc = "O‘quvchida tashkilotchilik qobiliyati o‘rtacha shakllangan. Qulay sharoitda va o‘rtoqlari qo‘llab-quvvatlasa jamoaviy ishlarda faol qatnashadi."
    else:
        level = "Past daraja" if lang == "uz" else "Низкий уровень"
        desc = "Tashkilotchilik qobiliyati sust ifodalangan. Yakka tartibda yoki tayyor yo‘riqnoma asosida ishlashni afzal ko‘radi."

    return {
        "type": "tashkilot",
        "score": total_score,
        "max": 20,
        "percent": round((total_score / 20) * 100),
        "level": level,
        "description": desc
    }
