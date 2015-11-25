package se.uu.csproject.monadvehicle;

import java.util.Date;

public class BusStop {
    private int busId;
    private String name;
    private int latitude;
    private int longitude;
    private Date arrivalTime;
    //private Date departureTime;
    private int boardingPassengers;
    private int leavingPassengers;

    public BusStop(int busId, String name, int latitude, int longitude, Date arrivalTime, int boardingPassengers, int leavingPassengers) {
        this.busId = busId;
        this.name = name;
        this.latitude = latitude;
        this.longitude = longitude;
        this.arrivalTime = arrivalTime;
        this.boardingPassengers = boardingPassengers;
        this.leavingPassengers = leavingPassengers;
    }

    public int getBusId() {
        return busId;
    }

    public String getName() {
        return name;
    }

    public int getLatitude() {
        return latitude;
    }

    public int getLongitude() {
        return longitude;
    }

    public Date getArrivalTime() {
        return arrivalTime;
    }

//    public Date getDepartureTime() {
//        return departureTime;
//    }

    public int getBoardingPassengers() {
        return boardingPassengers;
    }

    public int getLeavingPassengers() {
        return leavingPassengers;
    }
}