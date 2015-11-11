package se.uu.csproject.monadclient.recyclerviews;

import java.util.Comparator;

public class FullTripsStartTimeComparator implements Comparator<FullTrip> {

    @Override
    public int compare(FullTrip trip1, FullTrip trip2) {
        int boolToInt1 = trip1.isHistory() ? 1 : 0;
        int boolToInt2 = trip2.isHistory() ? 1 : 0;
        int compareResult = boolToInt2 - boolToInt1;

        if (compareResult != 0){
            return compareResult;
        } else {
            return trip1.getStartTime().compareTo(trip2.getStartTime());
        }
    }
}
