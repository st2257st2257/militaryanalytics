class NotificationManager {
    constructor(maxVisibleNotifications = 1) {
        this.maxVisibleNotifications = maxVisibleNotifications;
        this.visibleNotifications = [];
        this.notificationsQueue = [];
        this.notificationsChangeCallback = null;
        this.notificationTextSet = new Set();
        this.notificationTimeouts = {};
    }

    setMaxVisibleNotifications(maxVisibleNotifications) {
        this.maxVisibleNotifications = maxVisibleNotifications;
        this.processQueue();
    }

    addNotification(type, message, duration = 3000, autoClose = true, onClose = null) {
        if (this.notificationTextSet.has(message)) {
            return;
        }

        const notification = {
            id: `notification_${Date.now()}`,
            type,
            message,
            duration,
            autoClose,
            onClose
        };

        this.notificationTextSet.add(message);

        if (this.visibleNotifications.length < this.maxVisibleNotifications) {
            this.showNotification(notification);
        } else {
            this.addToQueue(notification);
        }
    }

    showNotification(notification) {
        if (this.visibleNotifications.length >= this.maxVisibleNotifications) {
            const removedNotification = this.visibleNotifications.shift();
            this.notificationTextSet.delete(removedNotification.message);
        }
        this.visibleNotifications.push(notification);
        if (notification.autoClose) {
            this.startAutoCloseTimeout(notification);
        }
        this.notifyNotificationsChange();
    }

    addToQueue(notification) {
        this.notificationsQueue.push(notification);
        if (this.visibleNotifications.length < this.maxVisibleNotifications) {
            this.processQueue();
        }
    }

    processQueue() {
        if (this.notificationsQueue.length > 0 && this.visibleNotifications.length < this.maxVisibleNotifications) {
            const notificationToAdd = this.notificationsQueue.shift();
            setTimeout(() => {
                this.showNotification(notificationToAdd);
                this.processQueue();
            }, 100);
        }
    }

    handleClose(id) {
        const index = this.visibleNotifications.findIndex(notification => notification.id === id);
        if (index !== -1) {
            const removedNotification = this.visibleNotifications.splice(index, 1)[0];
            clearTimeout(this.notificationTimeouts[id]);
            this.notificationTextSet.delete(removedNotification.message);
            if (removedNotification.onClose) {
                removedNotification.onClose();
            }
            this.processQueue();
        }
        this.notifyNotificationsChange();
    }

    startAutoCloseTimeout(notification) {
        const { id, duration } = notification;
        this.notificationTimeouts[id] = setTimeout(() => {
            this.handleClose(id);
        }, duration);
    }

    onNotificationsChange(callback) {
        this.notificationsChangeCallback = callback;
    }

    notifyNotificationsChange() {
        if (this.notificationsChangeCallback) {
            this.notificationsChangeCallback(this.visibleNotifications);
        }
    }
}

export default NotificationManager;
