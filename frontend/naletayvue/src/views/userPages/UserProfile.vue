<template>
    <div v-if="user" class="user-profile">
        <h2>Профиль {{ user.companyName }}</h2>
        <div class="profile-container">
            <div class="profile-header">
                <LogoUploader
                    :logoUrl="logoUrl"
                    :isEditMode="isEditMode"
                    @logo-upload="onLogoUpload"
                />
                <div class="profile-details">
                    <div class="legal-info">
                    <h3>Юридическая информация</h3>
                        <div v-for="(field, index) in legalFields" :key="index" class="profile-field">
                            <p>
                                <strong>{{ field.label }}:</strong>
                                <span style="margin-left: 5px;">{{ user[field.name] }}</span>
                            </p>
                        </div>
                    </div>
                </div>
            </div>
            <div class="company-info">
                <h3>Информация о компании</h3>
                <div v-for="(field, index) in profileFields" :key="index" class="profile-field">
                    <p>
                    <strong>{{ field.label }}:</strong>
                    <span style="margin-left: 5px;" v-if="!isEditMode || !field.editable">{{ user[field.name] }}</span>
                    <CustomInput
                        v-else
                        v-model="user[field.name]"
                        :placeholder="field.placeholder"
                        :inputType="field.inputType"
                    />
                    </p>
                </div>
                <h3>Описание</h3>
                <p v-if="!isEditMode">{{ user.fullDescription }}</p>
                <CustomInput
                    v-else
                    v-model="user.fullDescription"
                    placeholder="Введите описание компании"
                    inputType="textarea"
                />
            </div>

            <div v-if="isOwner" class="edit-buttons">
                <button class="btn green-btn" @click="toggleEditMode">
                    {{ isEditMode ? 'Сохранить' : 'Изменить' }}
                </button>
                <button class="btn error-btn" v-if="isEditMode" @click="cancelEditMode">
                    Отмена
                </button>
                <router-link class="link grey" v-if="isEditMode" :to="{ name: 'LegalInfo' }">
                    Изменить юридическую информацию
                </router-link>
            </div>
        </div>
    </div>

    <div style="display: flex; justify-content: center; align-items: center; width: 100%; min-height: 400px; height: 100%;" v-else-if="user != false">
        <LoadingController :fetchData="loadUserData" />
    </div>

    <div v-else-if="user === false">
        <ErrorMessage
            type="notfound"
            title="Пользователь не найден"
            message="Профиль пользователя не найден. Пожалуйста, проверьте правильность URL или войдите в систему."
        />
    </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import ErrorMessage from '@/components/ErrorMessage.vue';
import CustomInput from '@/components/inputs/CustomInput.vue';
import LoadingController from '@/components/LoadingController.vue';
import LogoUploader from '@/components/inputs/LogoUploader.vue';
import api from '@/authAPI.js';

export default {
    props: {
        userId: {
            type: String,
            required: true,
        },
    },
    data() {
        return {
            user: null,
            originalUserData: null,
            logoUrl: null,
            isEditMode: false,
            profileFields: [
                { name: 'email', label: 'Почта', editable: false },
                { name: 'companySite', label: 'Сайт компании', placeholder: 'Введите сайт компании', inputType: 'input', editable: true },
            ],
            legalFields: [
                { name: 'companyName', label: 'Компания' },
                { name: 'inn', label: 'ИНН' },
                { name: 'kpp', label: 'КПП' },
                { name: 'ogrn', label: 'ОГРН' },
                { name: 'legalAddress', label: 'Юридический адрес' },
                { name: 'country', label: 'Страна' },
                { name: 'mainCity', label: 'Город' },
            ],
        };
    },
    computed: {
        ...mapGetters('user', ['currentUser', 'isAuthenticated']),
        isOwner() {
            return this.isAuthenticated && this.currentUser.username === this.userId;
        },
    },
    methods: {
        ...mapActions('user', ['fetchUserData', 'updateUser']),
        toggleEditMode() {
            if (this.isEditMode) {
                this.saveProfileChanges();
            }
            window.notificationManager.addNotification('success', `Вы вошли в режим редактирования`, 2000);
            this.isEditMode = true;
        },
        cancelEditMode() {
            window.notificationManager.addNotification('error', `Вы вышли из режима редактирования`, 2000);
            this.user = JSON.parse(JSON.stringify(this.originalUserData));
            this.isEditMode = false;
        },
        async saveProfileChanges() {
            try {
                const result = await this.updateUser({
                    username: this.currentUser.username,
                    updatedData: this.user
                });
                if (result.success) {
                    window.notificationManager.addNotification('success', `Профиль успешно обновлен`, 3000);
                    this.originalUserData = JSON.parse(JSON.stringify(this.user));
                    this.isEditMode = false;
                } else {
                    window.notificationManager.addNotification('error', result.message, 2000);
                }
            } catch (error) {
                console.error('Error saving profile changes:', error);
            }
        },
        onLogoUpload(file) {
            if (file) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    this.logoUrl = e.target.result;
                };
                reader.readAsDataURL(file);
                this.uploadLogo(file);
            }
        },
        async uploadLogo(file) {
            try {
                const formData = new FormData();
                formData.append('action', 'addOneFile');
                formData.append('className', 'User');
                formData.append('userOwner', this.currentUser.username);
                formData.append('objectType', 'img');
                formData.append('fileName', 'company_logo');
                formData.append('filePhoto', file);

                await api.post('/upload_file/', formData);
            } catch (error) {
                console.error('Error uploading logo:', error);
            }
        },
        async loadUserData() {
            try {
                const userData = await this.fetchUserData(this.userId);
                this.user = userData;
                this.originalUserData = JSON.parse(JSON.stringify(this.user));
                await this.fetchLogoUrl();
            } catch (error) {
                this.user = null;
                console.error('Error fetching user data:', error);
                throw error;
            }
        },
        async fetchLogoUrl() {
            const formData = new FormData();
            formData.append('action', 'getFileName');
            formData.append('fileName', 'company_logo');
            formData.append('userOwner', this.userId);
            
            try {
                const response = await api.post('/get_file/', formData);
                this.logoUrl = response.data.file_static_url;
            } catch (error) {
                console.error('Error fetching logo URL:', error);
            }
        }
    },
    async created() {
        await this.loadUserData();
    },
    components: {
        ErrorMessage,
        CustomInput,
        LoadingController,
        LogoUploader
    },
};
</script>

<style scoped>
.user-profile {
    display: flex;
    flex-flow: column;
    width: 100%;
    max-width: 1280px;
    background: var(--color-background-soft);
    padding: 10px !important;
    margin-bottom: 15px;
    border-radius: 10px;
}

.profile-container {
    display: flex;
    flex-flow: column;
    gap: 15px;
}

.profile-container h3 {
    font-weight: 600;
}

.profile-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-top: 15px;
}

.logo-container {
    width: 256px;
    height: 256px;
    margin-left: 20px;
    text-align: right;
    border-radius: 100%;
    order: 2;
    background: var(--color-background);
    display: flex;
    justify-content: center;
    align-items: center;
}

.logo {
    width: 150px;
    height: 150px;
    object-fit: cover;
    border-radius: 50%;
}

.profile-details {
    display: flex;
    flex-flow: column;
    gap: 5px;
    flex: 0.8;
}

.company-info {
    display: flex;
    flex-flow: column;
    gap: 5px;
}

.legal-info {
    display: flex;
    flex-flow: column;
    gap: 5px;
}

.edit-buttons {
    display: flex;
    align-items: center;
    gap: 20px;
    margin-top: 20px;
}

@media (max-width: 768px) {
    .user-profile {
        padding: 10px;
    }

    .profile-header {
        flex-direction: column;
        align-items: center;
    }

    .logo-container {
        width: 150px;
        height: 150px;
        margin: 0 auto 20px;
    }

    .logo {
        width: 100px;
        height: 100px;
    }

    .profile-details {
        width: 100%;
        text-align: center;
    }

    .profile-details p {
        margin: 5px 0;
    }

    .edit-buttons {
        width: 100%;
        display: flex;
        justify-content: center;
    }
}
</style>
