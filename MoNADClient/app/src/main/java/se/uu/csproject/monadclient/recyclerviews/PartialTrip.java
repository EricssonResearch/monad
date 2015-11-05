package se.uu.csproject.monadclient.recyclerviews;

import android.os.Parcel;
import android.os.Parcelable;
import android.util.Log;

import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.GregorianCalendar;

/**
 *
 */
public class PartialTrip implements Parcelable {
    //private String id;
    private int line;
    private String startBusStop; // this is the bus stop name
    private Date startTime;
    private String endBusStop; // this is the bus stop name
    private Date endTime;
    private ArrayList<String> trajectory;

    public PartialTrip(int line, String startBusStop, Date startTime, String endBusStop,
                       Date endTime, ArrayList<String> trajectory) {
        //this.id = id;
        this.line = line;
        this.startBusStop = startBusStop;
        this.startTime = startTime;
        this.endBusStop = endBusStop;
        this.endTime = endTime;
        this.trajectory = trajectory;
    }

    protected PartialTrip(Parcel in) {
        line = in.readInt();
        startBusStop = in.readString();
        long tmpStartTime = in.readLong();
        startTime = tmpStartTime != -1 ? new Date(tmpStartTime) : null;
        endBusStop = in.readString();
        long tmpEndTime = in.readLong();
        endTime = tmpEndTime != -1 ? new Date(tmpEndTime) : null;
        if (in.readByte() == 0x01) {
            trajectory = new ArrayList<String>();
            in.readList(trajectory, String.class.getClassLoader());
        } else {
            trajectory = null;
        }
    }

    /*public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }*/

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

    public void printValues(){
        Log.d("oops", "Line: " + getLine());
        Log.d("oops", "Start time: " + getStartTime());
        Log.d("oops", "End time: " + getEndTime());
        Log.d("oops", "Start bus stop: " + getStartBusStop());
        Log.d("oops", "End bus stop: " + getEndBusStop());
        for (int i = 0; i < trajectory.size(); i++){
            Log.d("oops", "Trajectory number " + (i+1) + ": " + trajectory.get(i));
        }
    }

    @Override
    public int describeContents() {
        return 0;
    }

    @Override
    public void writeToParcel(Parcel dest, int flags) {
        dest.writeInt(line);
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

}
