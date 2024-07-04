<template>
    <div class="profile_info">
        <h2>Личный кабинет</h2>
        <span>{{ currentUser.companyName }}</span>
    </div>
</template>

<script>
import SettingsForm from '@/components/inputs/CustomForm.vue';
import { mapGetters } from 'vuex';

export default {
    components: {
        SettingsForm,
    },
    computed: {
        ...mapGetters('user', ['currentUser']),
    },
    data() {
        return {
        };
    },
};
</script>

<style scoped>
.profile_info {
    display: flex;
    flex-flow: column;
    width: 100%;
    height: fit-content;
    padding: 10px;
    border-radius: 15px;
    background: var(--color-background-soft);
}

@media (max-width: 1345px) { 
    .profile_info {
        flex-flow: column;
    }
}
</style>
