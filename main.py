import flet as ft
import random
import json
import os

# --- ПОЛНАЯ БАЗА ДАННЫХ ---
DATABASE = {
    "Холиномиметики": {
        "Прямые": {
            "М-холиномиметики (М-ХМ)": ["Пилокарпин"],
            "Н-холиномиметики (Н-ХМ)": ["Никотин", "Цитизин", "Варениклин"],
            "М,Н-холиномиметики (М,Н-ХМ)": ["Карбахол"]
        },
        "Непрямые (Антихолинэстеразные)": {
            "Центрального действия": ["Донепезил", "Ривастигмин", "Галантамин"],
            "Центрально-периферического действия": ["Ипидакрин"],
            "Периферического действия": ["Пиридостигмин", "Неостигмин"]
        },
        "Реактиваторы холинэстеразы": ["Карбоксим"],
        "Центрального действия": ["Холина альфосцерат"]
    },
    "Холиноблокаторы": {
        "М-ХБ Неселективные": {
            "Системного действия": ["Атропин", "Платифиллин"],
            "Местного действия": ["Белладонны листьев экстракт"]
        },
        "М-ХБ Селективные и органотропные": {
            "Урологические": ["Солифенацин", "Оксибутинин", "Троспия хлорид"],
            "Ингаляционные короткого действия": ["Ипратропия бромид"],
            "Ингаляционные длительного действия": ["Тиотропия бромид", "Гликопиррония бромид"],
            "Офтальмологические": ["Тропикамид", "Циклопентолат"]
        },
        "Центральные М-ХБ (антипаркинсонические)": ["Тригексифенидил", "Бипериден"],
        "Н-ХБ Ганглиоблокаторы": ["Азаметония бромид"],
        "Н-ХБ Миорелаксанты": {
            "Деполяризующие": ["Суксаметония йодид"],
            "Недеполяризующие": ["Пипекурония бромид", "Рокурония бромид", "Атракурия безилат", "Цисатракурия безилат"]
        },
        "Нарушающие высвобождение ацетилхолина": ["Ботулинический токсин типа А"],
        "Миорелаксанты центрального действия": ["Толперизон", "Тизанидин", "Баклофен", "Циклобензаприн"],
        "Миорелаксанты прямого действия": ["Дантролен"]
    },
    "Адреномиметики": {
        "Неселективные α,β-АМ": {
            "α1, α2, β1, β2-АМ": ["Эпинефрин"],
            "α1, α2, β1-АМ": ["Норэпинефрин"],
            "Дофаминергические и адренергические": ["Допамин"]
        },
        "α-АМ": {
            "α1-АМ периферические": ["Фенилэфрин"],
            "α1,2-АМ местные (деконгестанты)": ["Нафазолин", "Ксилометазолин", "Оксиметазолин"],
            "Офтальмологические α1,2-АМ": ["Тетризолин"],
            "Офтальмологические α2-АМ": ["Бримонидин"],
            "α2-АМ центрального действия": ["Клонидин", "Метилдопа"]
        },
        "β-АМ": {
            "β1-АМ": ["Добутамин"],
            "β2-АМ короткого действия": ["Сальбутамол", "Фенотерол"],
            "β2-АМ длительного действия": ["Формотерол", "Салметерол"],
            "β2-АМ ультрадлительного действия": ["Индакатерол", "Олодатерол"],
            "β2-АМ токолитического действия": ["Гексопреналин"],
            "β3-АМ урологические": ["Миробегрон"]
        },
        "Симпатомиметики": ["Эфедрин"]
    },
    "Адреноблокаторы": {
        "α,β-АБ": ["Карведилол"],
        "α-АБ": {
            "Неселективные α1, α2-АБ": ["Ницерголин"],
            "Селективные α1-АБ (урологические)": ["Тамсулозин", "Алфузозин", "Силодозин"],
            "Селективные α1-АБ системные": ["Доксазозин", "Теразозин"],
            "α1-АБ для неотложной терапии": ["Урапидил"],
            "Селективные α2-АБ": ["Йохимбин"]
        },
        "β-АБ": {
            "Неселективные β1,β2-АБ": ["Пропранолол", "Тимолол", "Соталол"],
            "Селективные β1-АБ": ["Метопролол", "Бисопролол", "Атенолол", "Бетаксолол"],
            "β1-АБ с вазодилатацией": ["Небиволол"],
            "Ультракороткие β1-АБ": ["Эсмолол"]
        },
        "Симпатолитики": ["Раувольфии алкалоиды", "Метилдопа"]
    },
    "Анестетики и Снотворные": {
        "Общая анестезия (Ингаляционные)": {
            "Жидкие летучие": ["Севофлуран", "Десфлуран", "Изофлуран", "Галотан"],
            "Газообразные": ["Динитрогена оксид", "Ксенон"]
        },
        "Общая анестезия (Неингаляционные)": {
            "Короткого действия": ["Пропофол", "Кетамин"],
            "Средней продолжительности": ["Тиопентал натрия"],
            "Длительного действия": ["Натрия оксибутират"]
        },
        "Седация и премедикация": {
            "Бензодиазепины": ["Мидазолам"],
            "α2-АМ": ["Дексмедетомидин"]
        },
        "Местная анестезия (Поверхностная)": ["Бензокаин", "Лидокаин", "Оксибупрокаин", "Проксиметакаин", "Тетракаин"],
        "Местная анестезия (Инфильтрационная)": ["Лидокаин", "Артикаин", "Прокаин", "Метивакаин"],
        "Местная анестезия (Проводниковая/Спинальная)": ["Артикаин", "Метивакаин", "Лидокаин", "Бутивакаин", "Ротивакаин", "Левобутивакаин"],
        "Снотворные": {
            "Z-препараты": ["Зопиклон", "Эсзопиклон", "Золпидем", "Залеплон"],
            "Бензодиазепиновые": ["Нитразепам"],
            "Барбитураты": ["Фенобарбитал"],
            "Мелатонинового ряда": ["Мелатонин"],
            "Блокаторы Н1-гистаминовых рецепторов": ["Доксиламин"]
        }
    },
    "Анальгетики и НПВС": {
        "Опиоидные анальгетики": {
            "Полные агонисты": ["Морфин", "Тримеперидин", "Фентанил", "Ремифентанил"],
            "Частичные агонисты": ["Бупренорфин"],
            "Агонисты-антагонисты": ["Буторфанол", "Налбуфин"],
            "Смешанный механизм": ["Трамадол", "Тапентадол"],
            "Антагонисты": ["Налоксон", "Налтрексон"]
        },
        "Неопиоидные анальгетики": {
            "Анальгетики-антипиретики": ["Парацетамол", "Метамизол натрия"],
            "Центрального действия": ["Нефопам"]
        },
        "НПВС Неселективные": {
            "Салицилаты": ["Ацетилсалициловая кислота (>500 мг)"],
            "Пропионаты": ["Ибупрофен", "Флурбипрофен", "Напроксен", "Кетопрофен", "Декскетопрофен"],
            "Ацетаты": ["Диклофенак", "Ацеклофенак", "Индометацин"],
            "Пирролизинкарбоновые": ["Кеторолак"],
            "Оксикамы": ["Пироксикам", "Лорноксикам", "Теноксикам"]
        },
        "НПВС Селективные ЦОГ-2": {
            "Преимущественно селективные": ["Мелоксикам", "Нимесулид"],
            "Высокоселективные (коксибы)": ["Целекоксиб", "Эторикоксиб"]
        }
    },
    "Психотропные средства": {
        "Антипсихотики (Типичные)": {
            "Фенотиазины": ["Хлорпромазин", "Трифлуоперазин", "Перициазин"],
            "Бутирофеноны": ["Галоперидол", "Дроперидол"],
            "Тиоксантены": ["Хлорпротиксен", "Зуклопентиксол"]
        },
        "Антипсихотики (Атипичные)": ["Клозапин", "Рисперидон", "Оланзапин", "Кветиапин", "Амисульприд", "Арипипразол", "Палиперидон", "Карипразин"],
        "Анксиолитики (Транквилизаторы)": {
            "Бензодиазепиновые": ["Хлордиазепоксид", "Диазепам", "Бромдигидрохлорфенилбензодиазепин", "Лоразепам", "Алпразолам"],
            "Небензодиазепиновые": ["Буспирон", "Гидроксизин", "Этифоксин", "Фабомотизол", "Прегабалин"]
        },
        "Седативные средства": {
            "Коркового действия": ["Бромкамфора", "Натрия бромид"],
            "Растительные": ["Валериана", "Пустырник", "Пион", "Персен", "Ново-Пассит"]
        },
        "Противопаркинсонические": {
            "Дофаминергические (Леводопа)": ["Леводопа + Карбидопа", "Леводопа + Бенсеразид"],
            "Агонисты дофаминовых рецепторов": ["Прамипексол", "Пирибедил"],
            "Ингибиторы МАО-В": ["Разагилин"],
            "Ингибиторы КОМТ": ["Энтакапон"],
            "Антагонисты NMDA": ["Амантадин"],
            "Центральные М-ХБ": ["Тригексифенидил", "Бипериден"]
        },
        "Антидепрессанты": {
            "Трициклические (ТЦА)": ["Амитриптилин", "Кломипрамин"],
            "СИОЗС": ["Флуоксетин", "Пароксетин", "Флувоксамин", "Сертралин", "Эсциталопрам", "Циталопрам"],
            "СИОЗСН": ["Венлафаксин", "Дулоксетин"],
            "НаССА": ["Миртазапин"],
            "ИМАО-А": ["Пирлиндол"],
            "Атипичные": ["Агомелатин", "Вортиоксетин", "Тразодон"]
        }
    },
    "Противоэпилептические и Нормотимики": {
        "Противосудорожные (АЭП)": {
            "Блокаторы Na-каналов": ["Карбамазепин", "Окскарбазепин", "Ламотриджин", "Лакосамид", "Фенитоин"],
            "ГАМК-ергические (Бензодиазепины)": ["Клоназепам", "Диазепам", "Мидазолам"],
            "ГАМК-ергические (Барбитураты)": ["Фенобарбитал"],
            "Комбинированный механизм": ["Вальпроевая кислота", "Топирамат"],
            "Блокаторы Ca-каналов Т-типа": ["Этосуксимид"],
            "Лиганды α2δ-субъединицы Ca-каналов": ["Габапентин", "Прегабалин"],
            "Связывающиеся с SV2A": ["Леветирацетам"],
            "Для купирования статуса": ["Диазепам", "Мидазолам", "Вальпроевая кислота", "Леветирацетам"]
        },
        "Нормотимики (Стабилизаторы настроения)": {
            "Препараты лития": ["Лития карбонат"],
            "Противоэпилептические": ["Вальпроевая кислота", "Карбамазепин", "Ламотриджин"],
            "Антипсихотики": ["Оланзапин", "Кветиапин", "Арипипразол", "Карипразин"]
        }
    },
    "Ноотропы и Адаптогены": {
        "Психостимуляторы": ["Кофеин-бензоат натрия"],
        "Адаптогены растительные": ["Женьшень", "Элеутерококк", "Родиола розовая", "Лимонник", "Аралия", "Левзея"],
        "Адаптогены животные": ["Пантокрин"],
        "Ноотропы (Рацетамы)": ["Пирацетам"],
        "Ноотропы (ГАМК-ергические)": ["ГАМК", "Пикамилон", "Гопантеновая кислота", "Аминофенилмасляная кислота"],
        "Холинергические церебропротекторы": ["Холина альфосцерат", "Цитиколин"],
        "Нейрометаболические и пептидные": ["Церебролизин", "Кортексин", "Омберацетам", "Семакс"],
        "Влияющие на мозговое кровообращение": ["Винпоцетин", "Циннаризин", "Ницерголин", "Гинкго двулопастного экстракт"]
    },
    "Дыхательная система": {
        "Противокашлевые (Ненаркотические)": ["Бутамират", "Глауцин"],
        "Противокашлевые (Кодеинсодержащие)": ["Кодеин + терпингидрат", "Кодеин + термопсис + солодка"],
        "Противокашлевые (Периферические)": ["Преноксдиазин", "Леводропропизин"],
        "Отхаркивающие (Рефлекторные)": ["Термопсис", "Алтей", "Солодка", "Тимьян", "Плющ", "Первоцвет", "Подорожник", "Гвайфенезин"],
        "Отхаркивающие (Резорбтивные)": ["Натрия гидрокарбонат", "Аммония хлорид"],
        "Муколитики (Тиоловые)": ["Ацетилцистеин", "Эрдостеин"],
        "Муколитики (Ферментные)": ["Трипсин", "Химотрипсин", "Дорназа альфа"],
        "Муколитики (Мукорегуляторы)": ["Карбоцистеин"],
        "Муколитики (Секретолитики)": ["Амброксол", "Бромгексин"],
        "Бронхолитики β2-АМ": ["Сальбутамол", "Фенотерол", "Формотерол", "Салметерол", "Индакатерол", "Олодатерол"],
        "Бронхолитики М-ХБ": ["Ипратропия бромид", "Тиотропия бромид", "Гликопиррония бромид", "Умеклидиния бромид"],
        "Бронхолитики (Метилксантины)": ["Теофиллин", "Аминофиллин"],
        "Базисная терапия астмы (иГКС)": ["Будесонид", "Беклометазон", "Флутиказон", "Мометазон", "Циклесонид"],
        "Базисная терапия астмы (сГКС)": ["Преднизолон", "Метилпреднизолон", "Дексаметазон"],
        "Антагонисты лейкотриенов": ["Монтелукаст"],
        "Биологические препараты": ["Омализумаб", "Меполизумаб", "Бенрализумаб", "Дупилумаб"],
        "Дыхательные аналептики": ["Никетамид", "Сульфокамфокаин", "Кофеин-бензоат натрия"]
    },
    "Кардиология": {
        "Антиангинальные (Нитраты)": ["Нитроглицерин", "Изосорбида динитрат", "Изосорбида мононитрат", "Пентаэритритила тетранитрат", "Молсидомин"],
        "Антиангинальные (Прочие)": ["Никорандил", "Ивабрадин", "Ранолазин", "Триметазидин", "Валидол"],
        "Гиполипидемические (Статины)": ["Розувастатин", "Аторвастатин", "Симвастатин", "Питавастатин"],
        "Гиполипидемические (Прочие)": ["Эзетимиб", "Фенофибрат", "Алирокумаб", "Эволокумаб", "Инклисиран", "Омега-3"],
        "Антиаритмики (I класс)": ["Прокаинамид", "Лидокаин", "Фенитоин", "Пропафенон", "Флекаинид", "Аллапинин", "Этацизин"],
        "Антиаритмики (III класс)": ["Амиодарон", "Соталол"],
        "Антиаритмики (Прочие)": ["Трифосаденин", "Магния сульфат", "Атропин"],
        "Кардиотоники (Гликозиды)": ["Дигоксин"],
        "Кардиотоники (Негликозидные)": ["Добутамин", "Допамин", "Левосимендан", "Милринон"]
    },
    "Гипертензия и Гипотензия": {
        "Антигипертензивные (иАПФ)": ["Каптоприл", "Эналаприл", "Лизиноприл", "Периндоприл", "Рамиприл", "Фозиноприл"],
        "Антигипертензивные (Сартаны)": ["Лозартан", "Валсартан", "Ирбесартан", "Кандесартан", "Телмисартан", "Олмесартан", "Азилсартан"],
        "Антигипертензивные (АРНИ)": ["Валсартан + Сакубитрил"],
        "Антигипертензивные (Центральные)": ["Метилдопа", "Моксонидин", "Рилменидин", "Клонидин"],
        "Антигипертензивные (Неотложные)": ["Натрия нитропруссид", "Урапидил"],
        "Диуретики (Петлевые)": ["Фуросемид", "Торасемид"],
        "Диуретики (Осмотические)": ["Маннитол"],
        "Диуретики (Тиазидные)": ["Гидрохлоротиазид", "Индапамид", "Хлорталидон"],
        "Диуретики (Ингибиторы карбоангидразы)": ["Ацетазоламид"],
        "Диуретики (Калийсберегающие)": ["Спиронолактон", "Эплеренон"],
        "Вазопрессоры (Шок)": ["Эпинефрин", "Норэпинефрин", "Допамин", "Фенилэфрин", "Флудрокортизон"],
        "Инфузионные растворы": ["Натрия хлорид 0.9%", "Рингер-лактат", "Стерофундин", "Альбумин"]
    },
    "Гастроэнтерология": {
        "Влияющие на аппетит": ["Полыни настойка", "Орлистат", "Сибутрамин", "Лираглутид", "Семаглутид", "Тирзенатид"],
        "Антациды (Всасывающиеся)": ["Натрия гидрокарбонат", "Кальция карбонат + Магния карбонат"],
        "Антациды (Невсасывающиеся)": ["Алюминия фосфат", "Алюминия оксид + Магния гидроксид", "Алгелдрат + Магния гидроксид"],
        "Альгинаты": ["Натрия альгинат + Натрия гидрокарбонат + Кальция карбонат"],
        "Антисекреторные (ИПП)": ["Омепразол", "Пантопразол", "Рабепразол", "Эзомепразол"],
        "Антисекреторные (P-CAB)": ["Тегопразан"],
        "Антисекреторные (H2-гистаминоблокаторы)": ["Фамотидин"],
        "Гастропротекторы": ["Висмута трикалия дицитрат", "Ребамипид"],
        "Прокинетики": ["Метоклопрамид", "Домперидон", "Итоприд"],
        "Противорвотные (5-HT3)": ["Ондансетрон", "Палноосетрон"],
        "Противорвотные (NK1)": ["Апрепитант", "Фосапрепитант"],
        "Противорвотные (Прочие)": ["Дексаметазон", "Дименгидринат"],
        "Противодиарейные": ["Регидрон", "Лоперамид", "Смектит диоктаэдрический", "Энтеросгель", "Полисорб", "Нифуроксазид", "Рифаксимин", "Сахаромицеты буларди", "Лактобактерии"],
        "Слабительные (Объемные)": ["Подорожника овального семян оболочка"],
        "Слабительные (Осмотические)": ["Макрогол", "Лактулоза", "Лактитол", "Магния сульфат"],
        "Слабительные (Стимулирующие)": ["Бисакодил", "Натрия пикосульфат", "Сеннозиды А и В"],
        "Слабительные (Ректальные)": ["Глицерол", "Натрия цитрат + Натрия лаурилсульфоацетат + Сорбитол"],
        "Спазмолитики": ["Дротаверин", "Мебеверин", "Пинаверия бромид", "Отилония бромид", "Гиосцина бутилбромид", "Тримебутин", "Алверин + Симетикон"],
        "Пеногасители": ["Симетикон"]
    }
}

def parse_pharmacology(class_text, subclass_text=""):
    text = (class_text + " " + subclass_text).lower()
    selectivity = "-"
    receptors = "-"
    if "неселектив" in text: selectivity = "Неселективный"
    elif "селектив" in text: selectivity = "Селективный"
    recs = []
    if "α1" in text or "a1" in text: recs.append("α1")
    if "α2" in text or "a2" in text: recs.append("α2")
    if "β1" in text or "b1" in text: recs.append("β1")
    if "β2" in text or "b2" in text: recs.append("β2")
    if "β3" in text or "b3" in text: recs.append("β3")
    if "м-х" in text or "м-хб" in text: recs.append("М")
    if "н-х" in text or "н-хб" in text: recs.append("Н")
    if "м,н" in text: recs.append("М, Н")
    if recs: receptors = ", ".join(sorted(list(set(recs))))
    return selectivity, receptors

TOPIC_DRUGS, TOPIC_CATS, ALL_DRUGS_FLAT = {}, {}, []
for t, classes in DATABASE.items():
    topic_drugs, topic_cats = [], []
    for cls, subcls in classes.items():
        if isinstance(subcls, dict):
            for sub, drugs in subcls.items():
                for d in drugs: topic_drugs.append((d, t, cls, sub))
                topic_cats.append((cls, sub, t))
        else:
            for d in subcls: topic_drugs.append((d, t, cls, None))
            topic_cats.append((cls, None, t))
    TOPIC_DRUGS[t] = topic_drugs
    TOPIC_CATS[t] = topic_cats
    ALL_DRUGS_FLAT.extend([d[0] for d in topic_drugs])
ALL_DRUGS_FLAT = list(set(ALL_DRUGS_FLAT))

STATS_FILE = "stats.json"
def load_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, 'r', encoding='utf-8') as f: return json.load(f)
    return {}
def save_stats(stats):
    with open(STATS_FILE, 'w', encoding='utf-8') as f: json.dump(stats, f, ensure_ascii=False)

def get_topic_stats(stats, topic):
    if topic not in stats: stats[topic] = {"class_mastered": [], "search_mastered": []}
    return stats[topic]

def calc_progress(stats, topics, mode="class"):
    done, total = 0, 0
    for t in topics:
        drugs = TOPIC_DRUGS[t] if mode == "class" else TOPIC_CATS[t]
        total += len(drugs)
        if mode == "class": done += sum(1 for d in drugs if d[0] in get_topic_stats(stats, t)["class_mastered"])
        else: done += len(get_topic_stats(stats, t)["search_mastered"])
    return done, total

# --- ИНТЕРФЕЙС FLET ---
def main(page: ft.Page):
    page.title = "Фарма Ассистент"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#F0F4F8"
    page.padding = 15
    
    stats = load_stats()

    def clear_page():
        page.controls.clear()
        page.update()

    # ГЛАВНЫЙ ЭКРАН
    def show_home(e=None):
        clear_page()
        page.add(ft.Text("Бойко хочет чтобы ты знал фарму 😏", italic=True, color="#7f8c8d", size=14))
        page.add(ft.Text("Ассистент", size=32, weight=ft.FontWeight.BOLD, color="#2C3E50"))
        
        page.add(ft.Row([
            ft.ElevatedButton("Сбросить прогресс", bgcolor="#FFCDD2", color="#D32F2F", on_click=reset_confirm),
            ft.ElevatedButton("🎓 ЭКЗАМЕН", bgcolor="#F39C12", color="#FFF", on_click=show_exam_setup)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN))

        list_view = ft.ListView(expand=True, spacing=10)
        for topic in DATABASE.keys():
            dc, tc = calc_progress(stats, [topic], "class")
            ds, ts = calc_progress(stats, [topic], "search")
            pc = dc / tc if tc > 0 else 0
            ps = ds / ts if ts > 0 else 0

            card = ft.Container(
                content=ft.Column([
                    ft.Text(topic, size=18, weight=ft.FontWeight.BOLD),
                    ft.Row([ft.Text("Класс:", width=90), ft.ProgressBar(value=pc, color="#2ECC71", bgcolor="#FFCDD2", expand=True), ft.Text(f"{int(pc*100)}%", width=40)]),
                    ft.Row([ft.Text("Поиск:", width=90), ft.ProgressBar(value=ps, color="#3498DB", bgcolor="#FFCDD2", expand=True), ft.Text(f"{int(ps*100)}%", width=40)]),
                    ft.Row([
                        ft.ElevatedButton("Классифицировать", bgcolor="#8ACDA6", color="#FFF", expand=True, on_click=lambda e, t=topic: start_mode1(t)),
                        ft.ElevatedButton("Найти средства", bgcolor="#6BA4D9", color="#FFF", expand=True, on_click=lambda e, t=topic: start_mode2(t))
                    ])
                ]), bgcolor="#FFFFFF", padding=15, border_radius=15, border=ft.border.all(1, "#E2E8F0")
            )
            list_view.controls.append(card)
        page.add(list_view)

    # СБРОС
    def reset_confirm(e):
        def do_reset(ev):
            nonlocal stats
            stats = {}
            save_stats(stats)
            page.dialog.open = False
            show_home()
        page.dialog = ft.AlertDialog(title=ft.Text("Сброс"), content=ft.Text("Сбросить весь прогресс?"), actions=[
            ft.TextButton("Да", on_click=do_reset), ft.TextButton("Нет", on_click=lambda _: setattr(page.dialog, 'open', False) or page.update())
        ])
        page.dialog.open = True
        page.update()

    # НАСТРОЙКА ЭКЗАМЕНА
    def show_exam_setup(e):
        clear_page()
        page.add(ft.Text("Настройка экзамена", size=24, weight=ft.FontWeight.BOLD))
        cbs = {}
        col = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True)
        for topic in DATABASE.keys():
            cb = ft.Checkbox(label=topic, value=True)
            cbs[topic] = cb
            col.controls.append(cb)
        page.add(col)
        
        def start(mode):
            selected = [t for t, cb in cbs.items() if cb.value]
            if not selected: return
            if mode == 'class': start_exam_classify(selected)
            else: start_exam_search(selected)

        page.add(ft.Row([
            ft.ElevatedButton("Классификация", bgcolor="#2ECC71", color="#FFF", expand=True, on_click=lambda _: start('class')),
            ft.ElevatedButton("Поиск", bgcolor="#3498DB", color="#FFF", expand=True, on_click=lambda _: start('search'))
        ]))
        page.add(ft.TextButton("Назад", on_click=show_home))

    # РЕЖИМ КЛАССИФИКАЦИИ (ОБЩИЙ)
    def build_classify_ui(selected_topics, target_drug, target_topic, target_cls, target_sub, is_exam):
        clear_page()
        
        # Прогресс
        dc, tc = calc_progress(stats, selected_topics, "class")
        pc = dc / tc if tc > 0 else 0
        pb = ft.ProgressBar(value=pc, color="#2ECC71", bgcolor="#FFCDD2")
        lbl_prog = ft.Text(f"Освоено: {dc} из {tc} ({int(pc*100)}%)", size=12)
        page.add(ft.Container(content=ft.Column([pb, lbl_prog]), bgcolor="#FFF", padding=10, border_radius=10))

        # Карточка препарата
        page.add(ft.Container(content=ft.Column([
            ft.Text("Классифицируйте:", size=14, color="#7f8c8d"),
            ft.Text(target_drug, size=32, weight=ft.FontWeight.BOLD, color="#E67E22")
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER), bgcolor="#FFF", padding=20, border_radius=15, margin=10))

        # Выпадающие списки
        dd_topic = ft.Dropdown(label="Тема", options=[ft.dropdown.Option(t) for t in selected_topics], disabled=not is_exam)
        if is_exam: dd_topic.value = None
        else: dd_topic.value = selected_topics[0]

        dd_class = ft.Dropdown(label="Класс")
        dd_sub = ft.Dropdown(label="Подкласс/Механизм")
        dd_sel = ft.Dropdown(label="Селективность", options=[ft.dropdown.Option("-"), ft.dropdown.Option("Селективный"), ft.dropdown.Option("Неселективный")])
        dd_rec = ft.Dropdown(label="Рецепторы", options=[ft.dropdown.Option(x) for x in ["-", "α1", "α2", "α1, α2", "β1", "β2", "β1, β2", "β3", "М", "Н", "М, Н"]])

        def update_classes(e=None):
            if not dd_topic.value: return
            classes = list(DATABASE[dd_topic.value].keys())
            dd_class.options = [ft.dropdown.Option(c) for c in classes]
            dd_class.value = classes[0]
            update_subclasses()

        def update_subclasses(e=None):
            if not dd_topic.value or not dd_class.value: return
            subs = DATABASE[dd_topic.value].get(dd_class.value, {})
            if isinstance(subs, dict):
                keys = list(subs.keys())
                dd_sub.options = [ft.dropdown.Option(k) for k in keys]
                dd_sub.value = keys[0]
            else:
                dd_sub.options = [ft.dropdown.Option("-")]
                dd_sub.value = "-"
            update_props()

        def update_props(e=None):
            if not dd_class.value: return
            s, r = parse_pharmacology(dd_class.value, dd_sub.value if dd_sub.value != "-" else "")
            dd_sel.value = s
            dd_rec.value = r
            page.update()

        dd_topic.on_change = update_classes
        dd_class.on_change = update_subclasses
        dd_sub.on_change = update_props

        if is_exam:
            update_classes()
        else:
            dd_class.options = [ft.dropdown.Option(c) for c in DATABASE[selected_topics[0]].keys()]
            dd_class.value = list(DATABASE[selected_topics[0]].keys())[0]
            update_subclasses()

        page.add(dd_topic, dd_class, dd_sub, dd_sel, dd_rec)

        feedback = ft.Text("", weight=ft.FontWeight.BOLD, size=16)
        page.add(feedback)

        def check(e):
            if not dd_topic.value or not dd_class.value: return
            target_s, target_r = parse_pharmacology(target_cls, target_sub if target_sub else "")
            correct = (dd_topic.value == target_topic and dd_class.value == target_cls and 
                       (dd_sub.value == target_sub if target_sub else dd_sub.value == "-") and 
                       dd_sel.value == target_s and dd_rec.value == target_r)
            
            if correct:
                get_topic_stats(stats, target_topic)["class_mastered"].append(target_drug)
                get_topic_stats(stats, target_topic)["class_mastered"] = list(set(get_topic_stats(stats, target_topic)["class_mastered"]))
                save_stats(stats)
                feedback.value = "✅ Верно!"
                feedback.color = "#2ECC71"
                # Обновляем прогресс
                dc, tc = calc_progress(stats, selected_topics, "class")
                pb.value = dc / tc if tc > 0 else 0
                lbl_prog.value = f"Освоено: {dc} из {tc} ({int(pb.value*100)}%)"
            else:
                feedback.value = f"❌ Ошибка.\nПравильно: {target_topic} -> {target_cls} -> {target_sub}\nСелективность: {target_s}, Рецепторы: {target_r}"
                feedback.color = "#E74C3C"
            
            btn_next.visible = True
            page.update()

        def next_q(e):
            if is_exam: start_exam_classify(selected_topics)
            else: start_mode1(selected_topics[0])

        btn_check = ft.ElevatedButton("Проверить", bgcolor="#F39C12", color="#FFF", on_click=check)
        btn_next = ft.ElevatedButton("Далее", bgcolor="#2ECC71", color="#FFF", on_click=next_q, visible=False)
        page.add(btn_check, btn_next, ft.TextButton("В меню", on_click=show_home))
        page.update()

    def start_mode1(topic):
        target = random.choice(TOPIC_DRUGS[topic])
        build_classify_ui([topic], *target, is_exam=False)

    def start_exam_classify(topics):
        pool = [item for t in topics for item in TOPIC_DRUGS[t]]
        target = random.choice(pool)
        build_classify_ui(topics, *target, is_exam=True)

    # РЕЖИМ ПОИСКА
    def build_search_ui(selected_topics, target_cls, target_sub, target_topic, correct_drugs, is_exam):
        clear_page()
        dc, tc = calc_progress(stats, selected_topics, "search")
        pc = dc / tc if tc > 0 else 0
        pb = ft.ProgressBar(value=pc, color="#3498DB", bgcolor="#FFCDD2")
        lbl_prog = ft.Text(f"Освоено: {dc} из {tc} ({int(pc*100)}%)", size=12)
        page.add(ft.Container(content=ft.Column([pb, lbl_prog]), bgcolor="#FFF", padding=10, border_radius=10))

        task_name = f"Тема: {target_topic}\n{target_cls}" + (f" -> {target_sub}" if target_sub else "")
        page.add(ft.Container(content=ft.Column([
            ft.Text("Найдите препараты:", size=14, color="#7f8c8d"),
            ft.Text(task_name, size=18, weight=ft.FontWeight.BOLD, color="#3498DB")
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER), bgcolor="#FFF", padding=15, border_radius=15, margin=10))

        wrong = list(set(ALL_DRUGS_FLAT) - set(correct_drugs))
        random.shuffle(wrong)
        options = correct_drugs + wrong[:max(0, 10 - len(correct_drugs))]
        random.shuffle(options)

        selected_btns = []
        grid = ft.GridView(expand=True, max_extent=150, child_aspect_ratio=2.5, spacing=10)
        
        for drug in options:
            btn = ft.ElevatedButton(drug, bgcolor="#FFF", color="#333", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)))
            def toggle(e, b=btn, d=drug):
                if d in selected_btns:
                    selected_btns.remove(d); b.bgcolor = "#FFF"; b.color = "#333"
                else:
                    selected_btns.append(d); b.bgcolor = "#DFF0D8"; b.color = "#2C3E50"
                page.update()
            btn.on_click = toggle
            grid.controls.append(btn)
        
        page.add(grid)
        feedback = ft.Text("", weight=ft.FontWeight.BOLD, size=16)
        page.add(feedback)

        def finish(e):
            if set(correct_drugs) == set(selected_btns):
                get_topic_stats(stats, target_topic)["search_mastered"].append(f"{target_cls}|{target_sub}")
                get_topic_stats(stats, target_topic)["search_mastered"] = list(set(get_topic_stats(stats, target_topic)["search_mastered"]))
                save_stats(stats)
                feedback.value = "✅ Идеально!"
                feedback.color = "#2ECC71"
                dc, tc = calc_progress(stats, selected_topics, "search")
                pb.value = dc / tc if tc > 0 else 0
                lbl_prog.value = f"Освоено: {dc} из {tc} ({int(pb.value*100)}%)"
            else:
                missed = set(correct_drugs) - set(selected_btns)
                extra = set(selected_btns) - set(correct_drugs)
                msg = ""
                if missed: msg += f"Забыли: {', '.join(missed)}\n"
                if extra: msg += f"Лишние: {', '.join(extra)}"
                feedback.value = f"❌ Ошибка:\n{msg}"
                feedback.color = "#E74C3C"
            
            btn_next.visible = True
            page.update()

        def next_q(e):
            if is_exam: start_exam_search(selected_topics)
            else: start_mode2(selected_topics[0])

        btn_finish = ft.ElevatedButton("Закончить выбор", bgcolor="#F39C12", color="#FFF", on_click=finish)
        btn_next = ft.ElevatedButton("Далее", bgcolor="#3498DB", color="#FFF", on_click=next_q, visible=False)
        page.add(btn_finish, btn_next, ft.TextButton("В меню", on_click=show_home))
        page.update()

    def start_mode2(topic):
        t_cls, t_sub, _ = random.choice(TOPIC_CATS[topic])
        correct = DATABASE[topic][t_cls][t_sub] if t_sub else DATABASE[topic][t_cls]
        build_search_ui([topic], t_cls, t_sub, topic, correct, is_exam=False)

    def start_exam_search(topics):
        pool = [item for t in topics for item in TOPIC_CATS[t]]
        t_cls, t_sub, t_topic = random.choice(pool)
        correct = DATABASE[t_topic][t_cls][t_sub] if t_sub else DATABASE[t_topic][t_cls]
        build_search_ui(topics, t_cls, t_sub, t_topic, correct, is_exam=True)

    show_home()

ft.app(target=main)
