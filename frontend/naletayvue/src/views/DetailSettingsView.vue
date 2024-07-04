<template>
    <div class="settings-menu">
        <h1>Детальные настройки</h1>
        <SettingsList/>
    </div>
</template>

<script>
import SettingsList from '@/components/SettingsList.vue';

export default {
    components: {
        SettingsList
    },
};
</script>

<style scoped>
.settings-menu {
    display: flex;
    flex-flow: column;
    margin-left: 2%;
    margin-right: 2%;
    overflow: hidden;
}
</style>
