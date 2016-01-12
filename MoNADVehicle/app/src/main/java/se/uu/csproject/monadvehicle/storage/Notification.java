package se.uu.csproject.monadvehicle.storage;

import java.util.Date;

public class Notification {
    private int id;
    private String message;
    private Date incomingTime;


    public Notification(int id, String message, Date incomingTime) {
        this.id = id;
        this.message = message;
        this.incomingTime = incomingTime;

    }

    public int getId() {
        return id;
    }

    public String getMessage() {
        return message;
    }


    public Date getIncomingTime() {
        return incomingTime;
    }
}
