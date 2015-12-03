package se.uu.csproject.monadclient.storage;

import java.util.ArrayList;
import java.util.Date;

public class UserLocation {
    private String locationId;
    private String time;
    private double latitude = 0.0;
    private double longitude = 0.0;

    public UserLocation(String locationId, String time) {
        ArrayList<BusStop> busStops = Storage.getBusStops();
        for (int i = 0; i < busStops.size(); i++){
            if (locationId.equals(busStops.get(i).getName())){
                latitude = busStops.get(i).getLatitude();
                longitude = busStops.get(i).getLongitude();
                break;
            }
        }
        this.locationId = locationId;
        this.time = time;
    }

    public double getLatitude() {
        return latitude;
    }

    public double getLongitude() {
        return longitude;
    }

    public String getLocationId() {
        return locationId;
    }

    public String getTime() {
        return time;
    }
}
