import EventsList from './EventsList.js';

let eventIdCounter = 0;

//TODO    Допилить создание ивентов, накинуть обработичков.

class Event {
    constructor(name, date, impact, comment) {
        this.id = ++eventIdCounter;
        this.name = name;
        this.date = date;
        this.impact = impact;
        this.comment = comment;
        EventsList.getInstance().addEvent(this);
    }
}

export default Event;
