package se.uu.csproject.monadclient.recyclerviews;

import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.GregorianCalendar;

/**
 *
 */
public class PartialTrip {
    //    private String id;
    private int line;
    private String startBusStop; // this is the bus stop name
    private Date startTime;
    private String endBusStop; // this is the bus stop name
    private Date endTime;
    private ArrayList<String> trajectory;

    public PartialTrip(int line, String startBusStop, Date startTime, String endBusStop,
                       Date endTime, ArrayList<String> trajectory) {
        this.line = line;
        this.startBusStop = startBusStop;
        this.startTime = startTime;
        this.endBusStop = endBusStop;
        this.endTime = endTime;
        this.trajectory = trajectory;
    }

    public int getLine() {
        return line;
    }

    public void setLine(int line) {
        this.line = line;
    }

    public Date getStartTime() {
        return startTime;
    }

    public void setStartTime(Date startTime) {
        this.startTime = startTime;
    }

    public String getEndBusStop() {
        return endBusStop;
    }

    public void setEndBusStop(String endBusStop) {
        this.endBusStop = endBusStop;
    }

    public Date getEndTime() {
        return endTime;
    }

    public void setEndTime(Date endTime) {
        this.endTime = endTime;
    }

    public ArrayList<String> getTrajectory() {
        return trajectory;
    }

    public void setTrajectory(ArrayList<String> trajectory) {
        this.trajectory = trajectory;
    }

    public String getStartBusStop() {
        return startBusStop;
    }

    public void setStartBusStop(String startBusStop) {
        this.startBusStop = startBusStop;
    }

}
