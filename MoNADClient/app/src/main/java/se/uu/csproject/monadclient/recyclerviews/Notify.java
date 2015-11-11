package se.uu.csproject.monadclient.recyclerviews;

import android.util.Log;

import java.util.Calendar;
import java.util.Date;

import se.uu.csproject.monadclient.R;

public class Notify {
    String id;      /* Corresponds to the Notification _id value in the database  */
    String text;
    Date time;
    int iconID;

    /* Used for generating notifications, which do not exist in the database */
    public Notify(String text, Date time, int iconID) {
        this.id = "-1";
        this.text = text;
        this.time = time;
        this.iconID = parseIconID(iconID);
    }

    /* Used for generating notifications, which are parsed from the database */
    public Notify(String id, String text, Date time, int iconID) {
        this.id = id;
        this.text = text;
        this.time = time;
        this.iconID = parseIconID(iconID);
    }

    public int parseIconID(int iconID) {
        int returnedIconID;

        if (iconID == 1) {
            returnedIconID = R.drawable.ic_assistant_photo_black_24dp;
        }
        else if (iconID == 2) {
            returnedIconID = R.drawable.ic_feedback_black_24dp;
        }
        else if (iconID == 3) {
            returnedIconID = R.drawable.ic_alarm_black_24dp;
        }
        else {
            returnedIconID = R.drawable.ic_assistant_photo_black_24dp;
        }
        return returnedIconID;
    }

    public boolean isToday() {
        Calendar today = Calendar.getInstance();
        Calendar date = Calendar.getInstance();
        date.setTime(time);
        return today.get(Calendar.DAY_OF_MONTH) == date.get(Calendar.DAY_OF_MONTH)
                && today.get(Calendar.MONTH) == date.get(Calendar.MONTH)
                && today.get(Calendar.YEAR) == date.get(Calendar.YEAR);
    }

    public void printValues() {
        Log.d("Notification", "-- Printing Values --");
        Log.d("Notification", "ID: " + this.getID());
        Log.d("Notification", "Text: " + this.getText());
        Log.d("Notification", "Time: " + getTime());
        Log.d("Notification", "IconID: " + getIconID());
    }

    public String getID() {
        return id;
    }

    public void setID(String id) {
        this.id = id;
    }

    public String getText() {
        return text;
    }

    public void setText(String text) {
        this.text = text;
    }

    public Date getTime() {
        return time;
    }

    public void setTime(Date time) {
        this.time = time;
    }

    public int getIconID() {
        return iconID;
    }

    public void setIconID(int iconID) {
        this.iconID = iconID;
    }

}