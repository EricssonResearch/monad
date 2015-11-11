package se.uu.csproject.monadclient.recyclerviews;

import java.util.Comparator;

public class FullTripsStartTimeComparator implements Comparator<FullTrip> {

    @Override
    public int compare(FullTrip trip1, FullTrip trip2) {
        return trip1.getStartTime().compareTo(trip2.getStartTime());
    }
}
