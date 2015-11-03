package se.uu.csproject.monadclient.recyclerviews;

import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.GregorianCalendar;

/**
 *
 */
public class FullTrip {
    private String id;
    private ArrayList<PartialTrip> partialTrips = new ArrayList<>();
    private int duration;
    private boolean booked;
    private int feedback;

    public FullTrip(String id, ArrayList<PartialTrip> partialTrips, int duration, boolean booked, int feedback) {
        this.id = id;
        this.partialTrips = partialTrips;
        this.duration = duration;
        this.booked = booked;
        this.feedback = feedback;
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

    public ArrayList<PartialTrip> getPartialTrips() {
        return partialTrips;
    }

    public void setPartialTrips(ArrayList<PartialTrip> partialTrips) {
        this.partialTrips = partialTrips;
    }

    public int getDuration() {
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

}
