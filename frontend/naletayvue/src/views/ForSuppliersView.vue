<template>
    <div class="suppliers-container">
        <SingleCarousel :autoScroll="true" :scrollInterval="5000" :singleBanner="true" :path="'suppliers_carusels'" />

        <section class="why-section">
            <h2>Зачем поставщикам маркетплейс Налетай.рф?</h2>
            <div class="why-benefits">
                <div class="why-benefit">
                    <div class="icon-placeholder"><graphsIcon/></div>
                    <p>Для существенного расширения своей клиентской базы</p>
                </div>
                <div class="why-benefit">
                    <div class="icon-placeholder"><lineGraphsIcon/></div>
                    <p>Для укрепления своей репутации и позиций на рынке</p>
                </div>
                <div class="why-benefit">
                    <div class="icon-placeholder"><chatIcon/></div>
                    <p>Для прямой и быстрой коммуникации с потенциальными клиентами</p>
                </div>
            </div>
        </section>

        <section class="benefits-section">
            <h2>Преимущества работы с нами</h2>
            <div class="benefits">
                <div class="benefit-card" 
                    v-for="(benefit, index) in benefits" 
                    :key="index" 
                    :style="{ backgroundColor: benefit.color, color: benefit.textColor }">
                    <div class="icon-placeholder"><flagIcon/></div>
                    <span>
                        <h3 :style="{ color: benefit.textColor }">{{ benefit.title }}</h3>
                        <p :style="{ color: benefit.textColor }">{{ benefit.description }}</p>
                    </span>
                </div>
            </div>
            <button class="btn grey-btn" style="align-self: center;" @click="openRegister()">Стать поставщиком</button>
        </section>

        <section class="fit-section">
            <h2>Кому подходит маркетплейс Налетай.рф?</h2>
            <div class="fit-steps">
                <div class="fit-step" v-for="(step, index) in fitSteps" :key="index">
                    <h3>{{ step.number }}</h3>
                    <p>{{ step.text }}</p>
                </div>
            </div>
        </section>

        <section class="existing-suppliers-section">
            <h2>Поставщики, которые уже с нами:</h2>
            <Slider :suppliers="partners" :visibleItems="4" />
        </section>

        <section class="steps-section">
            <h2>Шаги для поставщиков</h2>
            <div class="steps">
                <div class="step" v-for="(step, index) in steps.slice(0, 4)" :key="index">
                    <div class="step-content">
                        <h3 class="step-number">{{ step.title }}</h3>
                        <p>{{ step.description }}</p>
                    </div>
                    <svg v-if="index < 3" class="arrow-shape right-arrow" viewBox="0 0 30 25">
                        <polygon points="0,0 30,12.5 0,25" />
                    </svg>
                    <svg v-if="index == 3" class="arrow-shape down-arrow" viewBox="0 0 30 25">
                        <polygon points="0,0 30,12.5 0,25" />
                    </svg>
                </div>
                <div class="step last-step" :data-step="steps[4].title">
                    <h3 class="step-number">{{ steps[4].title }}</h3>
                    <p>{{ steps[4].description }}</p>
                </div>
            </div>
        </section>
        
        <section class="join-section">
            <h2>
                Присоединяйтесь к Налетай.рф.<br/>
                Создайте свой первый каталог.<br/>
                И начните получать новых клиентов сейчас!
            </h2>
            <button class="btn white-btn" @click="openRegister()">Зарегистрироваться</button>
        </section>
    </div>
</template>

<script scoped>
import api from '@/authAPI.js';
import chatIcon from '@/assets/icons/chat.svg';
import graphsIcon from '@/assets/icons/graphs.svg';
import lineGraphsIcon from '@/assets/icons/line_graphs.svg';
import flagIcon from '@/assets/icons/flag.svg';
import SingleCarousel from '@/components/Carousel.vue';
import Slider from '@/components/MiniSlider.vue';

export default {
    components: {
        chatIcon,
        graphsIcon,
        lineGraphsIcon,
        flagIcon,
        SingleCarousel,
        Slider
    },
    data() {
        return {
            partners: [],
            benefits: [
                {
                    title: "Новый канал сбыта продукции",
                    description: "B2B онлайн-канал в лице сильного и надежного партнера. Широкая сеть и возможности платформы позволят всем участникам рынка занять и вести развитый рынок беспилотной авиации.",
                    color: "#088B95",
                    textColor: "#FFFFFF"
                },
                {
                    title: "Больше клиентов, прямые контракты",
                    description: "Мы привлекаем на платформу максимально новых и заинтересованных клиентов. Увеличение клиентской базы с нами, идеальных ваших регулярных поставок.",
                    color: "#343A40",
                    textColor: "#FFFFFF"
                },
                {
                    title: "Быстрый и понятный процесс заказов",
                    description: "Мы размещаем каталог и отправляем КТ в ответ на заявки, ведем переговоры и все объемы документов в едином чате.",
                    color: "#78E1C2",
                    textColor: "#000000"
                },
                {
                    title: "Мы все делаем за вас",
                    description: "Берем продвижение платформы и категорий на себя: освещаем в прессе, ведем рекламные кампании, работаем с трафиком. От вас нужно только регистрация, каталог и конкурентные цены.",
                    color: "#DEE2E6",
                    textColor: "#000000"
                }
            ],
            fitSteps: [
                { number: "01", text: "Производителям БПЛА и дронопортов" },
                { number: "02", text: "Компаниям, оказывающим услуги с использованием БПЛА" },
                { number: "03", text: "Дистрибьюторам" },
                { number: "04", text: "Конструкторам и мелким предприятиям на стадии развития" },
                { number: "05", text: "На первом этапе развития функционал маркетплейса доступен только для юридических лиц." }
            ],
            steps: [
                { title: "Шаг 1", description: "Пройдите быструю регистрацию" },
                { title: "Шаг 2", description: "Заполните данные о компании в личном кабинете" },
                { title: "Шаг 3", description: "Подпишите договор на доступ к платформе" },
                { title: "Шаг 4", description: "Загрузите свой каталог в личном кабинете" },
                { title: "Шаг 5", description: "Принимайте заказы!" }
            ]
        };
    },
    methods: {
        openRegister() {
            window.loginModal.open('register')
        },
        async fetchPartners() {
            try {
                const formData = new FormData();
                formData.append('actionType', 'getAllSellers');
                const response = await api.post('/user/get_partners/', formData);
                if (response.data.result) {
                    const partnersData = [];
                    for (let key in response.data) {
                        if (response.data.hasOwnProperty(key) && key !== 'result') {
                            partnersData.push(response.data[key]);
                        }
                    }
                    this.partners = partnersData;
                } else {
                    console.error('Failed to fetch partners: no result');
                    throw new Error('Failed to fetch partners: no result');
                }
            } catch (error) {
                console.error('Failed to fetch partners:', error);
                throw error;
            }
        }
    },
    mounted() {
        this.fetchPartners();
    }
};
</script>

<style>
.suppliers-container {
    display: flex;
    flex-flow: column;
    width: 100%;
    gap: 70px;
    max-width: 1280px;
    padding: 0px 20px;
    box-sizing: border-box;
    overflow-x: hidden;
}

.suppliers-container h2 {
    font-size: 26px;
    font-weight: 600;
    line-height: 1.5;
    color: #343A40;
}

.suppliers-container .why-section {
    display: flex;
    flex-direction: column;
    text-align: left;
    gap: 25px;
    box-sizing: border-box;
}

.suppliers-container .why-benefits {
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 15px;
}

.suppliers-container .why-benefit {
    display: flex;
    width: 32%;
    height: 114px;
    text-align: center;
    justify-content: center;
    align-items: center;
    gap: 15px;
    background: #F8F9FA;
    padding: 10px;
    transition: transform 0.3s ease;
    border-radius: 10px;
    box-sizing: border-box;
}

.suppliers-container .why-benefit .icon-placeholder {
    width: 64px;
    height: 64px;
    padding: 10px;
}

.suppliers-container .why-benefit .icon-placeholder path {
    stroke: #000;
}

.suppliers-container .why-benefit p {
    font-size: 18px;
    font-weight: 400;
    line-height: 1.2;
    text-align: left;
    width: 80%;
}

.suppliers-container .why-benefit:hover {
    transform: translateY(-10px);
}

.suppliers-container .benefits-section {
    display: flex;
    flex-direction: column;
    text-align: left;
    gap: 25px;
    box-sizing: border-box;
}

@media (min-width: 1024px) {
    .suppliers-container .benefits-section .benefits {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 20px;
    }
}

@media (min-width: 768px) and (max-width: 1023px) {
    .suppliers-container .benefits-section .benefits {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 20px;
    }
}

@media (max-width: 767px) {
    .suppliers-container .benefits-section .benefits {
        display: flex;
        flex-direction: column;
        gap: 20px;
        align-items: center;
    }
    .suppliers-container .benefit-card {
        width: 100%;
        max-width: none;
    }
}

.suppliers-container .benefit-card {
    display: flex;
    flex-direction: column;
    gap: 30px;
    padding: 20px;
    text-align: left;
    transition: transform 0.3s ease;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    box-sizing: border-box;
}

.suppliers-container .benefit-card .icon-placeholder path {
    stroke: #343A40;
}

.suppliers-container .benefit-card:hover {
    transform: translateY(-10px);
}

.suppliers-container .benefit-card .icon-placeholder {
    width: 84px;
    height: 84px;
    background: #fff;
    padding: 10px;
    border-radius: 10px;
}

.suppliers-container .benefit-card h3 {
    font-size: 20px;
    font-weight: 500;
    line-height: 1.3;
    margin-bottom: 15px;
}

.suppliers-container .benefit-card p {
    font-size: 14px;
}

.suppliers-container .fit-section {
    display: flex;
    flex-flow: column;
    gap: 25px;
    background-color: #fff;
    text-align: left;
    box-sizing: border-box;
}

.suppliers-container .fit-steps {
    display: flex;
    flex-flow: wrap;
    gap: 20px;
}

.suppliers-container .fit-step {
    cursor: default;
    display: flex;
    gap: 10px;
    max-height: 74px;
    justify-content: flex-start;
    align-items: center;
    width: fit-content;
    text-align: left;
    transition: all 0.3s ease;
    overflow: hidden;
    border-radius: 15px;
    background: #F8F9FA;
    box-sizing: border-box;
}

.suppliers-container .fit-step p {
    font-size: 18px;
    font-weight: 400;
    line-height: 21.6px;
    letter-spacing: -0.02em;
    text-align: left;
    padding-right: 105px;
}

.suppliers-container .fit-step:last-child p {
    padding-right: 40px;
}

.suppliers-container .fit-step h3 {
    display: flex;
    justify-content: center;
    align-items: center;
    background: var(--color-btn-green-background);
    width: 74px;
    height: 74px;
    min-width: 74px;
    min-height: 74px;
    font-size: 32px;
    font-weight: 600;
    line-height: 38.73px;
    text-align: center;
    color: #fff;
}

.suppliers-container .fit-step:hover {
    transform: translateX(5px);
    box-shadow: 0px 0px 10px rgba(0, 0, 0, .1);
}

.suppliers-container .existing-suppliers-section {
    text-align: left;
}

.suppliers-container .supplier-logos {
    display: flex;
    justify-content: space-around;
    flex-wrap: wrap;
}

.suppliers-container .logo-placeholder {
    width: 100px;
    height: 50px;
    background-color: #e9ecef;
    margin: 10px;
    transition: transform 0.3s ease;
}

.suppliers-container .logo-placeholder:hover {
    transform: scale(1.1);
}

.suppliers-container .steps-section {
    display: flex;
    flex-flow: column;
    gap: 20px;
    box-sizing: border-box;
}

.suppliers-container .steps {
    display: grid;
    justify-content: center;
    align-items: center;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
}

.suppliers-container .step {
    background-color: #343a40;
    color: #fff;
    border-radius: 20px;
    padding: 20px;
    position: relative;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    text-align: left;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 210px;
    box-sizing: border-box;
}

.suppliers-container .step-content {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 100%;
}

.suppliers-container .step-number {
    width: fit-content;
    background-color: #78e1c2;
    color: #343a40;
    font-weight: normal;
    font-size: 14px;
    padding: 5px 15px;
    border-radius: 50px;
    display: inline-block;
    margin-bottom: 10px;
}

.suppliers-container .step:hover {
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.suppliers-container .step p {
    width: 80%;
    font-size: 18px;
    font-weight: 400;
    line-height: 21.6px;
    letter-spacing: -0.02em;
    text-align: left;
}

.suppliers-container .arrow-shape {
    position: absolute;
    width: 30px;
    height: 25px;
    fill: #343a40;
}

.suppliers-container .right-arrow {
    top: 50%;
    right: -20px;
    transform: translateY(-50%);
}

.suppliers-container .down-arrow {
    bottom: -20px;
    left: 50%;
    transform: translateX(-50%) rotate(90deg);
}

.suppliers-container .steps .step.last-step {
    grid-column: span 4;
    background: url('@/assets/lastStepbackground.png') no-repeat center center;
    display: flex;
    object-fit: contain;
    background-size: cover;
    flex-direction: column;
    height: 211px;
    border-radius: 20px;
    overflow: hidden;
}

.suppliers-container .steps .step.last-step p {
    font-size: 32px;
    font-weight: 600;
    line-height: 38.4px;
    letter-spacing: -0.02em;
    text-align: left;
}

.suppliers-container .join-section {
    display: flex;
    flex-flow: column;
    justify-content: space-between;
    background: linear-gradient(90deg, rgba(255, 118, 20, 1) 0%, rgba(255, 68, 100, 1) 100%);
    padding: 40px 100px;
    height: 440px;
    margin-bottom: 50px;
    border-radius: 20px;
    text-align: left;
    color: #fff;
    box-sizing: border-box;
}

.suppliers-container .join-section h2 {
    font-size: 32px;
    font-weight: 600;
    line-height: 1.5;
    margin-bottom: 10px;
    color: #fff;
}

.suppliers-container .join-section p {
    font-size: 24px;
    font-weight: 400;
    line-height: 1.5;
    margin-bottom: 20px;
}

@media (max-width: 768px) {
    .suppliers-container {
        gap: 40px;
        padding: 0 20px;
    }

    .suppliers-container .intro-section {
        padding: 20px;
        height: auto;
    }

    .suppliers-container .fit-step {
        width: 100% !important;
        max-width: none;
    }

    .suppliers-container .intro-content {
        flex-direction: column;
        align-items: flex-start;
    }

    .suppliers-container .intro-text {
        max-width: 100%;
        text-align: left;
    }

    .suppliers-container .why-benefits, .benefits, .fit-steps, .supplier-logos {
        width: 100%;
        max-width: none;
        flex-direction: column;
        align-items: center;
    }

    .suppliers-container .why-benefit, .benefit-card, .fit-step {
        width: 100%;
        max-width: none;
    }

    .suppliers-container .arrow-shape {
        display: none;
    }

    .suppliers-container .steps-section .steps {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 20px;
    }

    .suppliers-container .steps-section .steps .step {
        width: 100%;
    }

    .suppliers-container .steps-section .steps .step.last-step {
        font-size: 28px;
        max-width: 100%;
    }

    .suppliers-container .steps-section .steps .step.last-step p {
        width: 100%;
        font-size: 26px;
    }

}

@media (max-width: 480px) {
    .suppliers-container {
        padding: 0 10px;
    }

    .suppliers-container .intro-text h1 {
        font-size: 24px;
    }

    .suppliers-container .intro-text p {
        font-size: 14px;
    }

    .suppliers-container .fit-step {
        width: 100% !important;
    }

    .suppliers-container .fit-step h3 {
        font-size: 18px;
    }

    .suppliers-container .fit-step p {
        font-size: 14px;
        padding: 0;
        width: 100%;
        min-width: 340px;
    }

    .suppliers-container .fit-step:last-child p {
        font-size: 14px;
        padding: 0;
    }

    .suppliers-container .steps-section .steps {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 20px;
    }

    .suppliers-container .steps-section .steps .step {
        width: 100%;
        max-width: 400px;
    }

    .suppliers-container .steps-section .steps .step.last-step {
        width: 100%;
        max-width: 100%;
    }
}

</style>
