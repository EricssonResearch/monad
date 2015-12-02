package se.uu.csproject.monadclient.recyclerviews;

import java.util.Date;

import se.uu.csproject.monadclient.ClientAuthentication;

public class UserLocation {
    private String userId;
    private String locationId;
    private Date time;

    public UserLocation(String locationId, Date time) {
        this.userId = ClientAuthentication.getClientId();
        this.locationId = locationId;
        this.time = time;
    }

    public String getUserId() {
        return userId;
    }

    public String getLocationId() {
        return locationId;
    }

    public Date getTime() {
        return time;
    }

}
