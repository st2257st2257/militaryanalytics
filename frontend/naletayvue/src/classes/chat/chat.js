import ChatMessage from './chatMessage';
import api from '@/authAPI.js';

class Chat {
  constructor(id, firstUserLogin, secondUserLogin, firstUserName, secondUserName, secondCompanyName, firstCompanyName, visibility) {
    this.id = id;
    this.firstCompanyName = firstCompanyName;
    this.secondCompanyName = secondCompanyName;
    this.firstUserLogin = firstUserLogin;
    this.secondUserLogin = secondUserLogin;
    this.firstUserName = firstUserName;
    this.secondUserName = secondUserName;
    this.visibility = visibility;
    this.messages = [];
  }
  
  async addMessage(userLogin, text, file) {

    if (!text.trim() && !file) {
        console.error('Нельзя отправить пустое сообщение.');
        return;
    }

    const formData = new FormData();
    formData.append('actionType', 'sendMessage');
    formData.append('firstUserLogin', userLogin);
    formData.append('chatId', this.id);
    formData.append('text', text);

    if (file) {
      formData.append('fileData', file);
    }

    await api.post('/user/chat/', formData)
      .then(response => {
          if (response.data) {
              const id = this.messages.length + 1;
              const message = new ChatMessage(id, userLogin, text, file);
              this.messages.push(message);
              this.messages.length = id;
          } else {
              console.error(response.data);
          }
      })
      .catch(error => {
          console.error(error);
      });
  }

  async addSystemMessage(text, files = []) {
    const formData = new FormData();
    formData.append('actionType', 'sendMessage');
    formData.append('firstUserLogin', this.firstUserLogin);
    formData.append('chatId', this.id);
    formData.append('text', text);

    if (files.length > 0) {
      files.forEach(file => formData.append('fileData', file));
    }

    await api.post('/user/chat/', formData)
      .then(response => {
          if (response.data) {
              const id = this.messages.length + 1;
              const message = new ChatMessage(this.id, this.firstUserLogin, text, files);
              this.messages.push(message);
              this.messages.length = id;
          } else {
              console.error(response.data);
          }
      })
      .catch(error => {
          console.error(error);
      });
  }

  async loadMessages() {
    const formData = new FormData();
    formData.append('actionType', 'getChatMessages');
    formData.append('chatId', this.id);

    await api.post('/user/chat/', formData)
      .then(response => {
        if (response.data) {
          const messagesData = response.data;
          this.messages = Object.values(messagesData).map(messageData => (
            new ChatMessage(this.messages.length++, messageData.ownerLogin, messageData.ownerCompanyName ,messageData.text, messageData.url, messageData.date)
          ));
          return true
        } else {
          console.error(response.data.error);
          return false
        }
      })
      .catch(error => {
        console.error(error);
        return false
      });
  }
  
  getLastMessage() {
    if (this.messages.length > 0) {
        const lastMessage = this.messages[this.messages.length - 1];
        try {
            const parsedMessage = JSON.parse(lastMessage.text);
            if (parsedMessage && parsedMessage.messageType === 'order') {
                return `Заказ №${parsedMessage.orderNumber}`;
            } else {
              return lastMessage.text
            }
        } catch (error) {
            return lastMessage.text;
        }
    }
  }

  getChatPartner(username) {
    if (this.firstUserLogin === username) {
      return this.secondCompanyName || this.secondUserLogin;
    } else {
      return this.firstCompanyName || this.firstUserLogin;
    }
  }

  getLastMessageDate() {
    if (this.messages.length > 0) {
      const date = new Date(this.messages[this.messages.length - 1].date);
      const day = date.getDate();
      const month = date.getMonth() + 1;
      return `${day < 10 ? '0' + day : day}.${month < 10 ? '0' + month : month}`;
    }
  }

  getAllMessages() {
    return this.messages;
  }
}

export default Chat;
