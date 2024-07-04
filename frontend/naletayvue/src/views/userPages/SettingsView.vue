<template>
    <router-view />
</template>

<script>
import SettingsForm from '@/components/inputs/CustomForm.vue';

export default {
    components: {
        SettingsForm,
    },
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
