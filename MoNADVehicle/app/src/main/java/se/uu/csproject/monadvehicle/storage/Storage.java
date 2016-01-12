package se.uu.csproject.monadvehicle.storage;

import android.location.Location;
import android.util.Log;
import java.util.ArrayList;
import java.util.Calendar;

public class Storage {
    private static BusTrip busTrip;
    private static Location currentLocation;
    private static BusStop nextBusStop;
    private static int nextBusStopIndex = 0;
    private static ArrayList<TrafficInformation> trafficIncidents = new ArrayList<>();

    public static BusTrip getBusTrip() {
        return busTrip;
    }

    public static void setBusTrip(BusTrip busTrip) {
        Storage.busTrip = busTrip;
        Storage.nextBusStop = busTrip.getBusStops().get(0);
    }

    public static boolean isEmptyBusTrip() {
        return busTrip == null;
    }

    public static Location getCurrentLocation(){
        return currentLocation;
    }

    public static void setCurrentLocation(Location location){
        currentLocation = location;
    }

    public static BusStop getNextBusStop(){
        return nextBusStop;
    }

    public static void toNextBusStop(){
        nextBusStopIndex++;

        if (nextBusStopIndex < busTrip.getBusStops().size()) {
            nextBusStop = busTrip.getBusStops().get(nextBusStopIndex);
        }
    }

    public static long getDurationToNextBusStop(){

        if (nextBusStopIndex > 0) {
            return nextBusStop.getArrivalTime().getTime()
                    - busTrip.getBusStops().get(nextBusStopIndex-1).getArrivalTime().getTime();
        }
        else {
            return nextBusStop.getArrivalTime().getTime()
                    - Calendar.getInstance().getTimeInMillis();
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
