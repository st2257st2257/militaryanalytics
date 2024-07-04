<template>
    <div class="setting-group" :class="{ 'show-setting': isLoaded }" v-for="group in settingsGroups" :key="group.groupName">
        <h2>{{ group.groupName }}</h2>
        <div class="setting-container" v-for="setting in group.settings" :key="setting.variableName">
            <CustomInput :variableValue="setting.variableValue"  :variableName="setting.variableName" :inputType="'input'" :options="setting.options" />
            <label class="setting-desc">{{ setting.description }}</label>
        </div>
        <button class="btn-default" @click="saveGroupSettings(group)">Save Settings</button>
    </div>
</template>

<script>
import CustomInput from '@/components/inputs/CustomInput.vue';
import Setting from '@/classes/settings/Setting.js';
import SettingsGroup from '@/classes/settings/SettingsGroup.js';
//import SettingsData from '@/classes/settings/settingsData.json'

export default {
    components: {
        CustomInput
    },
    data() {
        return {
            settingsGroups: [],
            isLoaded: false
        };
    },
    methods: {
        saveGroupSettings(group) {
            console.log('Settings saved:', group.settings);
        },
        loadSettings() {
            try {
                const configData = JSON.parse(SettingsData);
                Object.keys(configData).forEach(groupName => {
                    const groupData = configData[groupName];
                    const group = new SettingsGroup(groupName);
                    // Если groupData не является объектом, просто создаем настройку
                    if (typeof groupData === 'object' && groupData !== null) {
                        Object.keys(groupData).forEach(settingName => {
                            const settingData = groupData[settingName];
                            console.log(settingName, settingData)
                            
                            if (typeof settingData !== 'object') {
                                var variableValue = settingData !== undefined ? settingData : null;
                                var description = settingData.description !== undefined ? settingData.description : null;
                                var inputType = settingData.inputType !== undefined ? settingData.inputType : null;
                                var options = settingData.options !== undefined ? settingData.options : [];                                        
                            }

                            const setting = new Setting(
                                settingName,
                                variableValue,
                                description,
                                inputType,
                                options
                            );
                            
                            group.addSetting(setting);
                        });
                    } else {
                        // Если groupData не является объектом, просто создаем настройку
                        const variableValue = groupData !== undefined ? groupData : null;
                        const setting = new Setting(
                            groupName,
                            variableValue,
                            null,
                            null,
                            []
                        );
                        group.addSetting(setting);
                    }
                    this.settingsGroups.push(group);
                });
            } catch (error) {
                console.error('Ошибка при разборе данных из JSON:', error);
            }
        }
    },
    mounted() {
        //this.loadSettings();
        this.isLoaded = true;
    }
};
</script>


<style scoped>
.setting-group {
    margin-bottom: 20px;
    opacity: 0;
    transition: all 0.5s ease;
}

.setting-container {
    position: relative;
    display: grid;
    grid-template-columns: 40% 60%;
    width: 100%;
    height: 115px;
    margin-bottom: 10px;
    align-items: center;
    padding-left: 25px;
    background: #E0EDF1;
    border-radius: 10px;
    opacity: 1;
    transition: all 0.5s ease;
}

.setting-group.show-setting {
    opacity: 1;
    margin-top: 20px;
    transition: all 0.5s ease;
}

.setting-input {
    width: 65%;
    height: 100%;
}

.setting-desc {
    display: flex;
    width: 100%;
    height: 80%;
    padding-left: 25px;
    font-size: 16px;
    font-weight: 600;
    color: #000;
}

</style>