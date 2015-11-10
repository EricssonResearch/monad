package se.uu.csproject.monadclient.recyclerviews;

import java.util.Date;

public class Notify{
    String text;
    Date time;
    int iconId;

    public  Notify(String text, Date time, int iconId) {
        this.text = text;
        this.time = time;
        this.iconId = iconId;
    }
}