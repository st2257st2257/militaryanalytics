<template>
    <div class="chat-view">
        <div class="chat-info">
            <button @click="backToList" class="btn green-btn back-button"><</button>
            <span class="info-user">
                <h3>{{ selectedChatPartner }}</h3>
                <p>Онлайн</p>
            </span>
        </div>
        <div class="chat-messages" ref="chatMessages">
            <template v-for="(message, index) in selectedChat.messages" :key="message.id">
                <template v-if="index === 0 || selectedChat.messages[index - 1].userLogin !== message.userLogin">
                    <div class="message">
                        <span class="message_login">{{ message.companyName || message.userLogin }}</span>
                        <MessageRenderer :orderMessage="message.text" />
                        <span v-if="message.file"><FileDownloader :fileUrl="message.file" /></span>
                    </div>
                </template>
                <template v-else>
                    <div class="message">
                        <MessageRenderer :orderMessage="message.text" />
                        <span v-if="message.file"><FileDownloader :fileUrl="message.file" /></span>
                    </div>
                </template>
            </template>
        </div>
        <div class="chat-input">
            <custom-input @send="sendMessage" @update:modelFile="updateInputData" :fileLoader="true" :showSendButton="true" inputType="input" v-model="newMessage" placeholder="Введите сообщение..." />
        </div>
    </div>
</template>

<script>
import { mapGetters } from 'vuex';
import CustomInput from '@/components/inputs/CustomInput.vue';
import FileDownloader from '@/components/FileDownloader.vue';
import MessageRenderer from '@/components/chat/MessageRenderer.vue';

export default {
    props: {
        selectedChat: {
            type: Object,
            required: true,
        },
    },
    components: {
        CustomInput,
        FileDownloader,
        MessageRenderer
    },
    data() {
        return {
            newMessage: '',
            selectedFile: null,
        };
    },
    computed: {
        ...mapGetters('user', ['currentUser', 'isAuthenticated']),
        selectedChatPartner() {
            return this.selectedChat.getChatPartner(this.currentUser.username);
        },
    },
    watch: {
        selectedChat: {
            immediate: true,
            handler(newVal, oldVal) {
                if (newVal !== oldVal) {
                    this.loadMessages();
                }
            },
        },
        'selectedChat.messages': {
            handler() {
                this.scrollToBottom();
            },
            deep: true,
        },
    },
    methods: {
        updateInputData(file) {
            this.selectedFile = file;
        },
        async sendMessage() {
            if (this.selectedChat) {
                await this.selectedChat.addMessage(this.currentUser.username, this.newMessage, this.selectedFile);
                this.selectedFile = null;
                this.newMessage = '';
                this.loadMessages()
                this.$nextTick(() => {
                    this.scrollToBottom(true);
                });
            }
        },
        handleFileChange(event) {
            this.selectedFile = event.target.files[0];
        },
        async loadMessages() {
            if (this.selectedChat !== null) {
                await this.selectedChat.loadMessages();
            }
            this.$nextTick(() => {
                this.scrollToBottom(false);
            });
        },
        scrollToBottom() {
            const container = this.$refs.chatMessages;
            if (container) {
                container.scrollTop = container.scrollHeight;
            }
        },
        backToList() {
            this.$emit('backToList');
        },
    },
    mounted() {
        this.loadMessages();
    },
};
</script>

<style scoped>
.chat-view {
    display: flex;
    flex-flow: column;
    justify-content: space-between;
    width: 75%;
    height: 100%;
    background: var(--color-background);
}

.chat-window {
    flex: 1;
    padding: 20px;
}

.chat-info {
    display: flex;
    justify-content: flex-start;
    align-items: center;
    padding-left: 15px;
    height: 60px;
    background: var(--color-background-soft);
    border-bottom: 1px solid #ccc;
}

.back-button {
    left: 15px;
    width: 40px;
    height: 40px;
    font-size: 14px;
    cursor: pointer;
    background-color: var(--color-btn-green-background);
    color: #fff;
    border: none;
}

.info-user {
    display: flex;
    justify-content: flex-start;
    text-align: left;
    flex-flow: column;
    line-height: 20px;
    margin-left: 15px;
}

.chat-messages {
    height: 100%;
    max-height: 100%;
    overflow-y: auto;
    padding: 0px 15px 20px 15px;
    box-sizing: border-box;
}

.message {
    display: flex;
    text-align: left;
    width: fit-content;
    justify-content: flex-start;
    align-items: flex-start;
    flex-flow: column;
    max-width: 68vw;
    overflow: hidden;
    padding: 5px 10px 0px 5px;
}

.chat-input {
    bottom: 0;
    padding: 15px;
    border-top: 1px solid #ccc;
}

.message_login {
    color: var(--color-black-text);
    font-weight: 600;
}

@media (max-width: 1024px) {
    .chat-view {
        width: 100%;
    }
}
</style>
