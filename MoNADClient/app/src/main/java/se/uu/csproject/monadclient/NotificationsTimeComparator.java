package se.uu.csproject.monadclient;

import java.util.Comparator;

import se.uu.csproject.monadclient.storage.Notify;

public class NotificationsTimeComparator implements Comparator<Notify> {

    @Override
    public int compare(Notify notification1, Notify notification2) {
        return notification1.getTime().compareTo(notification2.getTime());
    }
}
