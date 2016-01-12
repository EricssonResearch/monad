package se.uu.csproject.monadvehicle.storage;

import android.util.Log;
import java.util.Date;

public class TrafficInformation {
    private double startPointLatitude;
    private double startPointLongitude;
    private Date lastModifiedUTC;
    private Date startTimeUTC;
    private Date endTimeUTC;
    private String incidentType;
    private String incidentSeverity;
    private boolean roadClosed;
    private String description;
    private double stopPointLatitude;
    private double stopPointLongitude;

    public TrafficInformation(double startPointLatitude, double startPointLongitude, Date lastModifiedUTC,
                              Date startTimeUTC, Date endTimeUTC, String incidentType, String incidentSeverity,
                              boolean roadClosed, String description, double stopPointLatitude,
                              double stopPointLongitude) {

        this.startPointLatitude = startPointLatitude;
        this.startPointLongitude = startPointLongitude;
        this.lastModifiedUTC = lastModifiedUTC;
        this.startTimeUTC = startTimeUTC;
        this.endTimeUTC = endTimeUTC;
        this.incidentType = incidentType;
        this.incidentSeverity = incidentSeverity;
        this.roadClosed = roadClosed;
        this.description = description;
        this.stopPointLatitude = stopPointLatitude;
        this.stopPointLongitude = stopPointLongitude;
    }

    public void printValues() {
        Log.d("TrafficInformation", "-- Printing Values --");
        Log.d("TrafficInformation", "StartPointLatitude: " + startPointLatitude);
        Log.d("TrafficInformation", "StartPointLongitude: " + startPointLongitude);
        Log.d("TrafficInformation", "LastModifiedUTC: " + lastModifiedUTC);
        Log.d("TrafficInformation", "StartTimeUTC: " + startTimeUTC);
        Log.d("TrafficInformation", "EndTimeUTC: " + endTimeUTC);
        Log.d("TrafficInformation", "IncidentType: " + incidentType);
        Log.d("TrafficInformation", "RoadClosed: " + roadClosed);
        Log.d("TrafficInformation", "Description: " + description);
        Log.d("TrafficInformation", "StopPointLatitude: " + stopPointLatitude);
        Log.d("TrafficInformation", "StopPointLongitude: " + stopPointLongitude);
    }

    public double getStartPointLatitude() {
        return startPointLatitude;
    }

    public void setStartPointLatitude(double startPointLatitude) {
        this.startPointLatitude = startPointLatitude;
    }

    public double getStartPointLongitude() {
        return startPointLongitude;
    }

    public void setStartPointLongitude(double startPointLongitude) {
        this.startPointLongitude = startPointLongitude;
    }

    public Date getLastModifiedUTC() {
        return lastModifiedUTC;
    }

    public void setLastModifiedUTC(Date lastModifiedUTC) {
        this.lastModifiedUTC = lastModifiedUTC;
    }

    public Date getStartTimeUTC() {
        return startTimeUTC;
    }

    public void setStartTimeUTC(Date startTimeUTC) {
        this.startTimeUTC = startTimeUTC;
    }

    public Date getEndTimeUTC() {
        return endTimeUTC;
    }

    public void setEndTimeUTC(Date endTimeUTC) {
        this.endTimeUTC = endTimeUTC;
    }

    public String getIncidentType() {
        return incidentType;
    }

    public void setIncidentType(String incidentType) {
        this.incidentType = incidentType;
    }

    public String getIncidentSeverity() {
        return incidentSeverity;
    }

    public void setIncidentSeverity(String incidentSeverity) {
        this.incidentSeverity = incidentSeverity;
    }

    public boolean isRoadClosed() {
        return roadClosed;
    }

    public void setRoadClosed(boolean roadClosed) {
        this.roadClosed = roadClosed;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public double getStopPointLatitude() {
        return stopPointLatitude;
    }

    public void setStopPointLatitude(double stopPointLatitude) {
        this.stopPointLatitude = stopPointLatitude;
    }

    public double getStopPointLongitude() {
        return stopPointLongitude;
    }

    public void setStopPointLongitude(double stopPointLongitude) {
        this.stopPointLongitude = stopPointLongitude;
    }
}
