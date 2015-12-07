package se.uu.csproject.monadvehicle;

import android.util.Log;

import java.util.ArrayList;

/**
 *
 */
public class Storage {
    private static BusTrip busTrip;
    private static ArrayList<TrafficInformation> trafficIncidents = new ArrayList<>();

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

    public static ArrayList<TrafficInformation> getTrafficIncidents() {
        return trafficIncidents;
    }

    public static void setTrafficIncidents(ArrayList<TrafficInformation> trafficIncidents) {
        Storage.trafficIncidents = trafficIncidents;
    }

    public static boolean isEmptyTrafficIncidents() {
        return trafficIncidents.isEmpty();
    }

    public static void printTrafficIncidents() {

        if (!isEmptyTrafficIncidents()) {
            Log.d("Storage", "-- Printing TrafficIncidents --");

            for (int i = 0; i < trafficIncidents.size(); i++) {
                trafficIncidents.get(i).printValues();
            }
        }
        else {
            Log.d("Storage", "-- Printing TrafficIncidents -- EMPTY");
        }
    }
}
