<template>
    <div class="error-container">
        <div class="error-message">
            <h2>{{ title }}</h2>
            <p>{{ message }}</p>
            <template v-if="type === 'notfound'">
                <router-link class="btn white-btn" to="/">На главную</router-link>
            </template>
            <template v-else-if="type === 'unauthorized'">
                <button class="btn white-btn" @click="login">Авторизоваться</button>
            </template>
            <template v-else>
                <router-link class="btn white-btn" to="/">На главную</router-link>
            </template>
        </div>
    </div>

</template>

<script>
export default {
    name: 'ErrorMessage',
    props: {
        title: {
            type: String,
            default: 'Ошибка'
        },
        message: {
            type: String,
            default: 'Что-то пошло не так. Пожалуйста, попробуйте еще раз или вернитесь на главную страницу.'
        },
        type: {
            type: String,
            default: 'default'
        }
    },
    methods: {
        login() {
            window.loginModal.open()
        }
    }
};
</script>

<style scoped>

.error-container {
    display: flex;
    width: 100%;
    justify-content: center;
    align-items: center;
}

.error-message {
    max-width: 600px;
    height: fit-content;
    max-height: 600px;
    padding: 20px;
    background-color: #ffcccc;
    border: 1px solid #ff0000;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.error-message h2 {
    color: #ff0000;
}

.error-message p {
    margin-top: 10px;
}

.error-message button {
    margin-top: 15px
}

.error-message a {
    margin-top: 15px;
    color: #ff0000;
    text-decoration: none;
    cursor: pointer;
    border: none;
}
</style>
