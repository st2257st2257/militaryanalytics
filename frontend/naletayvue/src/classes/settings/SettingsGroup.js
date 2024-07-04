class SettingGroup {
    constructor(groupName, settings = []) {
        this.groupName = groupName;
        this.settings = settings;
    }

    addSetting(setting) {
        this.settings.push(setting);
    }
}

export default SettingGroup;