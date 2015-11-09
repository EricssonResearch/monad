package se.uu.csproject.monadclient.recyclerviews;

import android.os.Parcel;
import android.os.Parcelable;
import android.util.Log;

import java.util.ArrayList;
import java.util.Date;

/**
 *
 */
public class PartialTrip implements Parcelable {
    private String id;                      /* Same as the user trip id in the database */
    private int line;
    private int busID;                      /* Same as the bus id in the database */
    private String startBusStop;            /* Bus stop name */
    private Date startTime;
    private String endBusStop;              /* Bus stop name */
    private Date endTime;
    private ArrayList<String> trajectory;   /* List of bus stop names */

    /* TODO: Do we need this constructor ?? */
    public PartialTrip(int line, String startBusStop, Date startTime, String endBusStop,
                       Date endTime, ArrayList<String> trajectory) {
        this.line = line;
        this.startBusStop = startBusStop;
        this.startTime = startTime;
        this.endBusStop = endBusStop;
        this.endTime = endTime;
        this.trajectory = trajectory;
    }

    public PartialTrip(String id, int line, int busID, String startBusStop, Date startTime, String endBusStop,
                       Date endTime, ArrayList<String> trajectory) {
        this.id = id;
        this.line = line;
        this.busID = busID;
        this.startBusStop = startBusStop;
        this.startTime = startTime;
        this.endBusStop = endBusStop;
        this.endTime = endTime;
        this.trajectory = trajectory;
    }

    /* TODO: Do we need entries for id and busID ?? */
    protected PartialTrip(Parcel in) {
        id = in.readString();
        line = in.readInt();
        busID = in.readInt();
        startBusStop = in.readString();
        long tmpStartTime = in.readLong();
        startTime = tmpStartTime != -1 ? new Date(tmpStartTime) : null;
        endBusStop = in.readString();
        long tmpEndTime = in.readLong();
        endTime = tmpEndTime != -1 ? new Date(tmpEndTime) : null;

        if (in.readByte() == 0x01) {
            trajectory = new ArrayList<>();
            in.readList(trajectory, String.class.getClassLoader());
        } else {
            trajectory = null;
        }
    }

    public void printValues() {
        Log.d("PartialTrip", "-- Printing Values --");
        Log.d("PartialTrip", "ID: " + getID());
        Log.d("PartialTrip", "Line: " + getLine());
        Log.d("PartialTrip", "BusID: " + getBusID());
        Log.d("PartialTrip", "Start bus stop: " + getStartBusStop());
        Log.d("PartialTrip", "Start time: " + getStartTime());
        Log.d("PartialTrip", "End bus stop: " + getEndBusStop());
        Log.d("PartialTrip", "End time: " + getEndTime());

        for (int i = 0; i < trajectory.size(); i++) {
            Log.d("PartialTrip", "Trajectory number (" + (i+1) + "): " + trajectory.get(i));
        }
    }

    @Override
    public int describeContents() {
        return 0;
    }

    @Override
    public void writeToParcel(Parcel dest, int flags) {
        dest.writeString(id);
        dest.writeInt(line);
        dest.writeInt(busID);
        dest.writeString(startBusStop);
        dest.writeLong(startTime != null ? startTime.getTime() : -1L);
        dest.writeString(endBusStop);
        dest.writeLong(endTime != null ? endTime.getTime() : -1L);
        if (trajectory == null) {
            dest.writeByte((byte) (0x00));
        } else {
            dest.writeByte((byte) (0x01));
            dest.writeList(trajectory);
        }
    }

    public static final Parcelable.Creator<PartialTrip> CREATOR = new Parcelable.Creator<PartialTrip>() {
        @Override
        public PartialTrip createFromParcel(Parcel in) {
            return new PartialTrip(in);
        }

        @Override
        public PartialTrip[] newArray(int size) {
            return new PartialTrip[size];
        }
    };

    public String getID() {
        return id;
    }

    public void setID(String id) {
        this.id = id;
    }

    public int getLine() {
        return line;
    }

    public void setLine(int line) {
        this.line = line;
    }

    public int getBusID() {
        return busID;
    }

    public void setBusID(int busID) {
        this.busID = busID;
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
