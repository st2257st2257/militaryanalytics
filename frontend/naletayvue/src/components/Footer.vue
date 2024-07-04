<template>
        <div class="background"></div>
    <footer class="main-footer">
    <div class="footer-container">
        <!-- Навигация -->
        <div class="first-stage">
            <NaletayLogo class="org-logo naletay" />
            <GTLKLogo class="org-logo gtlk" />
        </div>

        <div class="second-stage">
            <div class="footer-column">
                <h3>Навигация</h3>
                <ul>
                    <li><router-link :to="{ path: '/catalog', query: { type: 'commodity' }}">Каталог товаров БАС</router-link></li>
                    <li><router-link :to="{ path: '/catalog', query: { type: 'service' }}">Каталог услуг БАС </router-link></li>
                    <li><router-link to="/">Контакты</router-link></li>
                </ul>
            </div>
            <!-- Помощь -->
            <div class="footer-column">
                <h3>Помощь</h3>
                <ul>
                    <li><a href="/docs/privacy_policy.docx" target="_blank">Политика конфиденциальности</a></li>
                    <li><a href="/docs/user_agreement.docx" target="_blank">Пользовательское соглашение</a></li>
                    <li><a href="/docs/consent_to_process_personal_data.docx" target="_blank">Согласие на обработку пресональных данных</a></li>
                    <li><a href="/docs/сontract_sale.docx" target="_blank">Договор использования платформы</a></li>
                    <!--<li><router-link to="/">Бонусы и промоакции</router-link></li>-->
                </ul>
            </div>
            <!-- Контакты -->
            <div class="footer-column">
                <h3>Контакты</h3>
                <!--<p>Телефон: +7 (123) 456-7890</p>-->
                <p>Email: info@naletai.su</p>
                <p>Адрес: Москва, Ленинградский проспект 31Ас1</p>
            </div>
            <!-- Подписка на рассылку -->
            <div class="footer-column">
                <h3>Подпишитесь на рассылку</h3>
                <div class="subscribe-form">
                    <custom-input 
                    @send="connectMailing()" 
                    :showSendButton="true" 
                    inputType="input" 
                    v-model="email" 
                    placeholder="Введите ваш email." />
                </div>
                <div class="social-icons">
                </div>
            </div>

            <div class="third-stage">
                2024 © Налетай
            </div>

        </div>
    </div>
    </footer>
</template>

<script>
import NaletayLogo from '@/assets/icons/logo_naletay.svg'
import GTLKLogo from '@/assets/icons/logo_gtlk.svg'
import CustomInput from '@/components/inputs/CustomInput.vue';
//import api from '@/authAPI.js';   

export default {
    components: {
        NaletayLogo,
        GTLKLogo,
        CustomInput
    },
    data() {
        return {
            email: ''
        };
    },
    methods: {
        async connectMailing() {
            window.notificationManager.addNotification('success', `Вы подписались на рассылку`);
           /* try {
                const response = await api.post('/user/form/', formData, {
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    }
                });
                window.notificationManager.addNotification('success', `Вы подписались на рассылку`);
            } catch (error) {
                console.error('Произошла ошибка при отправке данных:', error);
            }*/
        },
        toggleTheme() {
            if (localStorage.getItem('theme') === 'dark') {
                localStorage.setItem('theme', 'light');
            } else {
                localStorage.setItem('theme', 'dark');
            }
            this.applyTheme();
        },
        applyTheme() {
            const theme = localStorage.getItem('theme') || 'light';
            document.documentElement.setAttribute('data-theme', theme);
        }
    },
    mounted() {
        this.applyTheme();
    }
};
</script>

<style scoped>

.main-footer {
    position: relative;
    z-index: 1;
    display: flex;
    flex-shrink: 0;
    justify-content: center;
    align-items: center;
    width: 100vw;
    background-color: var(--color-background-footer);
    color: var(--color-text);
    transition: color 0.5s, background-color 0.5s;
    overflow: hidden;
}

.footer-container {
    position: relative;
    display: flex;
    flex-flow: column;
    width: 100%;
    max-width: 1440px;
    padding: 50px 25px 50px 25px;
    min-height: 80px;
    height: 100%;
    align-items: flex-start;
    box-sizing: border-box;
}

.subscribe-form {
    margin-bottom: 10px;
}

.footer-column ul{
    list-style-type: none;
}

.footer-column ul li, p{
    color: var(--color-active-text);
    margin-top: 8px;
}

.footer-column a{
    color: var(--color-active-text);
}

.footer-column h3{
    color: #7E858C;
}

.subscribe-form input {
    width: 100%;
    padding: 8px;
    margin-bottom: 5px;
    border: 1px solid #ccc;
    border-radius: 5px;
}

.social-icons img {
    width: 30px;
    height: 30px;
    margin-right: 10px;
}

.organization {
    display: flex;
    flex-flow: column;
    justify-content: center;
    align-items: flex-start;
}

.first-stage {
    display: flex;
    width: 100%;
    max-width: 320px;
    margin-bottom: 40px;
}

.second-stage {
    display: grid;
    width: 100%;
    grid-template-columns: repeat(auto-fit, minmax(200px, 23%));
    gap: 20px;
    grid-template-rows: auto auto;
}

.third-stage {
    color: #7E858C;
}

.org-logo {
    width: 100%;
    min-width: 150px;
    min-height: 32px;
    object-fit: contain;
}

.org-rights {
    margin-left: 15px;
    font-size: 0.6rem;
    color: #000;
    opacity: 30%;
    font-weight: 600;
}

.theme-toggle {
    cursor: pointer;
    border: none;
    background: none;
    font-size: 0.9rem;
    color: var(--color-text);
    transition: color 0.5s;
    min-width: fit-content;
}

.theme-toggle:hover {
    color: var(--vt-c-indigo);
}

.background {
    z-index: -1;
    position: absolute;
    width: 20%;
    height: 300px;
    bottom: 300px;
    left:40%;
    right: 50%;
    background: var(--color-btn-green-background);
    border-radius: 100%;
    filter: blur(200px);
}

</style>
