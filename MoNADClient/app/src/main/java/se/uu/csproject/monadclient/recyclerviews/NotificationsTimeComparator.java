package se.uu.csproject.monadclient.recyclerviews;

import java.util.Comparator;

public class NotificationsTimeComparator implements Comparator<Notify> {

    @Override
    public int compare(Notify notification1, Notify notification2) {
        return notification1.getTime().compareTo(notification2.getTime());
    }
}
