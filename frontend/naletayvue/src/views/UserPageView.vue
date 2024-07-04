<template>
    <div class="userPage_container" v-if="isAuthenticated">
        <SidebarMenu /> 
        <div class="content">
            <router-view class="centered"></router-view>
        </div>
    </div>
    <ErrorMessage type="unauthorized" title="Ошибка авторизации" message="Для доступа к этой странице необходимо авторизоваться. Пожалуйста, войдите в свой аккаунт или зарегистрируйтесь, если у вас еще нет учетной записи." v-else/>
</template>

<script>
import { mapGetters } from 'vuex';
import SidebarMenu from '@/components/SidebarMenu.vue';
import ErrorMessage from '@/components/ErrorMessage.vue';

export default {
    components: {
        SidebarMenu,
        ErrorMessage
    },
    computed: {
        ...mapGetters('user', ['currentUser', 'isAuthenticated'])
    },
    mounted() {
        if (!this.isAuthenticated) {
            window.loginModal.open()
        }
    }
};
</script>

<style scoped>
.userPage_container {
    display: flex;
    align-items: flex-start;
    text-align: left;
    flex-flow: row;
    height: 100%;
    width: 100%;
    max-width: 1280px;
    margin-top: 25px;
    margin-bottom: 25px;
    gap: 15px;
    box-sizing: border-box;
}

.content {
    display: flex;
    width: 100%;
    flex-flow: row wrap;
    border-radius: 15px;
    gap: 15px;
    margin-bottom: 25px;
}

.centered {
    display: flex;
    width: 100%;
}

@media (max-width: 1024px) { 
    .userPage_container {
        justify-content: center;
        flex-flow: row wrap;
    }

}
</style>
