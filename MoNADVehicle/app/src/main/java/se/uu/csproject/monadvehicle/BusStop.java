package se.uu.csproject.monadvehicle;

import android.util.Log;

import java.util.Date;

public class BusStop {
    private String busStopID;
    private String name;
    private double latitude;
    private double longitude;
    private Date arrivalTime;
    private int boardingPassengers;
    private int leavingPassengers;

    public BusStop(String busStopID, String name, double latitude, double longitude, Date arrivalTime,
                   int boardingPassengers, int leavingPassengers) {
        this.busStopID = busStopID;
        this.name = name;
        this.latitude = latitude;
        this.longitude = longitude;
        this.arrivalTime = arrivalTime;
        this.boardingPassengers = boardingPassengers;
        this.leavingPassengers = leavingPassengers;
    }

    public BusStop(String busStopID, String name, double latitude, double longitude, Date arrivalTime) {
        this.busStopID = busStopID;
        this.name = name;
        this.latitude = latitude;
        this.longitude = longitude;
        this.arrivalTime = arrivalTime;
        this.boardingPassengers = 0;
        this.leavingPassengers = 0;
    }

    public void printValues() {
        Log.d("BusStop", "-- Printing Values --");
        Log.d("BusStop", "ID: " + getBusStopID());
        Log.d("BusStop", "Name: " + getName());
        Log.d("BusStop", "Latitude: " + getLatitude());
        Log.d("BusStop", "Longitude: " + getLongitude());
        Log.d("BusStop", "ArrivalTime: " + getArrivalTime());
        Log.d("BusStop", "BoardingPassengers: " + getBoardingPassengers());
        Log.d("BusStop", "LeavingPassengers: " + getLeavingPassengers());
    }

    public String getBusStopID() {
        return busStopID;
    }

    public void setBusStopID(String busStopID) {
        this.busStopID = busStopID;
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

    public Date getArrivalTime() {
        return arrivalTime;
    }

    public void setArrivalTime(Date arrivalTime) {
        this.arrivalTime = arrivalTime;
    }

    public int getBoardingPassengers() {
        return boardingPassengers;
    }

    public void setBoardingPassengers(int boardingPassengers) {
        this.boardingPassengers = boardingPassengers;
    }

    public int getLeavingPassengers() {
        return leavingPassengers;
    }

    public void setLeavingPassengers(int leavingPassengers) {
        this.leavingPassengers = leavingPassengers;
    }

    public String coordinatesToString() {
        return "(" + longitude + ", " + latitude + ")";
    }
}