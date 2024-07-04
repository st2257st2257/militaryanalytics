<template>
    <div class="upload-form">
        <!-- Выбор типа товара -->
        <CustomInput
            label="Что хотите загрузить?"
            variableName="typeProduct"
            v-model="selectedCategory"
            :options="categoryOptions"
            inputType="select"
            @change="handleProductChange"
        />

        <!-- Загрузчик файла -->
        <file-uploader @file-selected="handleFileSelected" />

        <!-- Кнопка для запуска загрузки -->
        <button class="btn green-btn" style="padding: 15px;" @click="uploadFile">Загрузить каталог</button>
    </div>
</template>

<script>
import FileUploader from '@/components/UploadFilesController.vue';
import CustomInput from '@/components/inputs/CustomInput.vue';
import { mapGetters } from 'vuex';
import api from '@/authAPI.js';

export default {
    components: {
        FileUploader,
        CustomInput
    },
    computed: {
        ...mapGetters('user', ['currentUser', 'isAuthenticated'])
    },
    data() {
        return {
            file: null,
            selectedCategory: '',
            categoryOptions: [
                { value: 'commodity', label: 'Беспилотники' },
                { value: 'service', label: 'Услуги' },
                { value: 'droneHub', label: 'Дронопорты' },
            ],
        };
    },
    methods: {
        handleFileSelected(file) {
            this.file = file;
        },
        async uploadFile() {
            if (!this.selectedCategory || !this.file) {
                window.notificationManager.addNotification('error', 'Пожалуйста, заполните все поля.');
                return;
            }

            if (this.file.type !== "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet") {
                window.notificationManager.addNotification('error', 'Можно загрузить только EXCEL файлы');
                return;
            }

            const formData = new FormData();
            formData.append('typeAction', "addFile");
            formData.append('typeProduct', this.selectedCategory);
            formData.append('login', this.currentUser.username);
            formData.append('fileData', this.file);

            console.log("addFile", this.selectedCategory, this.currentUser.username, this.file);

            try {
                const response = await api.post('/upload_photo/', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                });
                window.notificationManager.addNotification('success', 'Файл успешно загружен');
            } catch (error) {
                const errorMessage = error.response?.data?.message || 'Ошибка при загрузке файла';
                window.notificationManager.addNotification('error', errorMessage);
                console.error('Ошибка загрузки:', error);
            }
        }
    }
};
</script>

<style scoped>
.upload-form {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 25px;
}
</style>
