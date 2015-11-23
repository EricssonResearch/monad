package se.uu.csproject.monadvehicle;

import java.util.Date;

public class BusStop {
    private int busId;
    private String name;
    private int latitude;
    private int longitude;
    private Date arrivalTime;
    private Date departureTime;
    private int boardingPassengers;
    private int leavingPassengers;


    public int getBusId() {
        return busId;
    }

    public String getName() {
        return name;
    }

    public int getLatitude() {
        return latitude;
    }

    public int getLongitude() {
        return longitude;
    }

    public Date getArrivalTime() {
        return arrivalTime;
    }

    public Date getDepartureTime() {
        return departureTime;
    }

    public int getBoardingPassengers() {
        return boardingPassengers;
    }

    public int getLeavingPassengers() {
        return leavingPassengers;
    }
}

/* test data for bus stops
    Calendar calendar = new GregorianCalendar(2015, 11, 23, 15, 0, 0);
    Date arrival1 = calendar.getTime();
    Calendar calendar = new GregorianCalendar(2015, 11, 23, 15, 5, 0);
    Date arrival2 = calendar.getTime();
    Calendar calendar = new GregorianCalendar(2015, 11, 23, 15, 10, 0);
    Date arrival3 = calendar.getTime();
    Calendar calendar = new GregorianCalendar(2015, 11, 23, 15, 20, 0);
    Date arrival4 = calendar.getTime();*/