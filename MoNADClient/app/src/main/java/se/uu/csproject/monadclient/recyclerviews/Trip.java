package se.uu.csproject.monadclient.recyclerviews;

/* This class is derived from the TravelRequest collection
 * The focus is on the assigned route rather than the request itself
 * Therefore, the class attributes are not comprehensive
 */

//TODO: change times and positions data types
public class Trip {
    int tripId;
    String startPosition; // this is the bus stop coordinate
    String startTime;
    String endPosition; // this is the bus stop coordinate
    String endTime;
    int durationMinutes;
    int userFeedback;

    public Trip(int tripId, String startPosition, String startTime,
                 String endPosition, String endTime, int duration, int userFeedback) {
        this.tripId = tripId;
        this.startPosition = startPosition;
        this.startTime = startTime;
        this.endPosition = endPosition;
        this.endTime = endTime;
        this.durationMinutes = duration;
        this.userFeedback = userFeedback;
    }

    // returns time in Milliseconds
    //TODO: return the difference between variable "startTime" and the current timestamp
    public long getTimeToDeparture(){
        return 15000;
    }

    //determines if the trip has occurred yet, helps assign the right UI to the trip
    //TODO: compare startTime with currentTime
    public boolean isCurrent(){
        if(this.tripId > 2) {
            return false;
        }
        else {
            return true;
        }
    }
}