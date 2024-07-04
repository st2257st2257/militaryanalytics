// Вместо данных в data() в файле скрипта, перенесём их в JSON формат

const commodityItems = [
    { "text": "Самолет легкий: до 30 кг", "query": { "type": "commodity", "category": "Самолет легкий: максимальная взлетная масса до 30 кг" } },
    { "text": "Самолет средний: от 30 кг до 500 кг", "query": { "type": "commodity", "category": "Самолет средний: максимальная взлетная масса от 30 кг до 500 кг" } },
    { "text": "Вертолет легкий: до 30 кг", "query": { "type": "commodity", "category": "Вертолет легкий: максимальная взлетная масса до 30 кг" } },
    { "text": "Вертолет средний: от 30 кг до 500 кг", "query": { "type": "commodity", "category": "Вертолет средний: максимальная взлетная масса от 30 кг до 500 кг" } },
    { "text": "Вертолет тяжелый: от 500 кг", "query": { "type": "commodity", "category": "Вертолет тяжелый: максимальная взлетная масса от 500 кг" } },
    { "text": "Мультиротор легкий: до 30 кг", "query": { "type": "commodity", "category": "Мультиротор легкий: максимальная взлетная масса до 30 кг" } },
    { "text": "Мультиротор средний: от 30 кг до 500 кг", "query": { "type": "commodity", "category": "Мультиротор средний: максимальная взлетная масса от 30 кг до 500 кг" } },
    { "text": "Мультиротор тяжелый: от 500 кг", "query": { "type": "commodity", "category": "Мультиротор тяжелый: максимальная взлетная масса от 500 кг" } },
    { "text": "Образовательные: до 1 кг", "query": { "type": "commodity", "category": "Образовательные: максимальная взлетная масса до 1 кг" } }
];

const serviceItems = [
    { "text": "Логистика: доставка грузов", "query": { "type": "service", "category": "Логистика: доставка грузов" } },
    { "text": "Логистика: перевозка грузов", "query": { "type": "service", "category": "Логистика: перевозка грузов" } }
];

const applicationItems = [
    { "text": "Логистика", "query": { "mainPurposes": "Логистика" }, "categories": ["commodity", "service"] },
    { "text": "Мониторинг", "query": { "mainPurposes": "Мониторинг" }, "categories": ["commodity", "service"] },
    { "text": "Сельское хоз-во", "query": { "mainPurposes": "Сельское хоз-во" }, "categories": ["commodity", "service"] },
    { "text": "Аэрофотосъемка", "query": { "mainPurposes": "Аэрофотосъемка" }, "categories": ["commodity", "service"] },
    { "text": "Дистанционное зондирование", "query": { "mainPurposes": "Дистанционное зондирование" }, "categories": ["commodity", "service"] },
    { "text": "Образование", "query": { "mainPurposes": "Образование" }, "categories": ["commodity", "service"] },
    { "text": "Поиск и спасание", "query": { "mainPurposes": "Поиск и спасание" }, "categories": ["commodity", "service"] }
];

const industryItems = [
    { "text": "Сельское хозяйство", "query": { "mainBranches": "Сельское хозяйство" }, "categories": ["commodity", "service"] },
    { "text": "Лесное хозяйство", "query": { "mainBranches": "Лесное хозяйство" }, "categories": ["commodity", "service"] },
    { "text": "Атомная промышленность", "query": { "mainBranches": "Атомная промышленность" }, "categories": ["commodity", "service"] },
    { "text": "Добыча полезных ископаемых", "query": { "mainBranches": "Добыча полезных ископаемых" }, "categories": ["commodity", "service"] },
    { "text": "Электроэнергетика", "query": { "mainBranches": "Электроэнергетика" }, "categories": ["commodity", "service"] },
    { "text": "ЖКХ", "query": { "mainBranches": "ЖКХ" }, "categories": ["commodity", "service"] },
    { "text": "Наука", "query": { "mainBranches": "Наука" }, "categories": ["commodity", "service"] },
    { "text": "ЧС и безопасность", "query": { "mainBranches": "ЧС и безопасность" }, "categories": ["commodity", "service"] },
    { "text": "Экология", "query": { "mainBranches": "Экология" }, "categories": ["commodity", "service"] },
    { "text": "Инновации", "query": { "mainBranches": "Инновации" }, "categories": ["commodity", "service"] }
];
