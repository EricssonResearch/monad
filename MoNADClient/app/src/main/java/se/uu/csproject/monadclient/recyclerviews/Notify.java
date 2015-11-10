package se.uu.csproject.monadclient.recyclerviews;

import java.util.Date;

import se.uu.csproject.monadclient.R;

public class Notify{
    String text;
    Date time;
    int iconId;

    public  Notify(String text, Date time, int iconId) {
        this.text = text;
        this.time = time;
        if (iconId == 1){
            this.iconId = R.drawable.ic_assistant_photo_black_24dp;
        }
        else if (iconId == 2){
            this.iconId = R.drawable.ic_feedback_black_24dp;
        }
        else if (iconId == 3){
            this.iconId = R.drawable.ic_alarm_black_24dp;
        }
        else
            this.iconId = R.drawable.ic_assistant_photo_black_24dp;
    }

    public Date getTime() {
        return time;
    }
}