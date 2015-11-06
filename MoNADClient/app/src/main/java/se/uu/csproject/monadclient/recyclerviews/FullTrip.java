package se.uu.csproject.monadclient.recyclerviews;

import android.content.res.Resources;
import android.os.Parcel;
import android.os.Parcelable;
import android.util.Log;

import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.GregorianCalendar;

/**
 *
 */
public class FullTrip implements Parcelable {
    private String id, requestID;
    private ArrayList<PartialTrip> partialTrips = new ArrayList<>();
    private long duration; //minutes
    private boolean booked;
    private int feedback;

    public FullTrip(String id, String requestID, ArrayList<PartialTrip> partialTrips, long duration,
                    boolean booked, int feedback) {
        this.id = id;
        this.requestID = requestID;
        this.partialTrips = partialTrips;
        this.duration = duration;
        this.booked = booked;
        this.feedback = feedback;
    }

    protected FullTrip(Parcel in) {
        id = in.readString();
        if (in.readByte() == 0x01) {
            partialTrips = new ArrayList<PartialTrip>();
            in.readList(partialTrips, PartialTrip.class.getClassLoader());
        } else {
            partialTrips = null;
        }
        duration = in.readInt();
        booked = in.readByte() != 0x00;
        feedback = in.readInt();
    }

//    public void test() {
//        Calendar calendar = new GregorianCalendar(2015, 10, 26, 10, 40, 0);
//        Date startDate1 = calendar.getTime();
//        ArrayList<String> trajectory = new ArrayList<String>() {{add("A"); add("B"); add("C");}};
//
//        PartialTrip partialTrip1 = new PartialTrip(21, "Polacks", startDate1, "Flogsta", startDate1, trajectory);
//        PartialTrip partialTrip2 = new PartialTrip(5, "Flogsta", startDate1, "Centralstation", startDate1, trajectory);
//
//        ArrayList<PartialTrip> partialTrips = new ArrayList<>();
//        partialTrips.add(partialTrip1);
//        partialTrips.add(partialTrip2);
//
//        FullTrip fullTrip1 = new FullTrip("O1", partialTrips, 100, false, -1);
//    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getRequestID(){
        return requestID;
    }

    public void setRequestID(String requestID){
        this.requestID = requestID;
    }

    public ArrayList<PartialTrip> getPartialTrips() {
        return partialTrips;
    }

    public void setPartialTrips(ArrayList<PartialTrip> partialTrips) {
        this.partialTrips = partialTrips;
    }

    public long getDuration() {
        return duration;
    }

    public void setDuration(int duration) {
        this.duration = duration;
    }

    public boolean isBooked() {
        return booked;
    }

    public void setBooked(boolean booked) {
        this.booked = booked;
    }

    public int getFeedback() {
        return feedback;
    }

    public void setFeedback(int feedback) {
        this.feedback = feedback;
    }

    public String getStartBusStop() {
        return partialTrips.get(0).getStartBusStop();
    }

    public String getEndBusStop() {
        return partialTrips.get(partialTrips.size() - 1).getEndBusStop();
    }

    // returns time in Milliseconds
    public long getTimeToDeparture() {
        return partialTrips.get(0).getStartTime().getTime() - Calendar.getInstance().getTimeInMillis();
    }

    public Date getStartTime() {
        return partialTrips.get(0).getStartTime();
    }

    public Date getEndTime() {
        return partialTrips.get(partialTrips.size() - 1).getEndTime();
    }

    public String getBusLines(){
        StringBuilder busLines = new StringBuilder("");
        for(int i = 0; i < partialTrips.size(); i++) {
            busLines.append(String.valueOf(partialTrips.get(i).getLine() + " "));
        }
        return busLines.toString();
    }

    // determines if the trip is happening now (true if: startTime < current time < endTime)
    public boolean isInProgress() {
        if (partialTrips.get(0).getStartTime().before(Calendar.getInstance().getTime()) &&
                partialTrips.get(partialTrips.size() - 1).getEndTime().after(Calendar.getInstance().getTime())) {
            return true;
        }
        else {
            return false;
        }
    }

    // Determines if the trip has occurred already (true: endTime < current time)
    public boolean isHistory(){
        if(partialTrips.get(partialTrips.size() - 1).getEndTime().before(Calendar.getInstance().getTime())) {
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
        startDate.setTime(partialTrips.get(0).getStartTime());
        return today.get(Calendar.DAY_OF_MONTH) == startDate.get(Calendar.DAY_OF_MONTH)
                && today.get(Calendar.MONTH) == startDate.get(Calendar.MONTH)
                && today.get(Calendar.YEAR) == startDate.get(Calendar.YEAR);
    }

    public void printValues(){
        Log.d("oops", "ID: " + getId());
        Log.d("oops", "Request ID: " + getRequestID());
        Log.d("oops", "Duration: " + getDuration());
        Log.d("oops", "Feedback: " + getFeedback());
    }

    @Override
    public int describeContents() {
        return 0;
    }

    @Override
    public void writeToParcel(Parcel dest, int flags) {
        dest.writeString(id);
        dest.writeString(requestID);
        if (partialTrips == null) {
            dest.writeByte((byte) (0x00));
        } else {
            dest.writeByte((byte) (0x01));
            dest.writeList(partialTrips);
        }
        dest.writeLong(duration);
        dest.writeByte((byte) (booked ? 0x01 : 0x00));
        dest.writeInt(feedback);
    }

    public static final Parcelable.Creator<FullTrip> CREATOR = new Parcelable.Creator<FullTrip>() {
        @Override
        public FullTrip createFromParcel(Parcel in) {
            return new FullTrip(in);
        }

        @Override
        public FullTrip[] newArray(int size) {
            return new FullTrip[size];
        }
    };

}
