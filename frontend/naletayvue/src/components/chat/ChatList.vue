<template>
    <div class="chat-list">
        <h2 v-if="isAuthenticated">Сообщения</h2>
        <ul>
            <li v-for="chat in this.chatsManager.getAllChats()" :key="chat.id" @click="selectChat(chat)" :class="{ 'active': selectedChat && selectedChat.id === chat.id }">
                <span class="chat-data">
                    <p>{{ chat.getChatPartner(this.currentUser.username) }}</p>
                    <p>{{ chat.getLastMessageDate() }}</p>
                </span>
                <p class="chat-lastMessage">{{ getLastMessageShort(chat.getLastMessage()) }}</p>
            </li>
        </ul>
    </div>
</template>

<script>
import { inject } from 'vue';
import { mapGetters } from 'vuex';

export default {
    props: {
        selectedChat: Object,
    },
    data() {
        return {
            chatsManager: inject('chatsManager'),
            chats: [],
        };
    },
    computed: {
        ...mapGetters('user', ['currentUser', 'isAuthenticated'])
    },
    async mounted() {
        try {
            await this.chatsManager.loadChats(this.currentUser);
        } catch (error) {
            console.error('Ошибка загрузки чатов:', error);
        }
    },
    methods: {
        getLastMessageShort(lastMessage) {
            const maxLength = 40;
            if (lastMessage) {
                return lastMessage.length > maxLength ? lastMessage.slice(0, maxLength) + '...' : lastMessage;
            } else {
                return 'Нет сообщений';
            }
        },
        selectChat(chat) {
            this.$emit('selectChat', chat);
            this.$router.push({ name: 'Chats', query: { chatId: chat.secondUserLogin } });
        },
    },
};
</script>

<style scoped>
.chat-list {
    text-align: left;
    width: 25%;
    height: 100%;
    border-right: 1px solid #ccc;
    background: var(--color-background);
    overflow: hidden;
}

.chat-data {
    display: flex;
    width: 100%;
    justify-content: space-between;
    transition: none;
}

.chat-lastMessage {
    width: 100%;
    line-height: 15px;
    height: 17px;
    margin-top: 2px;
    overflow: hidden;
}

.chat-list h2{
    display: flex;
    align-items: center;
    height: 69px;
    padding-left: 15px;
    font-weight: 600;
    border-bottom: 1px solid #ccc;
}

.chat-list ul {
    list-style-type: none;
    height: 90%;
    padding: 0;
    overflow-y: scroll;
}

.chat-list li {
    cursor: pointer;
    height: 60px;
    padding: 10px;
    border-bottom: 1px solid #ccc;
    overflow: hidden;
}

@media (hover: hover) {
    .chat-list li:hover {
        background-color: #f0f0f0;
    }
}

.chat-list li.active {
    background-color: var(--color-btn-green-background);
    color: #fff;
}

@media (max-width: 1024px) {
    .chat-list {
        width: 100%;
        height: 100%;
        border-right: none;
    }
}
</style>
