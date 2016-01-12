package se.uu.csproject.monadvehicle.storage;

import java.util.ArrayList;

public class Route {
    private ArrayList<BusStop> busStopList;
    private boolean completed;

    public Route(ArrayList<BusStop> busStops){
        this.busStopList = busStops;
        this.completed = false;
    }

    public boolean isCompleted(){
        return completed;
    }

    public void complete(){
        this.completed = true;
    }


    public ArrayList<BusStop> getBusStopList() {
        return busStopList;
    }
}
