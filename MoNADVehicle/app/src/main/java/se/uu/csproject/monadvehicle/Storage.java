package se.uu.csproject.monadvehicle;

/**
 *
 */
public class Storage {
    private static BusTrip busTrip;

    public static BusTrip getBusTrip() {
        return busTrip;
    }

    public static void setBusTrip(BusTrip busTrip) {
        Storage.busTrip = busTrip;
    }

    public static boolean isEmptyBusTrip() {
        if (busTrip == null) {
            return true;
        }
        else {
            return false;
        }
    }
}
