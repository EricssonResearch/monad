package se.uu.csproject.monadvehicle;

import android.util.Log;

import org.mapsforge.core.model.LatLong;

import java.util.ArrayList;
import java.util.Date;

public class BusTrip {
    String busTripID;
    int capacity;
    private ArrayList<BusStop> busStops;
    private ArrayList<LatLong> trajectory;

    public BusTrip(String busTripID, int capacity, ArrayList<BusStop> busStops) {
        this.busTripID = busTripID;
        this.capacity = capacity;
        this.busStops = busStops;
    }

    public void printValues() {
        Log.d("BusTrip", "-- Printing Values --");
        Log.d("BusTrip", "ID: " + getBusTripID());
        Log.d("BusTrip", "Capacity: " + getCapacity());
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
}
