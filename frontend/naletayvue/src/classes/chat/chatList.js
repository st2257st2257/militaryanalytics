import api from '@/authAPI';
import Chat from '@/classes/chat/chat.js';

class ChatList {
    constructor() {
        this.chats = [];
    }

    async removeChat(chatId) {
        this.chats = this.chats.filter(chat => chat.id !== chatId);
    }

    getAllChats() {
        return this.chats;
    }

    async getChatById(chatId) {
        return this.chats.find(chat => chat.id === chatId);
    }
    
    async getChatByUsers(firstUser, secondUser) {
        const convertUsername = { 
            username: firstUser
        }
        
        await this.loadChats(convertUsername);

        const foundChat = this.chats.find(chat => {
            const usersMatch = (
                (chat.firstUserLogin === firstUser && chat.secondUserLogin === secondUser) ||
                (chat.firstUserLogin === secondUser && chat.secondUserLogin === firstUser)
            );
            return usersMatch;
        });
        
        return foundChat || null;
    }

    async loadChats(user) {
        if (!user || !user.username) return false;
    
        try {
            const formData = new FormData();
            formData.append('actionType', 'getChats');
            formData.append('firstUserLogin', user.username);
        
            const response = await api.post('user/chat/', formData);
            const chatDataArray = Object.values(response.data);


            const newChats = await Promise.all(chatDataArray.map(async chatData => {
                const chat = new Chat(
                    chatData.chatId,
                    chatData.firstUserLogin,
                    chatData.secondUserLogin,
                    chatData.firstUserName,
                    chatData.secondUserName,
                    chatData.secondCompanyName,
                    chatData.firstCompanyName,
                    chatData.visibility
                );
                await chat.loadMessages();
                return chat;
            }));
            
            this.chats = newChats;
            return true;
        } catch (error) {
            console.error(error);
            throw new Error('Ошибка при загрузке чатов');
        }
    }    

    async addChat(currentUser, secondUser) {
        try {
            const formData = new FormData();
            formData.append('actionType', 'createChat');
            formData.append('firstUserLogin', currentUser);
            formData.append('secondUserLogin', secondUser);
            
            const response = await api.post('/user/chat/', formData);
            console.log(response)
            if (response.data) {
                await this.loadChats(currentUser);
                return true;
            } else {
                throw new Error('Ошибка при создании чата');
            }
        } catch (error) {
            console.error(error);
            window.notificationManager.addNotification('error', `Произошла ошибка при создании чата с пользователем ${secondUser}: ${error.message}`);
            throw new Error('Ошибка при создании чата');
        }
    }
}

export default ChatList;
