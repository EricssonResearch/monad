package se.uu.csproject.monadvehicle;

/**
 *
 */
public class Storage {
    private static BusTrip busTrip;
    private static TrafficInformation trafficInformation;

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

    public static TrafficInformation getTrafficInformation() {
        return trafficInformation;
    }

    public static void setTrafficInformation(TrafficInformation trafficInformation) {
        Storage.trafficInformation = trafficInformation;
    }
}
