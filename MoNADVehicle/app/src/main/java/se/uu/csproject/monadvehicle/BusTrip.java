package se.uu.csproject.monadvehicle;

import android.util.Log;
import java.util.ArrayList;
import java.util.Date;


/**
 *
 */
public class BusTrip {
    String busTripID;
    int capacity;
    private ArrayList<BusStop> trajectory;


    public BusTrip(String busTripID, int capacity, ArrayList<BusStop> trajectory) {
        this.busTripID = busTripID;
        this.capacity = capacity;
        this.trajectory = trajectory;
    }

    public void printValues() {
        Log.d("BusTrip", "ID: " + getBusTripID());
        Log.d("BusTrip", "Capacity: " + getCapacity());

        if (getTrajectory() != null) {
            for (int i = 0; i < trajectory.size(); i++) {
                trajectory.get(i).printValues();
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

    public ArrayList<BusStop> getTrajectory() {
        return trajectory;
    }

    public void setTrajectory(ArrayList<BusStop> trajectory) {
        this.trajectory = trajectory;
    }

    public Date getStartingTime() {

        if (trajectory != null) {
            return trajectory.get(0).getArrivalTime();
        }
        return null;
    }

    public Date getEndingTime() {

        if (trajectory != null) {
            return trajectory.get(trajectory.size() - 1).getArrivalTime();
        }
        return null;
    }


}
