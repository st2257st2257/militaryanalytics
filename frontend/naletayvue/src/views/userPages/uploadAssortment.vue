<template>
    <div class="profile_info">
        <div class="profile_section upload_section">
            <h2>Загрузка товаров</h2>
            <productUpload />
        </div>
        <div class="profile_section">
            <details class="info">
                <summary style="background: var(--color-background-error); color: var(--color-active-text)" @click="toggleArrow('info')" :class="{'open': openInfo}">
                    ОСНОВНЫЕ РЕКОМЕНДАЦИИ ПО ЗАПОЛНЕНИЮ
                    <span class="arrow"><arrowIcon/></span>
                </summary>
                <div style="padding: 15px;">
                    <p style="color: var(--color-background-error)">ОЗНАКОМЬТЕСЬ ВНИМАТЕЛЬНО:</p>
                    <ul>
                        <li>Чем подробнее информация в шаблоне, тем конкурентнее продукт на маркетплейсе.</li>
                        <li>В шаблонах запрещено менять что-либо, допустимо только заполнение (не удалять и не менять местами столбцы). Иначе информация не загрузится на платформу.</li>
                        <li>В ячейки необходимо вносить только значения, без единиц измерения и пр.</li>
                        <li>Если у вас нет данных для внесения в ячейку, необходимо очистить ее (не ставьте «0», «-» и прочие символы).</li>
                        <li>Ссылки на изображения и документы должны быть прямыми (не на папку, не на скачивание файла – только на само изображение). Иначе информация не загрузится на платформу, а продукты/услуги без изображения не принимаются к размещению на маркетплейсе.</li>
                    </ul>
                </div>
            </details>
            <details class="templates">
                <summary @click="toggleArrow('templates')" :class="{'open': openTemplates}">
                    Шаблоны
                    <span class="arrow"><arrowIcon/></span>
                </summary>
                <div style="padding: 15px;">
                    <div style="padding-left: 15px;">
                        <ul>
                            <li><a class="link" :href="getBackendURL('/static/excel/services.xlsx')" target="_blank">Шаблон для услуг</a></li>
                            <li><a class="link" :href="getBackendURL('/static/excel/products.xlsx')" target="_blank">Шаблон для товаров</a></li>
                        </ul>
                    </div>
                </div>
            </details>
            <div style="display: flex; gap: 15px; flex-flow: column; padding: 10px; border-radius: 15px; background: var(--color-background-soft);">
                <h2>Выгрузка списка товаров</h2>
                <CustomInput
                    label="Выберите шаблон"
                    variableName="selectedTemplate"
                    v-model="selectedTemplate"
                    :options="templateOptions"
                    inputType="select"
                />
                <button @click="downloadTemplate" style="padding: 15px;" class="btn green-btn">Выгрузить</button>
            </div>
        </div>
    </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import CustomInput from '@/components/inputs/CustomInput.vue';
import productUpload from '@/components/productUpload.vue';
import arrowIcon from '@/assets/icons/arrow.svg'
import api from '@/authAPI.js';

export default {
    components: {
        productUpload,
        CustomInput,
        arrowIcon
    },
    data() {
        return { 
            openInfo: false,
            openTemplates: false,
            selectedTemplate: '',
            templateOptions: [
                { label: 'Услуги', value: 'urlServ' },
                { label: 'Беспилотники', value: 'urlComm' },
                { label: 'Дронопорты', value: 'urlDronHub' },
            ]
        };
    },
    computed: {
        ...mapGetters('user', ['currentUser', 'isAuthenticated'])
    },
    methods: {
        ...mapActions('user', ['login', 'logout']),
        toggleArrow(section) {
            if (section === 'info') {
                this.openInfo = !this.openInfo;
            } else if (section === 'templates') {
                this.openTemplates = !this.openTemplates;
            }
        },
        getBackendURL(path) {
            return `${api.getBackendURL()}${path}`;
        },
        async downloadTemplate() {
            if (this.selectedTemplate) {
                try {
                    const formData = new FormData();
                    formData.append('userLogin', this.currentUser.username);
                    formData.append('classToEdit', "User");
                    formData.append('fieldName', this.selectedTemplate);

                    const response = await api.post('/get/', formData, {
                        responseType: 'blob'
                    });

                    if (response.data.size) {
                        const blob = new Blob([response.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
                        const url = URL.createObjectURL(blob);
                        const link = document.createElement('a');
                        link.href = url;
                        link.download = 'template.xlsx';
                        document.body.appendChild(link);
                        link.click();
                        document.body.removeChild(link);
                        URL.revokeObjectURL(url);
                    } else {
                        window.notificationManager.addNotification('error', 'Нет шаблона который можно выгрузить');
                    }
                } catch (error) {
                    console.error(error);
                    window.notificationManager.addNotification('error', 'Ошибка при получении ссылки на скачивание');
                }
            } else {
                window.notificationManager.addNotification('error', 'Пожалуйста, выберите шаблон для выгрузки.');
            }
        }
    },
    mounted() {
        if (!this.isAuthenticated) {
            window.loginModal.open();
        }
    }
};
</script>


<style scoped>
.info {
    display: flex;
    flex-flow: column;
    border-radius: 15px;
}

.info h2 {
    display: flex;
    font-size: 16px;
    color: var(--color-background-error);
    font-weight: 700;
}

.info ul {
    padding-left: 25px;
}

.info li {
    margin-bottom: 10px;
}

summary {
    display: flex;
    justify-content: space-between;
    align-items: center;
    cursor: pointer;
    font-size: 16px;
    font-weight: bold;
    padding: 15px;
    background: var(--color-background-soft);
    border-radius: 10px;
}

.arrow {
    width: 22px;
    height: 22px;
    font-size: 20px;
    font-weight: 800;
    display: inline-block;
    transition: transform 0.3s ease;
}

.arrow svg{
    width: 22px;
    height: 22px;
}

.open .arrow {
    transform: rotate(90deg);
}

.userPage_container {
    display: flex;
    align-items: flex-start;
    text-align: left;
    flex-flow: row wrap;
    height: 100%;
    width: 100%;
    max-width: 1280px;
    gap: 15px;
    box-sizing: border-box;
}

.profile_info {
    display: flex;
    width: 100%;
    flex-flow: row wrap;
    border-radius: 15px;
    gap: 15px;
}

.templates {
    display: flex;
    flex-flow: column;
    border-radius: 15px;
}



.settings_container {
    display: flex;
    flex-flow: row wrap;
    width: 100%;
}

.profile_section {
    display: flex;
    flex-flow: column;
    width: 90%;
    height: fit-content;
    gap: 10px;
    flex: 0.9;
    padding: 10px;
    border-radius: 15px;
}

.upload_section {
    background: var(--color-background-soft);
}

@media (max-width: 1345px) {
    .profile_info {
        flex-flow: column;
    }

    .profile_section {
        width: 100%;
        margin-bottom: 15px;
    }
}
</style>
