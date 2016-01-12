package se.uu.csproject.monadvehicle.storage;

import android.util.Log;
import org.mapsforge.core.model.LatLong;
import java.util.ArrayList;
import java.util.Date;

import se.uu.csproject.monadvehicle.storage.BusStop;

public class BusTrip {
    private String busTripID;
    private int capacity;
    private ArrayList<BusStop> busStops;
    private ArrayList<LatLong> trajectory;
    private int boardingPassengers;
    private int departingPassengers;

    public BusTrip(String busTripID, int capacity, ArrayList<BusStop> busStops) {
        this.busTripID = busTripID;
        this.capacity = capacity;
        this.busStops = busStops;
        this.boardingPassengers = 0;
        this.departingPassengers = 0;
    }

    public void printValues() {
        Log.d("BusTrip", "-- Printing Values --");
        Log.d("BusTrip", "ID: " + busTripID);
        Log.d("BusTrip", "Capacity: " + capacity);
        Log.d("BusTrip", "Boarding: " + boardingPassengers);
        Log.d("BusTrip", "Departing: " + departingPassengers);
        printBusStops();
        printTrajectory();
    }

    public void printBusStops() {

        if (busStops != null) {
            Log.d("BusTrip", "-- Printing BusStops --");

            for (int i = 0; i < busStops.size(); i++) {
                busStops.get(i).printValues();
            }
        }
    }

    public void printTrajectory() {

        if (trajectory != null) {
            Log.d("BusTrip", "-- Printing Trajectory --");

            for (int i = 0; i < trajectory.size(); i++) {
                Log.d("TrajectoryPoint", trajectory.get(i).toString());
            }
        }
    }

    public String getBusTripID() {
        return busTripID;
    }

    public void setBusTripID(String busTripID) {
        this.busTripID = busTripID;
    }

    public int getCapacity() {
        return capacity;
    }

    public void setCapacity(int capacity) {
        this.capacity = capacity;
    }

    public ArrayList<BusStop> getBusStops() {
        return busStops;
    }

    public void setBusStops(ArrayList<BusStop> busStops) {
        this.busStops= busStops;
    }

    public ArrayList<LatLong> getTrajectory() {
        return trajectory;
    }

    public void setTrajectory(ArrayList<LatLong> trajectory) {
        this.trajectory = trajectory;
    }

    public Date getStartingTime() {

        if (busStops != null) {
            return busStops.get(0).getArrivalTime();
        }
        return null;
    }

    public Date getEndingTime() {

        if (busStops != null) {
            return busStops.get(busStops.size() - 1).getArrivalTime();
        }
        return null;
    }

    public int getBoardingPassengers() {
        return boardingPassengers;
    }

    public void setBoardingPassengers(int boardingPassengers) {
        this.boardingPassengers = boardingPassengers;
    }

    public int getDepartingPassengers() {
        return departingPassengers;
    }

    public void setDepartingPassengers(int departingPassengers) {
        this.departingPassengers = departingPassengers;
    }
}
