package se.uu.csproject.monadclient.recyclerviews;

/* This class is derived from the TravelRequest collection
 * The focus is on the assigned route rather than the request itself
 * Therefore, the class attributes are not comprehensive
 */

//TODO: change times data types
public class Trip {
    private int tripId;
    private String startPosition; // this is the bus stop name
    private String startTime;
    private String endPosition; // this is the bus stop name
    private String endTime;
    private int durationMinutes;
    private int userFeedback;

    public Trip(int tripId, String startPosition, String startTime,
                 String endPosition, String endTime, int duration, int userFeedback) {
        this.tripId = tripId;
        this.setStartPosition(startPosition);
        this.setStartTime(startTime);
        this.setEndPosition(endPosition);
        this.setEndTime(endTime);
        this.setDurationMinutes(duration);
        this.setUserFeedback(userFeedback);
    }

    // returns time in Milliseconds
    //TODO: return the difference between variable "startTime" and the current timestamp im milliseconds)
    public long getTimeToDeparture(){
        return 15000;
    }

    //determines if the trip has occurred yet, helps assign the right UI to the trip
    //TODO: replace function with the commented one once the data types are changed
    public boolean isCurrent(){
        if(this.getTripId() > 2) {
            return false;
        }
        else {
            return true;
        }

        /*if(getTimeToDeparture() >= 0) {
            return true;
        }
        else {
            return false;
        }*/
    }


    public int getTripId() {
        return tripId;
    }

    public String getStartPosition() {
        return startPosition;
    }

    public void setStartPosition(String startPosition) {
        this.startPosition = startPosition;
    }

    public String getStartTime() {
        return startTime;
    }

    public void setStartTime(String startTime) {
        this.startTime = startTime;
    }

    public String getEndPosition() {
        return endPosition;
    }

    public void setEndPosition(String endPosition) {
        this.endPosition = endPosition;
    }

    public String getEndTime() {
        return endTime;
    }

    public void setEndTime(String endTime) {
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