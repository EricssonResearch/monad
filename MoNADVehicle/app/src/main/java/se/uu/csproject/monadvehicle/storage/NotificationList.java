package se.uu.csproject.monadvehicle.storage;

import java.util.ArrayList;

import se.uu.csproject.monadvehicle.storage.Notification;


public class NotificationList {
    private ArrayList<Notification> notificationsList;

    public NotificationList(ArrayList<Notification> notification){
        this.notificationsList = notification;
    }

    public ArrayList<Notification> getNotificationsList() {
        return notificationsList;
    }

}
