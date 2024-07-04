let instance = null;

class EventsList {
    constructor() {
        if (!instance) {
            instance = this;
            this.events = [];
        }
        return instance;
    }

    addEvent(event) {
        this.events.push(event);
    }

    getEvents() {
        return this.events;
    }

    static getInstance() {
        if (!instance) {
            instance = new EventsList();
        }
        return instance;
    }      
}

export default EventsList;
