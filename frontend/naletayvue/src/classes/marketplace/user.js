class User {
    constructor(data) {
        this.username = data.username || '';
        this.role = 'user';
        this.accessToken = null;
        this.profileType = null;
        this.settings = {};

        for (const key in data) {
            if (Object.hasOwnProperty.call(data, key) && !['username', 'role', 'accessToken', 'profileType', 'settings'].includes(key)) {
                this[key] = data[key];
            }
        }
    }

    setAccessToken(token) {
        this.accessToken = token;
    }

    clearAccessToken() {
        this.accessToken = null;
    }

    setProfileType(profileType) {
        this.profileType = profileType;
    }

    setSettings(settings) {
        this.settings = settings;
    }

    isAdmin() {
        return this.role === 'admin';
    }

    isBuyer() {
        return this.profileType === 'buyer';
    }

    isSeller() {
        return this.profileType === 'seller';
    }

    isProfileComplete() {
        const requiredFields = ['firstNM', 'secondNM', 'userRole', 'email', 'country', 'phone', 'companyName'];
        return requiredFields.every(field => this[field] && this[field].trim() !== '');
    }
}

export default User;
