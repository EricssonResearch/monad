package se.uu.csproject.monadclient.recyclerviews;

import android.util.Log;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.Collections;

import se.uu.csproject.monadclient.NotificationsInteraction;

public class Storage{
    private static ArrayList<FullTrip> searchResults = new ArrayList<>();
    private static ArrayList<FullTrip> bookings = new ArrayList<>();
    private static ArrayList<FullTrip> recommendations = new ArrayList();
    private static ArrayList<Notify> notifications = new ArrayList<>();
    private static ArrayList<BusStop> busStops = new ArrayList<>();
    private static JSONObject changedFeedback = new JSONObject();
    private static double latitude = 0.0, longitude = 0.0;

    public static final int SEARCH_RESULTS = 0;
    public static final int BOOKINGS = 1;

    public static void clearAll() {
        clearSearchResults();
        clearBookings();
        clearRecommendations();
        clearNotifications();
        clearBusStops();
    }

    /** Methods for coordinates */
    public static void setLatitude(double currentLatitude){
        latitude = currentLatitude;
    }

    public static double getLatitude(){
        return latitude;
    }

    public static void setLongitude(double currentLongitude){
        longitude = currentLongitude;
    }

    public static double getLongitude(){
        return longitude;
    }

    /** Methods for feedback */
    public static JSONObject getChangedFeedback(){
        return changedFeedback;
    }

    public static void changeFeedback(String tripID, int feedback){
        try {
            changedFeedback.put(tripID, new Integer(feedback));
        } catch (JSONException e) {
            Log.d("oops", e.toString());
        }
    }

    public static void clearChangedFeedback(){
        changedFeedback = new JSONObject();
    }

    /** Methods for searchResults */
    public static void setSearchResults(ArrayList<FullTrip> searchResults){
        Storage.searchResults = searchResults;
    }

    public static ArrayList<FullTrip> getSearchResults(){
        return searchResults;
    }

    public static void sortSearchResults() {
        Collections.sort(searchResults, new FullTripsStartTimeComparator());
    }

    public static void clearSearchResults(){
        searchResults.clear();
    }

    public static boolean isEmptySearchResults() {
        return searchResults.isEmpty();
    }

    /** Methods for bookings */
    public static void setBookings(ArrayList<FullTrip> bookings){
        Storage.bookings = bookings;
    }

    public static ArrayList<FullTrip> getBookings(){
        return bookings;
    }

    public static void addBooking(FullTrip fullTrip){
        bookings.add(fullTrip);
    }

    public static void removeBooking(FullTrip fullTrip){
        for (int i = 0; i < bookings.size(); i++){
            if (bookings.get(i).getId().equals(fullTrip.getId())){
                bookings.remove(i);
                break;
            }
        }
    }

    public static void clearBookings() {
        bookings.clear();
    }

    public static boolean isEmptyBookings() {
        return bookings.isEmpty();
    }

    public static void sortBookings(){
        Collections.sort(bookings, new FullTripsStartTimeComparator());
    }

    /** Methods for recommendations */
    public static ArrayList<FullTrip> getRecommendations() {
        return recommendations;
    }

    public static void setRecommendations(ArrayList<FullTrip> recommendations) {
        Storage.recommendations = recommendations;
    }

    public static void sortRecommendations() {
        Collections.sort(recommendations, new FullTripsStartTimeComparator());
    }

    public static boolean isEmptyRecommendations() {
        return recommendations.isEmpty();
    }

    public static void addRecommendation(FullTrip recommendation) {
        recommendations.add(recommendation);
    }

    public static void clearRecommendations() {
        recommendations.clear();
    }

    /** Methods for notifications */
    public static ArrayList<Notify> getNotifications() {
        return notifications;
    }

    public static void setNotifications(ArrayList<Notify> notifications) {
        Storage.notifications = notifications;
        sortNotifications();
    }

    public static void sortNotifications() {
        Collections.sort(notifications, new NotificationsTimeComparator());
        Collections.reverse(notifications);
    }

    public static boolean isEmptyNotifications() {
        return notifications.isEmpty();
    }

    public static void addNotification(Notify notification) {
        notifications.add(notification);
    }

    public static void addNotificationAndSort(Notify notification) {
        notifications.add(notification);
        sortNotifications();
    }

    public static void clearNotifications() {
        notifications.clear();
    }

    public static void removeNotification(int i) {
        new NotificationsInteraction("Storage").removeNotification(i);
        notifications.remove(i);
    }

    public static void printNotifications() {

        if (!isEmptyNotifications()) {

            for (int i = 0; i < notifications.size(); i++) {
                notifications.get(i).printValues();
            }
        }
    }

    public static void printSortedNotifications() {

        if (!isEmptyNotifications()) {
            sortNotifications();

            for (int i = 0; i < notifications.size(); i++) {
                notifications.get(i).printValues();
            }
        }
    }

    /** Methods for busStops */
    public static ArrayList<BusStop> getBusStops() {
        return busStops;
    }

    public static void setBusStops(ArrayList<BusStop> busStops) {
        Storage.busStops = busStops;
    }

    public static void clearBusStops() {
        busStops.clear();
    }

    public static boolean isEmptyBusStops() {
        return busStops.isEmpty();
    }

    public static void printBusStops() {

        if (!isEmptyBusStops()) {

            for (int i = 0; i < busStops.size(); i++) {
                busStops.get(i).printValues();
            }
        }
    }

    public static void initializeNotificationData() {
//        ArrayList<Notify> notifications = new ArrayList<>();
//        Calendar calendar = new GregorianCalendar(2015, 10, 26, 10, 40, 0);
//        Date time1 = calendar.getTime();
//        calendar = new GregorianCalendar(2015, 10, 26, 10, 50, 0);
//        Date time2 = calendar.getTime();
//        calendar = new GregorianCalendar(2015, 10, 26, 10, 45, 0);
//        Date time3 = calendar.getTime();
//        calendar = new GregorianCalendar(2015, 10, 26, 11, 0, 0);
//        Date time4 = calendar.getTime();
//        calendar = new GregorianCalendar(2015, 10, 27, 9, 50, 0);
//        Date time5 = calendar.getTime();
//        calendar = new GregorianCalendar(2015, 10, 27, 10, 5, 0);
//        Date time6 = calendar.getTime();
//        notifications.add(new Notify("Bus 805: 5 min delay", time1, 1));
//        notifications.add(new Notify("Bus 805: Coming in 5 min", time2, 2));
//        notifications.add(new Notify("Bus 805: Departing now", time3, 3));
//        notifications.add(new Notify("Bus 801: 5 min delay", time4, 1));
//        notifications.add(new Notify("Bus 801: Coming in 5 min", time5, 2));
//        notifications.add(new Notify("Bus 801: Departing now", time6, 3));
//
//        setNotifications(notifications);
    }

    public static void initializeRecommendationsData() {
//        Calendar calendar = new GregorianCalendar(2015, 10, 26, 10, 40, 0);
//        Date startdate1 = calendar.getTime();
//        calendar = new GregorianCalendar(2015, 10, 26, 10, 50, 0);
//        Date enddate1 = calendar.getTime();
//        calendar = new GregorianCalendar(2015, 10, 26, 10, 45, 0);
//        Date startdate2 = calendar.getTime();
//        calendar = new GregorianCalendar(2015, 10, 26, 11, 0, 0);
//        Date enddate2 = calendar.getTime();
//        calendar = new GregorianCalendar(2015, 10, 27, 9, 50, 0);
//        Date startdate3 = calendar.getTime();
//        calendar = new GregorianCalendar(2015, 10, 27, 10, 5, 0);
//        Date enddate3 = calendar.getTime();
//        calendar = new GregorianCalendar(2015, 10, 22, 11, 30, 0);
//        Date startdate4 = calendar.getTime();
//        calendar = new GregorianCalendar(2015, 10, 22, 12, 0, 0);
//        Date enddate4 = calendar.getTime();
//
//        ArrayList<PartialTrip> partialTrips = new ArrayList<>();
//        ArrayList<String> trajectory = new ArrayList<>();
//        trajectory.add("BMC");
//        trajectory.add("Akademiska Sjukhuset");
//        trajectory.add("Ekeby Bruk");
//        trajectory.add("Ekeby");
//
//        partialTrips.add(new PartialTrip("1", 2, 3, "Polacksbacken",startdate1,"Flogsta", enddate1, trajectory));
//        recommendations.add(new FullTrip("1", "2", partialTrips, 10, true, 0));
//
//        partialTrips.clear();
//        partialTrips.add(new PartialTrip("1", 2, 3, "Gamla Uppsala", startdate2, "Gottsunda", enddate2, trajectory));
//        recommendations.add(new FullTrip("2", "3", partialTrips, 15, true, 0));
//
//        partialTrips.clear();
//        partialTrips.add(new PartialTrip("1",2,3, "Granby",startdate3,"Tunna Backar", enddate3, trajectory));
//        recommendations.add(new FullTrip("3", "4", partialTrips, 15, true, 0));
//
//        partialTrips.clear();
//        partialTrips.add(new PartialTrip("1",2,3, "Kungsgatan", startdate4, "Observatoriet", enddate4, trajectory));
//        recommendations.add(new FullTrip("4", "5", partialTrips, 30, true, 0));
    }
}
