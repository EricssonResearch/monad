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

    //TODO: Remove this constructor once we integrate the parsing/reading of waypoints
    public BusTrip(String busTripID, int capacity, ArrayList<BusStop> busStops) {
        this.busTripID = busTripID;
        this.capacity = capacity;
        this.busStops = busStops;
        this.trajectory = new ArrayList<>();
        generateFakeTrajectory();
    }

    public BusTrip(String busTripID, int capacity, ArrayList<BusStop> busStops, ArrayList<LatLong> trajectory) {
        this.busTripID = busTripID;
        this.capacity = capacity;
        this.busStops = busStops;
        this.trajectory = trajectory;
    }

    public void printValues() {
        Log.d("BusTrip", "ID: " + getBusTripID());
        Log.d("BusTrip", "Capacity: " + getCapacity());

        if (getBusStops() != null) {
            for (int i = 0; i < busStops.size(); i++) {
                busStops.get(i).printValues();
            }
        }
        if (getTrajectory() != null) {
            for (int i = 0; i < trajectory.size(); i++) {
                Log.d("Trajectory", trajectory.get(i).toString());
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

    //TODO: Remove this function when reading/parsing real waypoints is implemented
    private void generateFakeTrajectory(){
        this.trajectory.add(new LatLong(59.851294, 17.593113));
        this.trajectory.add(new LatLong(59.850208, 17.600629));
        this.trajectory.add(new LatLong(59.851952, 17.603680));
        this.trajectory.add(new LatLong(59.850008, 17.610965));
        this.trajectory.add(new LatLong(59.852265, 17.613409));
        this.trajectory.add(new LatLong(59.853481, 17.616570));
        this.trajectory.add(new LatLong(59.850975, 17.618847));
        this.trajectory.add(new LatLong(59.849815, 17.620939));
        this.trajectory.add(new LatLong(59.846652, 17.624497));
        this.trajectory.add(new LatLong(59.846425, 17.624276));
        this.trajectory.add(new LatLong(59.844812, 17.625015));
        this.trajectory.add(new LatLong(59.840875, 17.630646));
        this.trajectory.add(new LatLong(59.841609, 17.639105));
        this.trajectory.add(new LatLong(59.839344, 17.640161));
        this.trajectory.add(new LatLong(59.840673, 17.647350));
        this.trajectory.add(new LatLong(59.840063, 17.647760));
    }
}
