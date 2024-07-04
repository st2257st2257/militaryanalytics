<template>
    <div class="chat-page">
        <ChatList :selectedChat="selectedChat" @selectChat="selectChat" v-if="isDesktop || (!isDesktop && !selectedChat)" />
        <ChatWindow :selectedChat="selectedChat" @backToList="backToList" v-if="selectedChat && (!isDesktop || isDesktop)" />
    </div>
</template>

<script>
import ChatList from '@/components/chat/ChatList.vue';
import ChatWindow from '@/components/chat/ChatWindow.vue';
import { mapGetters } from 'vuex';
import { inject } from 'vue';

export default {
    components: {
        ChatList,
        ChatWindow,
    },
    data() {
        return {
            chatsManager: inject('chatsManager'),
            selectedChat: null,
            isDesktop: window.innerWidth > 1024,
        };
    },
    computed: {
        ...mapGetters('user', ['currentUser', 'isAuthenticated']),
    },
    methods: {
        async selectChat(chat) {
            this.selectedChat = chat;
            await this.selectedChat.loadMessages();
        },
        backToList() {
            this.selectedChat = null;
        },
        handleResize() {
            this.isDesktop = window.innerWidth > 1024;
        },
        async loadChatFromRoute() {
            const chatId = this.$route.query.chatId;
            if (chatId) {
                const chat = await this.chatsManager.getChatByUsers(this.currentUser.username, chatId);
                if (chat) {
                    this.selectChat(chat);
                }
            }
        }
    },
    async mounted() {
        window.addEventListener('resize', this.handleResize);
        await this.loadChatFromRoute();
    },
    beforeUnmount() {
        window.removeEventListener('resize', this.handleResize);
    },
    watch: {
        '$route.query.chatId': 'loadChatFromRoute'
    }
};
</script>

<style scoped>
.chat-page {
    display: flex;
    align-items: flex-start;
    text-align: center;
    flex-flow: row;
    width: 100%;
    height: 90vh;
    max-width: 1280px;
    max-height: 780px;
    margin-bottom: 25px;
    box-sizing: border-box;
    border: 1px solid #ccc;
    background: var(--color-background);
}

@media (max-width: 1024px) {
    .chat-page {
        flex-direction: column;
    }
}
</style>
