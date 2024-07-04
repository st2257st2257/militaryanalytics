<template>
    <div class="settings-view">
        <h2>Безопасность</h2>
        <CustomForm :formData="emailData" title="Привязать почту" :requests="emailRequest" submitButtonText="Изменить">
            <template v-slot="{ formData, errors, handleInputError, submitted }">
                <CustomInput
                    label="Электронная почта"
                    variableName="email"
                    v-model="formData.email"
                    inputType="input"
                    placeholder="Введите ваш email"
                    :error="errors.email"
                    :shouldShowError="submitted"
                    @input-error="handleInputError"
                />
            </template>
        </CustomForm>
        <CustomForm :formData="passwordData" title="Изменить пароль" :requests="passwordRequest" submitButtonText="Изменить пароль">
            <template v-slot="{ formData, errors, handleInputError, submitted }">
                <CustomInput
                    label="Новый пароль"
                    variableName="password"
                    v-model="formData.password"
                    inputType="password"
                    placeholder="Введите новый пароль"
                    :validationFunction="validatePassword"
                    :error="errors.password"
                    :required="true"
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
                    :required="true"
                    :shouldShowError="submitted"
                    @input-error="handleInputError"
                />
            </template>
        </CustomForm>
    </div>
</template>

<script>
import CustomForm from '@/components/inputs/CustomForm.vue';
import CustomInput from '@/components/inputs/CustomInput.vue';
import { validatePassword, validateRepeatPassword } from '@/utils/validation';
import { mapGetters, mapActions } from 'vuex';

export default {
    components: {
        CustomForm,
        CustomInput,
    },
    computed: {
        ...mapGetters('user', ['currentUser']),
    },
    data() {
        return {
            emailData: {
                email: '',
            },
            passwordData: {
                password: '',
                repeatPassword: '',
            },
            emailRequest: {
                url: '/set/',
                createPayload: this.createEmailPayload
            },
            passwordRequest: {
                url: '/set/',
                createPayload: this.createPasswordPayload
            }
        };
    },
    mounted() {
        this.initializeFormData();
    },
    methods: {
        ...mapActions('user', ['fetchUserData', 'updateUser']),
        async initializeFormData() {
            if (this.currentUser) {
                await this.fetchUserData(this.currentUser.username);
                this.emailData.email = this.currentUser.email;
            }
        },
        createEmailPayload(data, username) {
            const formData = new FormData();
            formData.append('userLogin', username);
            formData.append('classToEdit', 'UserSuperSet');

            const fieldsNames = {};
            for (const key in data) {
                if (data.hasOwnProperty(key)) {
                    fieldsNames[key] = data[key];
                }
            }

            formData.append('fieldsNames', JSON.stringify(fieldsNames));
            return formData;
        },
        createPasswordPayload(data, username) {
            const formData = new FormData();
            formData.append('userLogin', username);
            formData.append('classToEdit', 'UserSuperSet');

            const fieldsNames = {};
            for (const key in data) {
                if (data.hasOwnProperty(key)) {
                    fieldsNames[key] = data[key];
                }
            }

            formData.append('fieldsNames', JSON.stringify(fieldsNames));
            return formData;
        },
        validatePassword,
        validateRepeatPassword
    }
};
</script>

<style scoped>
.settings-view {
    display: flex;
    flex-flow: column;
    width: 100%;
    height: fit-content;
    padding: 10px;
    border-radius: 15px;
    background: var(--color-background-soft);
}

@media (max-width: 1345px) { 
    .settings-view {
        width: 100%;
        flex-flow: column;
    }
}
</style>
