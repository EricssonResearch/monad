package se.uu.csproject.monadclient.recyclerviews;

/* This class is derived from the TravelRequest collection
 * The focus is on the assigned route rather than the request itself
 * Therefore, the class attributes are not comprehensive
 */

import java.util.Calendar;
import java.util.Date;

//TODO: change times data types
public class Trip {
    private int tripId;
    private String startBusStop; // this is the bus stop name
    private Date startTime;
    private String endBusStop; // this is the bus stop name
    private Date endTime;
    private int durationMinutes;
    private int userFeedback;

    public Trip(int tripId, String startBusStop, Date startTime,
                 String endBusStop, Date endTime, int duration, int userFeedback) {
        this.tripId = tripId;
        this.setStartBusStop(startBusStop);
        this.setStartTime(startTime);
        this.setEndBusStop(endBusStop);
        this.setEndTime(endTime);
        this.setDurationMinutes(duration);
        this.setUserFeedback(userFeedback);
    }

    // returns time in Milliseconds
    public long getTimeToDeparture(){
        return this.getStartTime().getTime() - Calendar.getInstance().getTimeInMillis();
    }

    //determines if the trip is happening now (true if: startTime < current time < endTime)
    public boolean isInProgress(){
        if(this.getStartTime().before(Calendar.getInstance().getTime()) &&
                this.getEndTime().after(Calendar.getInstance().getTime())) {
            return true;
        }
        else {
            return false;
        }
    }

    //determines if the trip has occurred already (true: endTime < current time)
    public boolean isHistory(){
        if(this.getEndTime().before(Calendar.getInstance().getTime())) {
            return true;
        }
        else {
            return false;
        }
    }

    //returns a boolean: true if day, month and year are all identical
    public boolean isToday() {
        Calendar today = Calendar.getInstance();
        Calendar startDate = Calendar.getInstance();
        startDate.setTime(this.getStartTime());
        return today.get(Calendar.DAY_OF_MONTH) == startDate.get(Calendar.DAY_OF_MONTH)
                && today.get(Calendar.MONTH) == startDate.get(Calendar.MONTH)
                && today.get(Calendar.YEAR) == startDate.get(Calendar.YEAR);
    }

    public int getTripId() {
        return tripId;
    }

    public String getStartBusStop() {
        return startBusStop;
    }

    public void setStartBusStop(String startBusStop) {
        this.startBusStop = startBusStop;
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

    public int getDurationMinutes() {
        return durationMinutes;
    }

    public void setDurationMinutes(int durationMinutes) {
        this.durationMinutes = durationMinutes;
    }

    public int getUserFeedback() {
        return userFeedback;
    }

    public void setUserFeedback(int userFeedback) {
        this.userFeedback = userFeedback;
    }
}