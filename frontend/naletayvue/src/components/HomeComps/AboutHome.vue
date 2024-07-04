<template>
    <div class="about-container">
    <h2>О проекте</h2>
        <div class="about-content">
            <div class="about-row">
                <div class="about-block">
                    <p>
                    <b>НАЛЕТАЙ.РФ</b> – первый в России маркетплейс на рынке беспилотной авиации, объединяющий
                    производителей, дистрибьюторов, эксплуатантов, конструкторов и заказчиков на одной площадке. Создан
                    ключевым игроком рынка беспилотной авиации в стране - АО «Государственная транспортная лизинговая компания».
                    </p>
                </div>
                <div class="about-card mission">
                    <div class="icon-placeholder"><flagIcon/></div>
                    <h3>Миссия</h3>
                    <p>
                    Мы видим нашу миссию в создании полноценной экосистемы, охватывающей все потребности основных участников рынка беспилотной авиации в России, включая продажу беспилотных авиационных систем (БАС) и предоставление сопутствующих сервисов и услуг, обеспечение обратной связи от эксплуатантов к производителям, сбор и систематизацию аналитических данных, а также организацию доступа к мерам господдержки.
                    </p>
                </div>
            </div>
            <div class="about-row">
                <div class="about-card development">
                    <div class="icon-placeholder"><settingsIcon/></div>
                    <h3>Развитие</h3>
                    <p>
                    Маркетплейс в настоящее время работает в режиме бета-версии. Регистрация на экосистеме открыта пока только для производителей и дистрибьюторов. В дальнейшем планируется подключение эксплуатантов и заказчиков, что позволит значительно увеличить количество участников.
                    </p>
                </div>
                <div class="about-card communication">
                    <div class="icon-placeholder"><puzzleIcon/></div>
                    <h3>Коммуникация</h3>
                    <p>
                    При необходимости можно также получить консультацию менеджеров или обратиться в службу технической поддержки маркетплейса.
                    </p>
                </div>
                <div class="about-card assortment">
                    <div class="icon-placeholder"><bookOpenIcon/></div>
                    <h3>Ассортимент</h3>
                    <p>
                    Сейчас на НАЛЕТАЙ.РФ доступны для заказа все представленные в каталоге БАС с описанием их сферы применения и всех технических характеристик. Удобная система фильтрации и возможность построить бриф для поиска поможет быстро найти интересующую модель. После выбора БАС клиентское подразделение будет отправлять коммерческое предложение, а также отгружать оферту на оформление БАС в лизинг.
                    </p>
                </div>
            </div>
        </div>
        <div class="about-stats">
            <div class="stat-item">
                <p class="stat-number">99</p>
                <p>коптеров в ассортименте</p>
            </div>
            <div class="stat-item">
                <p class="stat-number">99</p>
                <p>довольных клиентов</p>
            </div>
            <div class="stat-item">
                <p class="stat-number">99</p>
                <p>реализованных проектов</p>
            </div>
            <div class="stat-item">
                <p class="stat-number">99</p>
                <p>уникальных услуг</p>
            </div>
        </div>
    </div>
</template>

<script>
import puzzleIcon from '@/assets/icons/puzzle.svg'
import bookOpenIcon from '@/assets/icons/book_open.svg'
import flagIcon from '@/assets/icons/flag.svg'
import settingsIcon from '@/assets/icons/settings.svg'

export default {
    components: {
        puzzleIcon,
        bookOpenIcon,
        flagIcon,
        settingsIcon,

    },
    name: 'AboutProject'
}
</script>

<style>
.about-container {
    display: flex;
    flex-flow: column;
    justify-content: flex-start;
    align-items: flex-start;
}

.about-container h2{
    font-size: 36px;
    font-weight: 600;
    color: var(--color-mute-text);
}


.about-container .about-content {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.about-container .about-row {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    gap: 20px;
}

.about-container .about-block {
    display: flex;
    flex-flow: column;
    width: 25%;
    justify-content: center;
    text-align: left;
}

.about-container .about-card {
    flex: 1;
    text-align: left;
    padding: 20px;
    border-radius: 20px;
}

.about-container .about-block h3,
.about-container .about-card h3 {
    font-weight: 600;
    margin-top: 0;
}

@media (hover: hover) {
    .about-container .about-card:hover {
        transform: translateY(-5px);
    }
}
.about-container .mission {
    flex: 0.9;
    background-color: var(--color-btn-green-background);
    color: #fff;
}

.about-container .development {
    background-color: var(--color-btn-green-background);
    color: #fff;
}

.about-container .communication {
    flex: 0.8;
    background-color: #cccccc;
    color: #000;
}

.about-container .assortment {
    flex: 1.2;
    background-color: #333333;
    color: #fff;
}

.about-container .icon-placeholder {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 84px;
    height: 84px;
    background-color: #fff;
    border-radius: 15px;
    margin-bottom: 10px;
}

.about-container .icon-placeholder svg{
    display: flex;
    justify-content: center;
    align-items: center;
    width: fit-content;
    height: fit-content;
}

.about-container .icon-placeholder svg path{
    width: 100%;
    height: 100%;
    stroke: var(--color-mute-text);
}

.about-container .about-stats {
    display: none;
    width: 100%;
    justify-content: space-between;
    padding: 20px;
    border-radius: 10px;
    margin-top: 20px;
}

.about-container .stat-item {
    display: flex;
    text-align: left;
    flex-direction: column;
    align-items: flex-start;
}

.about-container .stat-item .icon {
    width: 60px;
    height: 60px;
    background-color: #cccccc;
    border-radius: 50%;
    margin-bottom: 10px;
}

.about-container .stat-number {
    font-size: 96px;
    font-weight: bold;
    height:70%;
    color: var(--color-btn-green-background);
}

.about-container b {
    font-weight: 600;
}

@media (max-width: 1024px) {

    .about-container h2 {
        font-size: 28px;
    }

    .about-container .about-row {
        flex-direction: column;
    }

    .about-container .about-block,
    .about-container .about-card {
        width: 100%;
        padding: 15px;
    }

    .about-container .stat-number {
        font-size: 64px;
    }

    .about-container .about-stats {
        flex-flow: row wrap;
    }
}
</style>
