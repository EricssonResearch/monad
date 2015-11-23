package se.uu.csproject.monadvehicle;

import java.util.ArrayList;
import java.util.List;

public class Route {
    private List<BusStop> busStopList;
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


    public List<BusStop> getBusStopList() {
        return busStopList;
    }
}
