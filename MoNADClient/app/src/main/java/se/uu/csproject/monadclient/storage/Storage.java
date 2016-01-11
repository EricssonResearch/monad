package se.uu.csproject.monadclient.storage;

import android.util.Log;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.Collections;

import se.uu.csproject.monadclient.NotificationsInteraction;
import se.uu.csproject.monadclient.FullTripsStartTimeComparator;
import se.uu.csproject.monadclient.NotificationsTimeComparator;

public class Storage{
    private static ArrayList<FullTrip> searchResults = new ArrayList<>();
    private static ArrayList<FullTrip> bookings = new ArrayList<>();
    private static ArrayList<FullTrip> recommendations = new ArrayList<>();
    private static ArrayList<Notify> notifications = new ArrayList<>();
    private static ArrayList<BusStop> busStops = new ArrayList<>();
    private static ArrayList<UserLocation> locations = new ArrayList<>();
    private static JSONObject changedFeedback = new JSONObject();
    private static JSONObject geofenceInfo = new JSONObject();
    private static double latitude = 0.0, longitude = 0.0;
    private static final String TAG = "oops";

    public static final int SEARCH_RESULTS = 0;
    public static final int BOOKINGS = 1;

    public static void clearAll() {
        clearSearchResults();
        clearBookings();
        clearRecommendations();
        clearNotifications();
        clearBusStops();
        clearLocations();
        clearChangedFeedback();
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
            changedFeedback.put(tripID, Integer.valueOf(feedback));
        } catch (JSONException e) {
            Log.d(TAG, e.toString());
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

	/* Methods for locations */
    public static void clearLocations() {
        locations.clear();
    }

    public static ArrayList<UserLocation> getLocations(){
        return locations;
    }

    public static boolean isEmptyLocations() {
        return locations.isEmpty();
    }

    public static void addLocation(UserLocation userLocation) {
        locations.add(userLocation);
    }

    public static void printLocations() {
        if (!isEmptyLocations()) {

            for (int i = 0; i < locations.size(); i++) {
                Log.d(TAG, locations.get(i).getLocationId() + " " + locations.get(i).getTime());
            }
        }
    }

    public static void turnLocationsToJson(){
        try {
            JSONObject location;
            for (int i = 0; i < locations.size(); i++){
                location = new JSONObject();
                location.put("latitude", locations.get(i).getLatitude());
                location.put("longitude", locations.get(i).getLongitude());
                location.put("time", locations.get(i).getTime());
                geofenceInfo.put(locations.get(i).getLocationId(), location);
            }

        } catch (JSONException e) {
            Log.d(TAG, e.toString());
        }
    }

    public static JSONObject getGeofenceInfo(){
        return geofenceInfo;
    }
}
