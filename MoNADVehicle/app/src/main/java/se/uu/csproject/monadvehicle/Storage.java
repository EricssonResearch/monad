package se.uu.csproject.monadvehicle;

import android.location.Location;
import android.util.Log;

public class Storage {
    private static BusTrip busTrip;
    private static Location currentLocation;
    private static BusStop nextBusStop;
    private static int nextBusStopIndex = 0;

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
        if(nextBusStopIndex < busTrip.getBusStops().size()) {
            nextBusStop = busTrip.getBusStops().get(nextBusStopIndex);
        }
    }

}
