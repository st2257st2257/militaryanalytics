<template>
    <ModalWindow ref="leasingModal" title="Заявка на лизинг">
        <template #content>
            <div class="item-preview">
                <img v-if="item.appends" :src="item.appends.settings.link1.value">
                <span>
                    <p>{{ item.name }}</p>
                    <p>{{ item.price + " руб"}}</p>
                </span>
            </div>
            <form @submit.prevent="handleSubmit">
                <CustomInput
                    label="ФИО"
                    v-model="formData.fullName"
                    inputType="input"
                    placeholder="Ваше ФИО"
                    :required="true"
                    :isInvalid="errors.fullName"
                />
                <CustomInput
                    label="Почта"
                    v-model="formData.email"
                    inputType="input"
                    placeholder="Ваш email"
                    type="email"
                    :required="true"
                    :isInvalid="errors.email"
                />
                <CustomInput
                    label="Компания"
                    v-model="formData.companyName"
                    inputType="input"
                    placeholder="Название компании"
                    :required="true"
                    :isInvalid="errors.companyName"
                />
                <CustomInput
                    label="Телефон"
                    v-model="formData.phone"
                    inputType="input"
                    placeholder="Ваш телефон"
                    type="tel"
                />
                <CustomInput
                    label="Сообщение"
                    v-model="formData.message"
                    inputType="textarea"
                    placeholder="Ваше сообщение"
                    fileLoader
                    accept=".pdf,.doc,.docx,.xls,.xlsx"
                    @change="handleFileChange"
                />
            </form>
        </template>
        <template #buttons>
            <button class="btn green-btn" type="submit" @click="handleSubmit">Отправить</button>
        </template>
    </ModalWindow>
</template>

<script>
import { mapGetters } from 'vuex';
import ModalWindow from '@/components/modals/ModalWindow.vue';
import CustomInput from '@/components/inputs/CustomInput.vue';
import api from '@/authAPI';

export default {
    components: {
        ModalWindow,
        CustomInput,
    },
    computed: {
        ...mapGetters('user', ['currentUser', 'isAuthenticated'])
    },
    data() {
        return {
            item: [],
            formData: {
                action: 'setOne',
                fullName: '',
                email: '',
                phone: '',
                companyName: '',
                message: '',
                file: null,
                quantity: '',
                productId: ''
            },
            errors: {
                fullName: false,
                email: false,
                companyName: false,
            }
        };
    },
    methods: {
        handleFileChange(file) {
            this.formData.file = file;
        },
        validateForm() {
            this.errors.fullName = !this.formData.fullName.trim();
            this.errors.email = !this.formData.email.trim();
            this.errors.companyName = !this.formData.companyName.trim();
            return !this.errors.fullName && !this.errors.email && !this.errors.companyName;
        },
        async handleSubmit() {
            if (!this.validateForm()) {
                window.notificationManager.addNotification('error', 'Заполните обязательные поля');
                return;
            }

            const formDataToSend = new FormData();
            Object.keys(this.formData).forEach(key => {
                formDataToSend.append(key, this.formData[key]);
            });

            try {
                const response = await api.post('/products/set/', formDataToSend);
                window.notificationManager.addNotification('success', 'Ваше обращение отправлено менеджеру', 3000, true, () => {
                    this.$refs.leasingModal.close();
                });
            } catch (error) {
                window.notificationManager.addNotification('error', 'Произошла ошибка при отправке данных');
            }
        },
        open(item) {
            console.log(item)
            this.item = item;
            this.formData.productId = item.id;
            this.formData.quantity = 1;
            if (this.isAuthenticated) {
                this.formData.fullName = `${this.currentUser.firstNM} ${this.currentUser.secondNM}` || "";
                this.formData.email = this.currentUser.email || "";
                this.formData.phone = this.currentUser.phone || "";
                this.formData.companyName = this.currentUser.companyName || "";
            } else {
                this.formData.fullName = '';
                this.formData.email = '';
                this.formData.phone = '';
                this.formData.companyName = '';
            }
            this.formData.message = 'Хочу в лизинг этот товар';

            this.$refs.leasingModal.open();
        },
    },
    mounted() {
        window.leasingModal = this;
    },
};
</script>

<style scoped>
input[required] {
    border-color: red;
}

input[is-invalid="true"] {
    border-color: red;
}

label {
    display: flex;
    justify-content: space-between;
}

label .required {
    color: red;
    padding-left: 5px;
}

.item-preview {
    display: flex;
    width: 100%;
    gap: 10px;
}

.item-preview img {
    max-width: 80px;
    height: 80px;
    object-fit: contain;
}
</style>
