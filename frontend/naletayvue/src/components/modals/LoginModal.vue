<template>
    <ModalWindow ref="loginModal" :title="isLoginMode ? 'Авторизация' : 'Регистрация'">
        <template #content>
            <CustomInput 
                label="Электронная почта" 
                variableName="username" 
                v-model="username" 
                inputType="input" 
                placeholder="Электронная почта" 
            />
            <CustomInput 
                v-if="!isLoginMode" 
                label="Название компании" 
                variableName="companyName" 
                v-model="companyName" 
                inputType="input" 
                placeholder="Название компании" 
            />
            <CustomInput 
                label="Пароль" 
                variableName="password" 
                v-model="password" 
                inputType="password" 
                placeholder="Пароль" 
            />
            <CustomInput 
                v-if="!isLoginMode" 
                label="Подтвердите пароль" 
                variableName="confirmPassword" 
                v-model="confirmPassword" 
                inputType="password" 
                placeholder="Подтвердите пароль" 
            />
            <router-link class="link" to="/recovery" style="min-width: 125px; margin-left: 5px; margin-top: 5px" @click="forgotPassword">
                Забыли пароль?
            </router-link>
        </template>
        <template #buttons>
            <button class="btn green-btn" style="min-width: 125px; color: var(--color-active-text);" @click="handleAuthorisation()">
                {{ isLoginMode ? 'Войти' : 'Зарегистрироваться' }}
            </button>
            <button class="btn soft-btn" style="min-width: 125px;" @click="toggleMode()">
                {{ isLoginMode ? 'Регистрация' : 'Есть аккаунт' }}
            </button>
        </template>
    </ModalWindow>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import ModalWindow from '@/components/modals/ModalWindow.vue';
import CustomInput from '@/components/inputs/CustomInput.vue';

export default {
    components: {
        ModalWindow,
        CustomInput
    },
    data() {
        return {
            username: '',
            password: '',
            confirmPassword: '',
            companyName: '',
            isLoginMode: true,
            modalClosed: false,
            timer: null,
        };
    },
    computed: {
        ...mapGetters('user', ['isAuthenticated'])
    },
    methods: {
        ...mapActions('user', ['login', 'registration']),
        handleInput(field, event) {
            this[field] = event.target.value;
        },
        toggleMode() {
            this.isLoginMode = !this.isLoginMode;
            this.resetForm();
        },
        async handleAuthorisation() {
            if (this.isLoginMode) {
                const result = await this.login({ username: this.username, password: this.password });
                this.handleResult(result);
            } else {
                const result = await this.registration({
                    username: this.username,
                    password: this.password,
                    repeat_password: this.confirmPassword,
                    company_name: this.companyName
                });
                this.handleResult(result);
            }
        },
        handleResult(result) {
            const { success, message } = result;
            if (success) {
                window.notificationManager.addNotification('success', message, 3000, true, () => {
                    this.$refs.loginModal.close();
                });
            } else {
                window.notificationManager.addNotification('error', message);
            }
        },
        forgotPassword() {
            this.$refs.loginModal.close();
        },
        open(mode = '') {
            this.$nextTick(() => {
                if (!this.isAuthenticated) {
                    this.isLoginMode = mode !== 'register';
                    this.resetForm();
                    this.$refs.loginModal.open();
                } else {
                    this.$router.push({ name: 'UserProfile' });
                }
            });
        },
        resetForm() {
            this.username = '';
            this.password = '';
            this.confirmPassword = '';
            this.companyName = '';
        }
    },
    mounted() {
        window.loginModal = this;
    }
}
</script>
