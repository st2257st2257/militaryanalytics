<template>
    <div v-if="formData" class="legal-info">
        <h2>Юридическая информация</h2>
        <CustomForm :formData="formData" title="Юридическая информация" :requests="requests" submitButtonText="Сохранить">
            <template v-slot="{ formData, errors, handleInputError, submitted }">
                <CustomInput
                    label="Юридическое название"
                    variableName="companyName"
                    v-model="formData.companyName"
                    inputType="input"
                    placeholder="Введите название организации"
                    note="Укажите название компании, именно это будет отображаться в поле 'Продавец'"
                    :error="errors.companyName"
                    :shouldShowError="submitted"
                    required
                    @input-error="handleInputError"
                />
                <CustomInput
                    label="ИНН"
                    variableName="inn"
                    v-model="formData.inn"
                    inputType="input"
                    placeholder="Введите ИНН"
                    :validationFunction="validateINN"
                    :error="errors.inn"
                    :shouldShowError="submitted"
                    required
                    @input-error="handleInputError"
                />
                <CustomInput
                    label="КПП"
                    variableName="kpp"
                    v-model="formData.kpp"
                    inputType="input"
                    placeholder="Введите КПП"
                    :validationFunction="validateKPP"
                    :error="errors.kpp"
                    :shouldShowError="submitted"
                    required
                    @input-error="handleInputError"
                />
                <CustomInput
                    label="ОГРН"
                    variableName="ogrn"
                    v-model="formData.ogrn"
                    inputType="input"
                    placeholder="Введите ОГРН"
                    :validationFunction="validateOGRN"
                    :error="errors.ogrn"
                    :shouldShowError="submitted"
                    required
                    @input-error="handleInputError"
                />
                <CustomInput
                    label="Юридический адрес"
                    variableName="legalAddress"
                    v-model="formData.legalAddress"
                    inputType="input"
                    placeholder="Введите юридический адрес"
                    :error="errors.legalAddress"
                    :shouldShowError="submitted"
                    required
                    @input-error="handleInputError"
                />
                <CustomInput
                    label="Фактический адрес"
                    variableName="factAddress"
                    v-model="formData.factAddress"
                    inputType="input"
                    placeholder="Введите фактический адрес"
                    :error="errors.factAddress"
                    :shouldShowError="submitted"
                    @input-error="handleInputError"
                />
                <span style="margin-top: 15px; display: flex; flex-flow: column; gap: 10px;">
                    <h4>Карточка компании</h4>
                    <div style="display: flex; gap: 15px;">
                        <file-uploader
                            icon="@/assets/icons/saveFiles.svg"
                            @file-upload="onFileUpload"
                        />
                        <a class="btn" v-if="uploadedFile && uploadedFile.file_static_url" :href="uploadedFile.file_static_url">Скачать карточку компании</a>
                    </div>
                </span>
            </template>
        </CustomForm>
    </div>
    <LoadingController v-else :fetchData="initializeFormData" />
</template>

<script>
import CustomForm from '@/components/inputs/CustomForm.vue';
import CustomInput from '@/components/inputs/CustomInput.vue';
import FileUploader from '@/components/inputs/FileUploader.vue';
import LoadingController from '@/components/LoadingController.vue';
import { mapGetters, mapActions } from 'vuex';
import api from '@/authAPI.js';

export default {
    components: {
        CustomForm,
        CustomInput,
        FileUploader,
        LoadingController
    },
    computed: {
        ...mapGetters('user', ['currentUser']),
    },
    data() {
        return {
            formData: null,
            uploadedFile: null,
            originalUserData: null,
            requests: [
                {
                    url: '/set/',
                    createPayload: this.createUserPayload
                },
                {
                    url: '/upload_file/',
                    createPayload: this.createFilePayload
                }
            ]
        };
    },
    mounted() {
        this.initializeFormData();
    },
    methods: {
        ...mapActions('user', ['fetchUserData', 'updateUser']),
        async fetchCompanyCard() {
            const formData = new FormData();
            formData.append('action', 'getFileName');
            formData.append('fileName', 'legal_document');
            formData.append('userOwner', this.currentUser.username);

            try {
                const response = await api.post('/get_file/', formData);
                this.uploadedFile = response.data;
            } catch (error) {
                console.error('Error fetching company card:', error);
            }
        },
        async initializeFormData() {
            if (this.currentUser) {
                try {
                    const userData = await this.fetchUserData(this.currentUser.username);
                    
                    this.formData = {
                        companyName: userData.companyName,
                        inn: userData.inn,
                        kpp: userData.kpp,
                        ogrn: userData.ogrn,
                        legalAddress: userData.legalAddress,
                        factAddress: userData.factAddress
                    };
                    this.originalUserData = { ...this.formData };
                    await this.fetchCompanyCard();
                } catch (error) {
                    console.error('Error initializing form data:', error);
                    throw error
                }
            }
        },
        onFileUpload(file) {
            this.uploadedFile = file;
        },
        createUserPayload(data, username) {
            const formData = new FormData();
            formData.append('userLogin', username);
            formData.append('classToEdit', 'UserSuperSet');

            const fieldsToUpdate = {};
            for (const key in data) {
                if (data.hasOwnProperty(key) && data[key] !== 0) {
                    fieldsToUpdate[key] = data[key];
                }
            }

            formData.append('fieldsNames', JSON.stringify(fieldsToUpdate));
            return formData;
        },
        createFilePayload() {
            if (!this.uploadedFile || !this.uploadedFile.lastModified) {
                return null;
            }

            const formData = new FormData();
            formData.append('action', 'addOneFile');
            formData.append('className', 'User');
            formData.append('userOwner', this.currentUser.username);
            formData.append('objectType', 'pdf');
            formData.append('fileName', 'legal_document');
            formData.append('fileData', this.uploadedFile);
            return formData;
        },
        validateINN(value) {
            const innRegex = /^\d{10}$|^\d{12}$/;
            if (!value) {
                return 'ИНН обязателен для заполнения';
            } else if (!innRegex.test(value)) {
                return 'ИНН должен содержать 10 или 12 цифр';
            }
            return '';
        },
        validateOGRN(value) {
            const ogrnRegex = /^\d{13}$/;
            if (!value) {
                return 'ОГРН обязателен для заполнения';
            } else if (!ogrnRegex.test(value)) {
                return 'ОГРН должен содержать 13 цифр';
            }
            return '';
        },
        validateKPP(value) {
            const kppRegex = /^\d{9}$/;
            if (!value) {
                return 'КПП обязателен для заполнения';
            } else if (!kppRegex.test(value)) {
                return 'КПП должен содержать 9 цифр';
            }
            return '';
        }
    }
};
</script>

<style scoped>
.legal-info {
  display: flex;
  flex-flow: column;
  width: 100%;
  height: fit-content;
  padding: 10px;
  border-radius: 15px;
  background: var(--color-background-soft);
}

@media (max-width: 1345px) {
  .legal-info {
    width: 100%;
    flex-flow: column;
  }
}
</style>
