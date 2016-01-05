package se.uu.csproject.monadclient.storage;

/* This class is derived from the TravelRequest collection.
 * The focus is on the assigned route rather than the request itself.
 * Therefore, the class attributes are not comprehensive.
 */

import android.os.Parcel;
import android.os.Parcelable;

import java.util.Calendar;
import java.util.Date;

public class Trip implements Parcelable {
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

    protected Trip(Parcel in) {
        tripId = in.readInt();
        startBusStop = in.readString();
        long tmpStartTime = in.readLong();
        startTime = tmpStartTime != -1 ? new Date(tmpStartTime) : null;
        endBusStop = in.readString();
        long tmpEndTime = in.readLong();
        endTime = tmpEndTime != -1 ? new Date(tmpEndTime) : null;
        durationMinutes = in.readInt();
        userFeedback = in.readInt();
    }

    // returns time in Milliseconds
    public long getTimeToDeparture(){
        return this.getStartTime().getTime() - Calendar.getInstance().getTimeInMillis();
    }

    //determines if the trip is happening now (true if: startTime < current time < endTime)
    public boolean isInProgress(){
        return this.getStartTime().before(Calendar.getInstance().getTime()) &&
                this.getEndTime().after(Calendar.getInstance().getTime());
    }

    //determines if the trip has occurred already (true: endTime < current time)
    public boolean isHistory(){
        return this.getEndTime().before(Calendar.getInstance().getTime());
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

    @Override
    public int describeContents() {
        return 0;
    }

    @Override
    public void writeToParcel(Parcel dest, int flags) {
        dest.writeInt(tripId);
        dest.writeString(startBusStop);
        dest.writeLong(startTime != null ? startTime.getTime() : -1L);
        dest.writeString(endBusStop);
        dest.writeLong(endTime != null ? endTime.getTime() : -1L);
        dest.writeInt(durationMinutes);
        dest.writeInt(userFeedback);
    }

    public static final Parcelable.Creator<Trip> CREATOR = new Parcelable.Creator<Trip>() {
        @Override
        public Trip createFromParcel(Parcel in) {
            return new Trip(in);
        }

        @Override
        public Trip[] newArray(int size) {
            return new Trip[size];
        }
    };
}