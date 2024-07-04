<template>
    <ModalWindow ref="contactModal" title="Обратная связь">
        <template #content>
            <form @submit.prevent="handleSubmit">
                <CustomInput
                    label="ФИО"
                    v-model="formData.name"
                    inputType="input"
                    placeholder="Ваше ФИО"
                    :required="true"
                    :isInvalid="errors.name"
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
                    label="Телефон"
                    v-model="formData.phone"
                    inputType="input"
                    placeholder="Ваш телефон"
                    type="tel"
                />
                <CustomInput
                    label="Компания"
                    v-model="formData.company"
                    inputType="input"
                    placeholder="Название компании"
                    :required="true"
                    :isInvalid="errors.company"
                />
                <CustomInput
                    label="Сообщение"
                    v-model="formData.message"
                    inputType="textarea"
                    placeholder="Ваше сообщение"
                    :required="true"
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
import api from '@/authAPI.js'

export default {
    components: {
        ModalWindow,
        CustomInput,
    },
    data() {
        return {
            formData: {
                name: '',
                email: '',
                phone: '',
                company: '',
                message: '',
                file: null,
            },
            errors: {
                name: false,
                email: false,
                company: false,
            },
        };
    },
    computed: {
        ...mapGetters('user', ['currentUser', 'isAuthenticated'])
    },
    methods: {
        handleFileChange(file) {
            this.formData.file = file;
        },
        validateForm() {
            this.errors.name = !this.formData.name.trim();
            this.errors.email = !this.formData.email.trim();
            this.errors.company = !this.formData.company.trim();
            return !this.errors.name && !this.errors.email && !this.errors.company;
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
                const response = await fetch(`http://127.0.0.1:8000/form/email/Требуется помощь/${this.formData.name}/${this.formData.email}/${this.formData.phone}/${this.formData.company}/${this.formData.message}`, {
                    method: 'POST',
                    body: formDataToSend
                });

                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                
                window.notificationManager.addNotification('success', 'Ваше обращение отправлено менеджеру', 3000, true, () => {
                    this.$refs.contactModal.close();
                });
            } catch (error) {
                window.notificationManager.addNotification('error', 'Ошибка при отправке данных, заполните все поля');
            }
        },
        open() {
            this.$refs.contactModal.open();
        },
    },
    mounted() {
        if (this.isAuthenticated == true) {
            this.formData = {
                name: this.currentUser.firstNM + " " + this.currentUser.secondNM || "",
                email: this.currentUser.email || "",
                phone: this.currentUser.phone || "",
                company: this.currentUser.companyName || "",
                message: '',
                file: null,
            }
        } else {
            this.formData = {
                name: '',
                email: '',
                phone: '',
                company: '',
                message: '',
                file: null,
            }
        }

        window.contactModal = this;
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

</style>
