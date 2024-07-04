<template>
    <div class="recovery-password">
        <h2>Восстановление пароля</h2>
        <CustomForm v-if="step === 1" :formData="emailData" title="" submitUrl="/user/recovery/" :createPayload="createEmailPayload" submitButtonText="Восстановить" @submit-success="handleStepChange" @submit-error="handleError">
            <template v-slot="{ formData, errors, handleInputError, submitted }">
                <CustomInput
                    label="Электронная почта"
                    variableName="email"
                    v-model="formData.email"
                    inputType="input"
                    placeholder="Введите вашу почту"
                    :error="errors.email"
                    :shouldShowError="submitted"
                    @input-error="handleInputError"
                />
                <div v-if="errors.global" class="error-message">{{ errors.global }}</div>
            </template>
        </CustomForm>
        <CustomForm v-if="step === 2" :formData="passwordData" title="" submitUrl="/user/recovery/" :createPayload="createPasswordPayload" submitButtonText="Изменить пароль" @submit-error="handleError">
            <template v-slot="{ formData, errors, handleInputError, submitted }">
                <CustomInput
                    label="Код"
                    variableName="token"
                    v-model="formData.token"
                    inputType="input"
                    placeholder="Введите полученный код"
                    :error="errors.token"
                    :shouldShowError="submitted"
                    @input-error="handleInputError"
                />
                <CustomInput
                    label="Новый пароль"
                    variableName="password"
                    v-model="formData.password"
                    inputType="password"
                    placeholder="Введите новый пароль"
                    :validationFunction="validatePassword"
                    :error="errors.password"
                    :shouldShowError="submitted"
                    @input-error="handleInputError"
                />
                <CustomInput
                    label="Повторите новый пароль"
                    variableName="repeatPassword"
                    v-model="formData.repeatPassword"
                    inputType="password"
                    placeholder="Повторите новый пароль"
                    :validationFunction="(value) => validateRepeatPassword(value, formData.password)"
                    :error="errors.repeatPassword"
                    :shouldShowError="submitted"
                    @input-error="handleInputError"
                />
                <div v-if="errors.global" class="error-message">{{ errors.global }}</div>
            </template>
        </CustomForm>
    </div>
</template>

<script>
import CustomForm from '@/components/inputs/CustomForm.vue';
import CustomInput from '@/components/inputs/CustomInput.vue';
import { validatePassword, validateRepeatPassword } from '@/utils/validation';

export default {
    components: {
        CustomForm,
        CustomInput,
    },
    data() {
        return {
            step: 1,
            emailData: {
                email: '',
            },
            passwordData: {
                token: '',
                password: '',
                repeatPassword: '',
            }
        };
    },
    methods: {
        createEmailPayload(data) {
            const formData = new FormData();
            formData.append('actionType', 'sendRecoveryLink');
            formData.append('user', data.email);
            return formData;
        },
        createPasswordPayload(data) {
            const formData = new FormData();
            formData.append('actionType', 'getRecoveryLink');
            formData.append('token', data.token);
            formData.append('pass1', data.password);
            formData.append('pass2', data.repeatPassword);
            return formData;
        },
        handleStepChange() {
            this.step = 2;
        },
        handleError(error) {
            if (error.response && error.response.data) {
                const errors = error.response.data.errors || {};
                this.$emit('submit-error', errors);
            } else {
                this.$emit('submit-error', { global: 'Произошла ошибка, попробуйте еще раз.' });
            }
        },
        validatePassword,
        validateRepeatPassword
    }
};
</script>

<style scoped>
.recovery-password {
    display: flex;
    flex-flow: column;
    width: 100%;
    max-width: 600px;
    height: fit-content;
    padding: 20px !important;
    border-radius: 10px;
    background: var(--color-background-soft);
}

.error-message {
    color: red;
    margin-top: 10px;
}
</style>
