class ChatMessage {
    constructor(id, userLogin, companyName, text, file, date) {
        this.id = id;
        this.userLogin = userLogin;
        this.companyName = companyName;
        this.text = text;
        this.file = file;
        this.date = date;
    }
}

export default ChatMessage;
