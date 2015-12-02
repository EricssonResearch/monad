package se.uu.csproject.monadclient.storage;

import android.util.Log;

public class BusStop {
    private String id;
    private String name;
    private double latitude;
    private double longitude;

    public BusStop(String id, String name, double latitude, double longitude) {
        this.id = id;
        this.name = name;
        this.latitude = latitude;
        this.longitude = longitude;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public double getLatitude() {
        return latitude;
    }

    public void setLatitude(double latitude) {
        this.latitude = latitude;
    }

    public double getLongitude() {
        return longitude;
    }

    public void setLongitude(double longitude) {
        this.longitude = longitude;
    }

    public void printValues() {
        Log.d("BusStop", "-- Printing Values --");
        Log.d("BusStop", "ID: " + id);
        Log.d("BusStop", "Name: " + name);
        Log.d("BusStop", "Latitude: " + latitude);
        Log.d("BusStop", "Longitude: " + longitude);
    }
}
